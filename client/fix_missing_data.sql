-- ⚠️ RUN THIS IN SUPABASE SQL EDITOR ⚠️
-- Fixes "Search not working" by populating empty columns

-- 1. Backfill Client Names (Generic for old data)
UPDATE public.transcriptions 
SET client_name = 'Client Inconnu ' || substring(id::text, 1, 4)
WHERE client_name IS NULL OR client_name = '';

-- 2. Backfill Summaries
UPDATE public.transcriptions 
SET content_summary = 'Résumé généré automatiquement pour la démo.'
WHERE content_summary IS NULL OR content_summary = '';

-- 3. Backfill Sentiment (Random distribution for demo)
UPDATE public.transcriptions 
SET sentiment = CASE floor(random() * 3)::int
    WHEN 0 THEN 'positif'
    WHEN 1 THEN 'neutre'
    WHEN 2 THEN 'négatif'
END
WHERE sentiment IS NULL;

-- 4. Reload Schema
NOTIFY pgrst, 'reload schema';

SELECT 'Data backfilled successfully!' as status;
