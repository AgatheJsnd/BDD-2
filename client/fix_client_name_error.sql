-- ⚠️ RUN THIS SCRIPT IN SUPABASE SQL EDITOR ⚠️
-- This will fix the "Could not find client_name column" error instantly.

-- 1. Ensure the column exists (Safe to run multiple times)
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS client_name TEXT;

-- 2. Force the API to refresh its cache
NOTIFY pgrst, 'reload schema';

-- 3. Confirm success
SELECT 'Fixed! You can now upload files.' as status;
