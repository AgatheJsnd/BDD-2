-- ═══════════════════════════════════════════════════════════
-- FIX PERMISSIONS & RELOAD CACHE
-- Run this in: Supabase Dashboard → SQL Editor → New Query → Run
-- ═══════════════════════════════════════════════════════════

-- 1. Grant permissions to API roles
GRANT ALL ON public.uploads TO anon, authenticated, service_role;
GRANT ALL ON public.transcriptions TO anon, authenticated, service_role;
GRANT ALL ON public.tags TO anon, authenticated, service_role;

-- 2. Force schema cache reload
NOTIFY pgrst, 'reload schema';
