-- ⚠️ RUN THIS SCRIPT IN SUPABASE SQL EDITOR ⚠️
-- This upgrades the transcriptions table to support Smart Ingestion & Upserts.

-- 1. ADD NEW COLUMNS
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS unique_reference_id TEXT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS transcription_date TIMESTAMPTZ;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS upload_date TIMESTAMPTZ DEFAULT now();
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT now();
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS source_filename TEXT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS source_folder_batch TEXT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS uploaded_by_user_id UUID; -- Link to auth.users if needed
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS ai_confidence_score FLOAT;
ALTER TABLE public.transcriptions ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::jsonb;

-- 2. ADD UNIQUE CONSTRAINT (Critical for Upsert)
-- We first ensure unique_reference_id is populated for existing rows to avoid errors
UPDATE public.transcriptions SET unique_reference_id = id::text WHERE unique_reference_id IS NULL;

-- Now add the constraint
ALTER TABLE public.transcriptions ADD CONSTRAINT unique_transcription_ref UNIQUE (unique_reference_id);

-- 3. RELOAD CACHE
NOTIFY pgrst, 'reload schema';

SELECT 'Smart Ingestion Schema Applied!' as status;
