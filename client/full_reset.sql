-- ⚠️ RUN THIS SCRIPT IN SUPABASE SQL EDITOR ⚠️
-- This performs a "Factory Reset":
-- 1. Deletes ALL uploaded files & analytics
-- 2. Deletes ALL client data
-- 3. Re-creates the 3 Seed Clients (Sophie, Marc, Hélène)

-- =============================================
-- 1. WIPE EVERYTHING (Cascade handles relations)
-- =============================================
TRUNCATE TABLE public.uploads CASCADE;
TRUNCATE TABLE public.transcriptions CASCADE;
TRUNCATE TABLE public.tags CASCADE;
TRUNCATE TABLE public.client_dna_attributes CASCADE;
TRUNCATE TABLE public.activations CASCADE;
TRUNCATE TABLE public.clients CASCADE;

-- =============================================
-- 2. RESTORE SEED DATA (Sophie, Marc, Hélène)
-- =============================================

-- Clients
INSERT INTO public.clients (id, full_name, status, email, phone)
VALUES 
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Sophie Castel', 'VIP', 'sophie.castel@email.com', '+33612345678'),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Marc Al-Fayed', 'Fidèle', 'marc.alfayed@email.com', '+971501234567'),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Hélène Dubois', 'Nouveau', 'helene.dubois@email.com', '+33698765432');

-- DNA Attributes
INSERT INTO public.client_dna_attributes (client_id, root_category, sub_category, value, confidence_score)
VALUES
    -- Sophie Castel
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Identité', 'Genre', 'Femme', 1.0),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Identité', 'Age', '36-45', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Identité', 'Profession', 'Entrepreneur', 0.95),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Lifestyle', 'Sport', 'Tennis', 0.8),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Lifestyle', 'Art_Culture', 'Art Contemporain', 0.85),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Style_Personnel', 'Look', 'Business', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Marques_Favorites', 'Louis Vuitton', 0.95),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Pièces_Favorites', 'Sacs (Capucines)', 0.95),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Marques_Favorites', 'Loro Piana', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Matières', 'Cachemire', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Budget', '25k+', 0.8),

    -- Marc Al-Fayed
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Identité', 'Genre', 'Homme', 1.0),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Identité', 'Age', '26-35', 0.9),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Identité', 'Profession', 'Finance', 0.95),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Localisation', 'Villes_Exemples', 'Dubai', 0.9),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Localisation', 'Villes_Exemples', 'London', 0.9),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Lifestyle', 'Sport', 'F1', 0.85),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Lifestyle', 'Gastronomie', 'Vegan', 0.9),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Projet_Achat', 'Pièces_Favorites', 'Montres', 0.95),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Projet_Achat', 'Marques_Favorites', 'Bulgari', 0.95),

    -- Hélène Dubois
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Identité', 'Genre', 'Femme', 1.0),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Identité', 'Age', '56+', 0.9),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Lifestyle', 'Art_Culture', 'Musique Classique', 0.8),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Lifestyle', 'Hobby', 'Jardinage', 0.8),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Lifestyle', 'Art_Culture', 'Opéra', 0.7),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Motif', 'Cadeau', 0.95),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Marques_Favorites', 'Dior', 0.95),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Budget', '5-10k', 0.9);

-- Activations
INSERT INTO public.activations (client_id, action_type, deadline, channel, status)
VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Inviter Déjeuner', NOW() + INTERVAL '7 days', 'Email', 'Pending'),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Envoyer Lookbook', NOW() + INTERVAL '2 days', 'WhatsApp', 'Pending'),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Rappeler', NOW() + INTERVAL '30 days', 'Appel', 'Pending');

SELECT 'Factory Reset Complete: Cleaned all data & Restored Seed Clients.' as status;
