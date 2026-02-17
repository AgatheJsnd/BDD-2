-- =============================================
-- CAMPAIGN MANAGER SCHEMA
-- Deep Memory & Anti-Spam Protection
-- =============================================

-- 1. Create Campaign History Table (Invariant)
CREATE TABLE IF NOT EXISTS public.campaign_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_id UUID REFERENCES public.clients(id) ON DELETE CASCADE,
    campaign_name TEXT NOT NULL,
    campaign_tag TEXT NOT NULL,
    channel TEXT NOT NULL,
    status TEXT DEFAULT 'Sent',
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 1.1 Add Marketing Consent Column (Idempotent)
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'clients' AND column_name = 'opt_in_marketing') THEN
        ALTER TABLE public.clients ADD COLUMN opt_in_marketing BOOLEAN DEFAULT TRUE;
    END IF;
END $$;

-- Enable RLS
ALTER TABLE public.campaign_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Enable read access for all users" ON public.campaign_history FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON public.campaign_history FOR INSERT WITH CHECK (true);

-- 2. Realtime
alter publication supabase_realtime add table public.campaign_history;

-- =============================================
-- 3. RPC: Deep Memory Search (V3 - Luxury CRM Spec)
-- =============================================
-- ⚠️ IMPORTANT: We must DROP the function first because the return type has changed.
DROP FUNCTION IF EXISTS public.deep_memory_search(text, text, text);

CREATE OR REPLACE FUNCTION public.deep_memory_search(
    filter_value TEXT, 
    filter_location TEXT,
    current_campaign_tag TEXT
)
RETURNS TABLE (
    client_id UUID,
    full_name TEXT,
    email TEXT,
    matched_criteria TEXT,
    last_contacted_at TIMESTAMP WITH TIME ZONE,
    eligibility_status TEXT,
    source_date TIMESTAMP WITH TIME ZONE,
    opt_in BOOLEAN
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH matched_clients AS (
        -- 1. Match via DNA (Seed/Profiled Data)
        SELECT 
            c.id, c.full_name, c.email, c.created_at as original_date, c.opt_in_marketing,
            dna.value as criteria_value
        FROM public.clients c
        JOIN public.client_dna_attributes dna ON c.id = dna.client_id
        WHERE (filter_value = '' OR dna.value ILIKE '%' || filter_value || '%')

        UNION

        -- 2. Match via Tags (Ingested Data)
        SELECT 
            c.id, c.full_name, c.email, c.created_at as original_date, c.opt_in_marketing,
            t.tag_name as criteria_value
        FROM public.clients c
        JOIN public.transcriptions tr ON c.id = tr.client_id
        JOIN public.tags t ON tr.id = t.transcription_id
        WHERE (filter_value = '' OR t.tag_name ILIKE '%' || filter_value || '%')
    ),
    spam_check AS (
        -- Check last contact for ANY campaign (Global Anti-Spam 60 Days)
        SELECT 
            ch.client_id, 
            MAX(ch.sent_at) as last_sent
        FROM public.campaign_history ch
        GROUP BY ch.client_id
    )
    SELECT 
        mc.id,
        mc.full_name,
        mc.email,
        mc.criteria_value,
        sc.last_sent,
        CASE 
            WHEN mc.opt_in_marketing = FALSE THEN 'Opt-out'
            WHEN sc.last_sent > (NOW() - INTERVAL '60 days') THEN 'Cooldown (60d)'
            ELSE 'Eligible'
        END as status,
        mc.original_date,
        mc.opt_in_marketing
    FROM matched_clients mc
    LEFT JOIN spam_check sc ON mc.id = sc.client_id;
END;
$$;

NOTIFY pgrst, 'reload schema';
