const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: './.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

const supabase = createClient(supabaseUrl, supabaseKey);

async function diagnose() {
    console.log("🔍 DIAGNOSTIC DÉMARRÉ...");

    // 1. Check Clients Count
    const { count: clientCount, error: countErr } = await supabase.from('clients').select('*', { count: 'exact', head: true });
    console.log(`\n👥 Total Clients: ${clientCount} (Error: ${countErr?.message || 'None'})`);

    // 2. Check for Seed Data
    const { data: sophie } = await supabase.from('clients').select('id, full_name').eq('full_name', 'Sophie Castel');
    console.log(`👤 Sophie Castel exists? ${sophie?.length > 0 ? 'YES' : 'NO'}`);

    // 3. Test SEARCH RPC (Vegan)
    console.log("\n🧪 Testing RPC 'deep_memory_search' for 'Vegan'...");
    const { data: veganResults, error: rpcErr } = await supabase.rpc('deep_memory_search', {
        filter_value: 'Vegan',
        filter_location: '',
        current_campaign_tag: 'TEST'
    });

    if (rpcErr) {
        console.error("❌ RPC ERROR:", rpcErr);
    } else {
        console.log(`✅ RPC Success! Found ${veganResults?.length} clients.`);
        if (veganResults?.length > 0) {
            console.log("   First result:", veganResults[0].full_name, "| Status:", veganResults[0].status);
        }
    }

    // 4. Test SEARCH RPC (Rappeler) - Top tag
    console.log("\n🧪 Testing RPC 'deep_memory_search' for 'Rappeler'...");
    const { data: recallResults } = await supabase.rpc('deep_memory_search', {
        filter_value: 'Rappeler',
        filter_location: '',
        current_campaign_tag: 'TEST'
    });
    console.log(`✅ Found ${recallResults?.length} clients for 'Rappeler'.`);

}

diagnose();
