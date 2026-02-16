const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// 1. Load Environment Variables manually
const envPath = path.resolve(__dirname, '../.env');
const envConfig = {};

try {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
        const [key, ...value] = line.split('=');
        if (key && value) {
            envConfig[key.trim()] = value.join('=').trim().replace(/^["']|["']$/g, '');
        }
    });
} catch (e) {
    console.error("❌ Could not read .env file:", e);
    process.exit(1);
}

const SUPABASE_URL = envConfig.SUPABASE_URL;
const SUPABASE_SERVICE_ROLE_KEY = envConfig.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SUPABASE_SERVICE_ROLE_KEY) {
    console.error("❌ Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env");
    process.exit(1);
}

console.log(`🔌 Connecting to Supabase: ${SUPABASE_URL}`);
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, {
    auth: { autoRefreshToken: false, persistSession: false }
});

const SEED_CLIENTS = [
    { id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', full_name: 'Sophie Castel', status: 'VIP', email: 'sophie.castel@email.com', phone: '+33612345678' },
    { id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', full_name: 'Marc Al-Fayed', status: 'Fidèle', email: 'marc.alfayed@email.com', phone: '+971501234567' },
    { id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', full_name: 'Hélène Dubois', status: 'Nouveau', email: 'helene.dubois@email.com', phone: '+33698765432' }
];

const SEED_ATTRIBUTES = [
    // Sophie
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Identité', sub_category: 'Genre', value: 'Femme', confidence_score: 1.0 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Identité', sub_category: 'Age', value: '36-45', confidence_score: 0.9 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Identité', sub_category: 'Profession', value: 'Entrepreneur', confidence_score: 0.95 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Lifestyle', sub_category: 'Sport', value: 'Tennis', confidence_score: 0.8 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Lifestyle', sub_category: 'Art_Culture', value: 'Art Contemporain', confidence_score: 0.85 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Style_Personnel', sub_category: 'Look', value: 'Business', confidence_score: 0.9 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Projet_Achat', sub_category: 'Marques_Favorites', value: 'Louis Vuitton', confidence_score: 0.95 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Projet_Achat', sub_category: 'Pièces_Favorites', value: 'Sacs (Capucines)', confidence_score: 0.95 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Projet_Achat', sub_category: 'Matières', value: 'Cachemire', confidence_score: 0.9 },
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', root_category: 'Projet_Achat', sub_category: 'Budget', value: '25k+', confidence_score: 0.8 },

    // Marc
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Identité', sub_category: 'Genre', value: 'Homme', confidence_score: 1.0 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Identité', sub_category: 'Age', value: '26-35', confidence_score: 0.9 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Identité', sub_category: 'Profession', value: 'Finance', confidence_score: 0.95 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Localisation', sub_category: 'Villes_Exemples', value: 'Dubai', confidence_score: 0.9 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Lifestyle', sub_category: 'Sport', value: 'F1', confidence_score: 0.85 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Lifestyle', sub_category: 'Gastronomie', value: 'Vegan', confidence_score: 0.9 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Projet_Achat', sub_category: 'Pièces_Favorites', value: 'Montres', confidence_score: 0.95 },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', root_category: 'Projet_Achat', sub_category: 'Marques_Favorites', value: 'Bulgari', confidence_score: 0.95 },

    // Hélène
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Identité', sub_category: 'Genre', value: 'Femme', confidence_score: 1.0 },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Identité', sub_category: 'Age', value: '56+', confidence_score: 0.9 },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Lifestyle', sub_category: 'Art_Culture', value: 'Musique Classique', confidence_score: 0.8 },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Lifestyle', sub_category: 'Hobby', value: 'Jardinage', confidence_score: 0.8 },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Projet_Achat', sub_category: 'Motif', value: 'Cadeau', confidence_score: 0.95 },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Projet_Achat', sub_category: 'Marques_Favorites', value: 'Dior', confidence_score: 0.95 },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', root_category: 'Projet_Achat', sub_category: 'Budget', value: '5-10k', confidence_score: 0.9 }
];

const SEED_ACTIVATIONS = [
    { client_id: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', action_type: 'Inviter Déjeuner', deadline: new Date(Date.now() + 7 * 86400000), channel: 'Email', status: 'Pending' },
    { client_id: 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380b22', action_type: 'Envoyer Lookbook', deadline: new Date(Date.now() + 2 * 86400000), channel: 'WhatsApp', status: 'Pending' },
    { client_id: 'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380c33', action_type: 'Rappeler', deadline: new Date(Date.now() + 30 * 86400000), channel: 'Appel', status: 'Pending' }
];

async function resetDB() {
    console.log("🔥 WIPING DATABASE...");

    // Delete tables in order (leaves leaf tables for last if doing delete, but we just wipe)
    // uploads (cascades to transcriptions/tags)
    const tables = ['uploads', 'transcriptions', 'tags', 'activations', 'client_dna_attributes', 'clients'];

    for (const table of tables) {
        const { error } = await supabase.from(table).delete().neq('id', '00000000-0000-0000-0000-000000000000'); // Delete *
        if (error && error.code !== 'PGRST116') { // Ignore "0 rows" if that's an error
            console.error(`Error clearing ${table}:`, error.message);
        } else {
            console.log(`✅ Cleared ${table}`);
        }
    }

    console.log("🌱 RESTORING SEED DATA...");

    // 1. Clients
    const { error: cliErr } = await supabase.from('clients').insert(SEED_CLIENTS);
    if (cliErr) console.error("Error inserting clients:", cliErr);
    else console.log("✅ Clients Restored");

    // 2. Attributes
    const { error: attErr } = await supabase.from('client_dna_attributes').insert(SEED_ATTRIBUTES);
    if (attErr) console.error("Error inserting attributes:", attErr);
    else console.log("✅ Attributes Restored");

    // 3. Activations
    const { error: actErr } = await supabase.from('activations').insert(SEED_ACTIVATIONS);
    if (actErr) console.error("Error inserting activations:", actErr);
    else console.log("✅ Activations Restored");

    console.log("✨ DATABASE RESET COMPLETE ✨");
}

resetDB();
