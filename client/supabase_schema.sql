-- ═══════════════════════════════════════════════════════════
-- LVMH PULSE — Supabase Schema
-- Run this in: Supabase Dashboard → SQL Editor → New Query → Run
-- ═══════════════════════════════════════════════════════════

-- CLEANUP: Drop old tables
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS transcriptions CASCADE;
DROP TABLE IF EXISTS uploads CASCADE;
DROP TABLE IF EXISTS opportunities CASCADE;

-- ═══ TABLE 1: UPLOADS ═══
CREATE TABLE uploads (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  filename TEXT,
  status TEXT DEFAULT 'processing',
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══ TABLE 2: TRANSCRIPTIONS ═══
CREATE TABLE transcriptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  upload_id UUID REFERENCES uploads(id) ON DELETE CASCADE,
  client_name TEXT,
  content_summary TEXT,
  sentiment TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══ TABLE 3: TAGS ═══
CREATE TABLE tags (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  transcription_id UUID REFERENCES transcriptions(id) ON DELETE CASCADE,
  tag_name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- ═══ ROW LEVEL SECURITY ═══
ALTER TABLE uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE tags ENABLE ROW LEVEL SECURITY;

CREATE POLICY "all_uploads" ON uploads FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "all_transcriptions" ON transcriptions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "all_tags" ON tags FOR ALL USING (true) WITH CHECK (true);

-- ═══ SEED DATA ═══
INSERT INTO uploads (filename, status) VALUES ('batch_initial.cvc', 'completed');

WITH u AS (SELECT id FROM uploads LIMIT 1)
INSERT INTO transcriptions (upload_id, client_name, content_summary, sentiment)
SELECT u.id, v.name, v.summary, v.sentiment FROM u,
(VALUES
  ('Sophie M.', 'Intéressée par collection Capucines SS26', 'positif'),
  ('Marc D.', 'Demande entretien souliers, client fidèle', 'neutre'),
  ('Hélène R.', 'Cross-sell montre Tank après achat sac', 'positif'),
  ('Louis P.', 'Anniversaire dans 30 jours, budget élevé', 'positif'),
  ('Claire B.', 'Réclamation livraison internationale', 'négatif')
) AS v(name, summary, sentiment);

INSERT INTO tags (transcription_id, tag_name)
SELECT t.id, v.tag FROM transcriptions t
CROSS JOIN (VALUES ('Maroquinerie'), ('Anniversaire'), ('VIP'), ('Cross-sell'), ('Souliers'), ('Montres'), ('Voyage')) AS v(tag)
WHERE random() > 0.5;
