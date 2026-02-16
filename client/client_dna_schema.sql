-- =============================================
-- 1. CLEANUP (Drop existing if conflict)
-- =============================================
DROP TABLE IF EXISTS public.activations CASCADE;
DROP TABLE IF EXISTS public.client_dna_attributes CASCADE;
DROP TABLE IF EXISTS public.transcriptions CASCADE;
DROP TABLE IF EXISTS public.clients CASCADE;

-- =============================================
-- 2. CREATE TABLES
-- =============================================

-- Table: clients
-- The core identity of the luxury client.
CREATE TABLE public.clients (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    full_name TEXT NOT NULL,
    status TEXT CHECK (status IN ('VIP', 'Fidèle', 'Nouveau', 'Occasionnel', 'Prospect')),
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Table: transcriptions
-- Raw source of the profiling data (e.g., conversation logs, audio transcriptions).
CREATE TABLE public.transcriptions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_id UUID REFERENCES public.clients(id) ON DELETE CASCADE,
    client_name TEXT, -- Added back for backward compatibility
    upload_id UUID REFERENCES public.uploads(id) ON DELETE CASCADE, -- For file uploads
    audio_file_url TEXT,
    raw_text TEXT,
    content_summary TEXT, -- Extracted summary
    sentiment TEXT,       -- Extracted sentiment
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Table: client_dna_attributes (The EAV Table)
-- Stores the granular profile data linked to the Profiling Tree.
CREATE TABLE public.client_dna_attributes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_id UUID REFERENCES public.clients(id) ON DELETE CASCADE,
    root_category TEXT NOT NULL, -- e.g., 'Lifestyle', 'Identité', 'Localisation'
    sub_category TEXT NOT NULL,  -- e.g., 'Sport > Individuel', 'Villes_Exemples'
    value TEXT NOT NULL,         -- e.g., 'Tennis', 'Paris'
    confidence_score FLOAT DEFAULT 1.0,
    source_transcription_id UUID REFERENCES public.transcriptions(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Table: activations
-- Actionable next steps derived from the profile.
CREATE TABLE public.activations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    client_id UUID REFERENCES public.clients(id) ON DELETE CASCADE,
    action_type TEXT NOT NULL, -- e.g., 'Rappeler', 'Inviter Déjeuner'
    deadline TIMESTAMP WITH TIME ZONE,
    channel TEXT,              -- e.g., 'WhatsApp', 'Email'
    status TEXT DEFAULT 'Pending' CHECK (status IN ('Pending', 'Done', 'Cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- =============================================
-- 3. ENABLE RLS (Row Level Security)
-- =============================================
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.client_dna_attributes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activations ENABLE ROW LEVEL SECURITY;

-- =============================================
-- 4. CREATE POLICIES (Allow public access for demo)
-- =============================================
-- Policy for 'clients'
CREATE POLICY "Enable read access for all users" ON public.clients FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON public.clients FOR INSERT WITH CHECK (true);
CREATE POLICY "Enable update access for all users" ON public.clients FOR UPDATE USING (true);

-- Policy for 'transcriptions'
CREATE POLICY "Enable read access for all users" ON public.transcriptions FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON public.transcriptions FOR INSERT WITH CHECK (true);

-- Policy for 'client_dna_attributes'
CREATE POLICY "Enable read access for all users" ON public.client_dna_attributes FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON public.client_dna_attributes FOR INSERT WITH CHECK (true);

-- Policy for 'activations'
CREATE POLICY "Enable read access for all users" ON public.activations FOR SELECT USING (true);
CREATE POLICY "Enable insert access for all users" ON public.activations FOR INSERT WITH CHECK (true);

-- =============================================
-- 5. REALTIME
-- =============================================
-- Add tables to publication for real-time subscription
alter publication supabase_realtime add table public.clients;
alter publication supabase_realtime add table public.client_dna_attributes;
alter publication supabase_realtime add table public.activations;

-- Output confirmation
-- =============================================
-- 6. RELOAD CACHE (Force API to see schema changes)
-- =============================================
NOTIFY pgrst, 'reload schema';

SELECT 'Schema created successfully' as status;
