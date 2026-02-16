const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Load env
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

async function check() {
    const { count: clientCount } = await supabase.from('clients').select('*', { count: 'exact', head: true });
    const { count: transCount } = await supabase.from('transcriptions').select('*', { count: 'exact', head: true });

    console.log(`Clients: ${clientCount}`);
    console.log(`Transcriptions: ${transCount}`);
}

check();
