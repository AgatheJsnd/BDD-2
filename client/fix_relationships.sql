-- ⚠️ RUN THIS IN SUPABASE SQL EDITOR ⚠️
-- Fixes "Could not find a relationship between 'transcriptions' and 'tags'"

-- 1. Ensure the foreign key exists explicitly
ALTER TABLE public.tags 
  DROP CONSTRAINT IF EXISTS tags_transcription_id_fkey;

ALTER TABLE public.tags
  ADD CONSTRAINT tags_transcription_id_fkey 
  FOREIGN KEY (transcription_id) 
  REFERENCES public.transcriptions(id)
  ON DELETE CASCADE;

-- 2. Grant permissions again just in case
GRANT ALL ON TABLE public.tags TO anon, authenticated, service_role;
GRANT ALL ON TABLE public.transcriptions TO anon, authenticated, service_role;

-- 3. Force Schema Cache Reload (Critical for PostgREST to see the FK)
NOTIFY pgrst, 'reload schema';

SELECT 'Relationship Fixed & Cache Reloaded' as status;
