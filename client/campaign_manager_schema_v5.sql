-- CAMPAIGN MANAGER SCHEMA V5 (Temporal Engine)
-- Adds Time-Based Logic to the Deep Memory Search

CREATE OR REPLACE FUNCTION public.deep_memory_search(
    filter_value TEXT, 
    filter_location TEXT,
    current_campaign_tag TEXT
)
RETURNS TABLE (
    client_id UUID,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    source_date TIMESTAMP,
    matched_criteria TEXT,
    eligibility_status TEXT,
    opt_in BOOLEAN,
    days_remaining INT,    -- NEW: Days until event
    urgency_score INT      -- NEW: 1=High, 2=Medium, 3=Low
) 
LANGUAGE plpgsql
AS $$
DECLARE
    today_date DATE := CURRENT_DATE;
BEGIN
    RETURN QUERY
    WITH merged_data AS (
        -- 1. DNA Attributes (Seed/VIP)
        SELECT 
            c.id, c.full_name, c.email, c.phone, c.created_at as original_date, c.opt_in_marketing,
            dna.value as criteria_value,
            'DNA' as source_type
        FROM public.clients c
        JOIN public.client_dna_attributes dna ON c.id = dna.client_id
        WHERE (filter_value = '' OR dna.value ILIKE '%' || filter_value || '%')

        UNION

        -- 2. Tags (Ingested)
        SELECT 
            c.id, c.full_name, c.email, c.phone, c.created_at as original_date, c.opt_in_marketing,
            t.tag_name as criteria_value,
            'TAG' as source_type
        FROM public.clients c
        JOIN public.transcriptions tr ON c.id = tr.client_id
        JOIN public.tags t ON tr.id = t.transcription_id
        WHERE (filter_value = '' OR t.tag_name ILIKE '%' || filter_value || '%')
    ),
    score_calculation AS (
        SELECT 
            m.*,
            -- Calculate Next Anniversary Date (Naive Approach)
            CASE 
                WHEN m.criteria_value ILIKE '%Anniversaire%' OR m.criteria_value ILIKE '%Cadeau%' THEN
                    (DATE(m.original_date) + ((EXTRACT(YEAR FROM today_date) - EXTRACT(YEAR FROM m.original_date)) || ' years')::INTERVAL)::DATE
                ELSE NULL
            END as next_event_date
        FROM merged_data m
    ),
    final_calc AS (
        SELECT 
            s.*,
            -- Adjust Next Event Date if it's in the past for this year -> Move to Next Year
            CASE 
                WHEN s.next_event_date < today_date THEN (s.next_event_date + INTERVAL '1 year')::DATE
                ELSE s.next_event_date
            END as adjusted_event_date
        FROM score_calculation s
    )
    SELECT 
        f.id, 
        f.full_name, 
        f.email, 
        f.phone, 
        f.original_date,
        f.criteria_value,
        -- Status Logic (Anti-Spam + Opt-in)
        CASE 
            WHEN f.opt_in_marketing = FALSE THEN 'Exclu (Opt-out)'
            WHEN EXISTS (
                SELECT 1 FROM public.campaign_history ch 
                WHERE ch.client_id = f.id 
                AND ch.sent_at > NOW() - INTERVAL '60 days'
            ) THEN 'Cooldown (60d)'
            ELSE 'Eligible'
        END as status,
        f.opt_in_marketing,
        -- Temporal Logic
        CASE 
            WHEN f.adjusted_event_date IS NOT NULL THEN 
                (f.adjusted_event_date - today_date)::INT
            ELSE NULL 
        END as days_remaining,
        -- Urgency Score
        CASE 
            WHEN f.adjusted_event_date IS NOT NULL AND (f.adjusted_event_date - today_date) <= 7 THEN 1 -- HIGH
            WHEN f.adjusted_event_date IS NOT NULL AND (f.adjusted_event_date - today_date) <= 30 THEN 2 -- MEDIUM
            ELSE 3 -- LOW
        END as urgency_score
    FROM final_calc f;
END;
$$;

SELECT 'Schema V5 (Temporal) deployed successfully.' as status;
