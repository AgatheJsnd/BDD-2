const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: './.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

async function debugRelationships() {
    console.log("🔍 TRACING RELATIONSHIPS for tag 'Rappeler'...");

    // 1. Get a Tag
    const { data: tags, error: tagErr } = await supabase
        .from('tags')
        .select('*')
        .eq('tag_name', 'Rappeler')
        .limit(1);

    if (tagErr || tags.length === 0) {
        console.error("❌ Tag 'Rappeler' not found in tags table!", tagErr);
        return;
    }

    const tag = tags[0];
    console.log(`✅ Step 1: Found Tag ID ${tag.id} linked to Transcription ID ${tag.transcription_id}`);

    // 2. Get Transcription
    const { data: trans, error: transErr } = await supabase
        .from('transcriptions')
        .select('*')
        .eq('id', tag.transcription_id)
        .single();

    if (transErr || !trans) {
        console.error(`❌ Step 2: Transcription ID ${tag.transcription_id} NOT FOUND! Orphaned Tag.`);
        return;
    }

    console.log(`✅ Step 2: Found Transcription. Linked to Client ID ${trans.client_id}`);

    // 3. Get Client
    if (!trans.client_id) {
        console.error("❌ Step 3: Transcription has NO client_id (NULL).");
        return;
    }

    const { data: client, error: clientErr } = await supabase
        .from('clients')
        .select('*')
        .eq('id', trans.client_id)
        .single();

    if (clientErr || !client) {
        console.error(`❌ Step 3: Client ID ${trans.client_id} NOT FOUND! Orphaned Transcription.`);
        return;
    }

    console.log(`✅ Step 3: Found Client '${client.full_name}'. The chain is COMPLETE.`);
}

debugRelationships();
