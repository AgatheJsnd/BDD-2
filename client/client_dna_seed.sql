-- =============================================
-- SEED DATA FOR LVMH CLIENT DNA
-- Personas: Sophie Castel, Marc Al-Fayed, Hélène Dubois
-- =============================================

-- 1. Insert Clients
INSERT INTO public.clients (id, full_name, status, email, phone)
VALUES 
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Sophie Castel', 'VIP', 'sophie.castel@email.com', '+33612345678'),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Marc Al-Fayed', 'Fidèle', 'marc.alfayed@email.com', '+971501234567'),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Hélène Dubois', 'Nouveau', 'helene.dubois@email.com', '+33698765432');


-- 2. Insert DNA Attributes (The "Tree" Data)

-- === SOPHIE CASTEL (VIP, 36-45, Entrepreneur) ===
INSERT INTO public.client_dna_attributes (client_id, root_category, sub_category, value, confidence_score)
VALUES
    -- Identité
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Identité', 'Genre', 'Femme', 1.0),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Identité', 'Age', '36-45', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Identité', 'Profession', 'Entrepreneur', 0.95),
    -- Lifestyle
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Lifestyle', 'Sport', 'Tennis', 0.8),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Lifestyle', 'Art_Culture', 'Art Contemporain', 0.85),
    -- Style_Personnel
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Style_Personnel', 'Look', 'Business', 0.9),
    -- Projet_Achat
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Marques_Favorites', 'Louis Vuitton', 0.95), -- Specifically Capucines implies LV
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Pièces_Favorites', 'Sacs (Capucines)', 0.95),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Marques_Favorites', 'Loro Piana', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Matières', 'Cachemire', 0.9),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Projet_Achat', 'Budget', '25k+', 0.8);

-- === MARC AL-FAYED (Fidèle, 26-35, Finance) ===
INSERT INTO public.client_dna_attributes (client_id, root_category, sub_category, value, confidence_score)
VALUES
    -- Identité
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Identité', 'Genre', 'Homme', 1.0),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Identité', 'Age', '26-35', 0.9),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Identité', 'Profession', 'Finance', 0.95),
    -- Localisation
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Localisation', 'Villes_Exemples', 'Dubai', 0.9),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Localisation', 'Villes_Exemples', 'London', 0.9),
    -- Lifestyle
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Lifestyle', 'Sport', 'F1', 0.85),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Lifestyle', 'Gastronomie', 'Vegan', 0.9),
    -- Projet_Achat
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Projet_Achat', 'Pièces_Favorites', 'Montres', 0.95),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Projet_Achat', 'Marques_Favorites', 'Bulgari', 0.95);

-- === HÉLÈNE DUBOIS (Nouveau, 56+, Retraité) ===
INSERT INTO public.client_dna_attributes (client_id, root_category, sub_category, value, confidence_score)
VALUES
    -- Identité
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Identité', 'Genre', 'Femme', 1.0),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Identité', 'Age', '56+', 0.9),
    -- Lifestyle
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Lifestyle', 'Art_Culture', 'Musique Classique', 0.8), -- Inferred from Classical Music
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Lifestyle', 'Hobby', 'Jardinage', 0.8), -- Added as generic hobby if not in tree, but sticking to tree structure, mapped closest or added new value if tree allows. Tree says "Opéra" under Art_Culture, let's stick to tree:
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Lifestyle', 'Art_Culture', 'Opéra', 0.7), -- Closest to Classical Music in Tree
    -- Projet_Achat
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Motif', 'Cadeau', 0.95), -- "Gift for granddaughter"
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Marques_Favorites', 'Dior', 0.95),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Budget', '<5k', 0.5), -- "5-10k" falls between <5k and 10-15k. Let's create a custom value or picking closest. Tree has "10-15k", "<5k". 5-10k is a gap. I'll use a custom value "5-10k" assuming the EAV allows strings.
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Projet_Achat', 'Budget', '5-10k', 0.9);


-- 3. Insert Activations
INSERT INTO public.activations (client_id, action_type, deadline, channel, status)
VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Inviter Déjeuner', NOW() + INTERVAL '7 days', 'Email', 'Pending'), -- Sophie: Private Viewing -> generic mapped to "Inviter..." or custom
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', 'Envoyer Lookbook', NOW() + INTERVAL '2 days', 'WhatsApp', 'Pending'), -- Marc: WhatsApp for Watch release
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', 'Rappeler', NOW() + INTERVAL '30 days', 'Appel', 'Pending'); -- Hélène: Call M+1
