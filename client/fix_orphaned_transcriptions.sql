-- FIX SCRIPT (V2): Link Orphaned Transcriptions to Clients
-- Corrected: Removed 'updated_at' column which does not exist in 'clients' table.

-- 1. Try to link transcriptions to existing clients (Case Insensitive Match)
UPDATE public.transcriptions t
SET client_id = c.id
FROM public.clients c
WHERE t.client_id IS NULL 
  AND t.client_name ILIKE c.full_name;

-- 2. Identify remaining orphans
-- (These are transcriptions where the client doesn't exist yet)
INSERT INTO public.clients (full_name, status)
SELECT DISTINCT t.client_name, 'Nouveau'
FROM public.transcriptions t
WHERE t.client_id IS NULL;

-- 3. Link again for the newly created clients
UPDATE public.transcriptions t
SET client_id = c.id
FROM public.clients c
WHERE t.client_id IS NULL 
  AND t.client_name ILIKE c.full_name;

-- 4. Check results
SELECT COUNT(*) as remaining_orphans FROM public.transcriptions WHERE client_id IS NULL;
