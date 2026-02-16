-- ⚠️ RUN THIS IN SUPABASE SQL EDITOR TO FIX EVERYTHING ⚠️

-- 1. CLEANUP (Supprime les anciennes versions si elles existent mal)
DROP TABLE IF EXISTS public.tags CASCADE;
DROP TABLE IF EXISTS public.transcriptions CASCADE;
DROP TABLE IF EXISTS public.uploads CASCADE;

-- 2. CREATE TABLES (Création propre)
CREATE TABLE public.uploads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  filename TEXT NOT NULL,
  status TEXT DEFAULT 'processing',
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.transcriptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  upload_id UUID REFERENCES public.uploads(id) ON DELETE CASCADE,
  client_name TEXT,
  content_summary TEXT,
  sentiment TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE public.tags (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  transcription_id UUID REFERENCES public.transcriptions(id) ON DELETE CASCADE,
  tag_name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. ENABLE RLS (Sécurité)
ALTER TABLE public.uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tags ENABLE ROW LEVEL SECURITY;

-- 4. POLICIES (Accès ouvert pour la démo - évite les erreurs 403)
CREATE POLICY "Enable all access for all users" ON public.uploads FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for all users" ON public.transcriptions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Enable all access for all users" ON public.tags FOR ALL USING (true) WITH CHECK (true);

-- 5. PERMISSIONS (CRITICAL - Donne les droits à l'API)
GRANT ALL ON TABLE public.uploads TO anon, authenticated, service_role;
GRANT ALL ON TABLE public.transcriptions TO anon, authenticated, service_role;
GRANT ALL ON TABLE public.tags TO anon, authenticated, service_role;

-- 6. RELOAD CACHE (Force l'API à voir les nouvelles tables)
NOTIFY pgrst, 'reload schema';

-- 7. VERIFICATION DATA
INSERT INTO uploads (filename, status) VALUES ('init_check.cvc', 'completed');
