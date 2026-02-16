const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

const envPath = path.resolve(__dirname, '../.env');
const envConfig = {};
try {
    const envContent = fs.readFileSync(envPath, 'utf8');
    envContent.split('\n').forEach(line => {
        const [key, ...value] = line.split('=');
        if (key && value) envConfig[key.trim()] = value.join('=').trim().replace(/^["']|["']$/g, '');
    });
} catch (e) { }

const supabase = createClient(envConfig.SUPABASE_URL, envConfig.SUPABASE_SERVICE_ROLE_KEY);

async function inspect() {
    console.log("Inspecting FKs...");
    // We can't query information_schema easily via JS client (RLS usually blocks or it's not exposed via API).
    // But we can try to RPC if possible, or just guess.
    // Actually, Supabase exposes introspection via the 'rpc' interface if enabled? No.

    // Alternative: Try to select from 'tags' and include 'transcriptions' (reverse).
    const { data, error } = await supabase.from('tags').select('*, transcriptions(*)').limit(1);
    if (error) {
        console.log("Reverse join error:", error.message);
        if (error.hint) console.log("Hint:", error.hint);
    } else {
        console.log("Reverse join SUCCESS");
    }
}

inspect();
