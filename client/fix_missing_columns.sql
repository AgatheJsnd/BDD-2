-- ⚠️ RUN THIS IN SUPABASE SQL EDITOR ⚠️
-- Fixes "column transcriptions.created_at does not exist"

-- 1. Ensure created_at exists
ALTER TABLE public.transcriptions 
ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT now();

-- 2. Ensure other critical columns exist (just in case)
ALTER TABLE public.transcriptions 
ADD COLUMN IF NOT EXISTS client_name TEXT,
ADD COLUMN IF NOT EXISTS content_summary TEXT,
ADD COLUMN IF NOT EXISTS sentiment TEXT,
ADD COLUMN IF NOT EXISTS raw_text TEXT;

-- 3. Backfill created_at if it was null (optional but good)
UPDATE public.transcriptions 
SET created_at = now() 
WHERE created_at IS NULL;

-- 4. Reload Schema
NOTIFY pgrst, 'reload schema';

SELECT 'Fixed missing columns!' as status;
