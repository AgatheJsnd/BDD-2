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

async function run() {
    console.log("--- START ---");

    // 1. List all tables (hacky way via inspection not available, so just query)
    console.log("Querying tags...");
    const { data: tags, error: err1 } = await supabase.from('tags').select('*').limit(1);
    if (err1) console.log("ERROR accessing tags:", err1.message);
    else console.log("SUCCESS accessing tags. Count:", tags.length);

    // 2. Join
    console.log("Querying join...");
    const { data: joinData, error: err2 } = await supabase.from('transcriptions').select('id, tags(*)').limit(1);
    if (err2) {
        console.log("ERROR joining:", err2.message);
        if (err2.hint) console.log("Hint:", err2.hint);
    } else {
        console.log("SUCCESS joining.");
    }
    console.log("--- END ---");
}

run();
