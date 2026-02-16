-- ⚠️ RUN THIS SCRIPT IN SUPABASE SQL EDITOR ⚠️
-- This fixes ALL missing columns (client_name, content_summary, sentiment, upload_id).

-- 1. Add missing columns safely
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS client_name TEXT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS content_summary TEXT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS sentiment TEXT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS upload_id UUID REFERENCES public.uploads(id) ON DELETE CASCADE;

-- 2. Force the API to refresh its cache
NOTIFY pgrst, 'reload schema';

-- 3. Confirm success
SELECT 'Fixed! All columns (client_name, summary, sentiment) restored.' as status;
