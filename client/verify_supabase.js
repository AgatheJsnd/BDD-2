const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
const path = require('path');

// Manually parse .env.local
const envPath = path.join(__dirname, '.env.local');
let supabaseUrl = '';
let supabaseKey = '';

if (fs.existsSync(envPath)) {
    const envConfig = fs.readFileSync(envPath, 'utf8');
    envConfig.split('\n').forEach(line => {
        const [key, value] = line.split('=');
        if (key === 'REACT_APP_SUPABASE_URL') supabaseUrl = value?.trim();
        if (key === 'REACT_APP_SUPABASE_ANON_KEY') supabaseKey = value?.trim();
    });
}

console.log('Checking Supabase connection...');
console.log('URL:', supabaseUrl ? 'Found' : 'Missing');
console.log('Key:', supabaseKey ? 'Found' : 'Missing');

if (!supabaseUrl || !supabaseKey) {
    console.error('❌ Missing environment variables in .env.local');
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function check() {
    console.log('Attempting to select from "uploads"...');
    const { count, error } = await supabase
        .from('uploads')
        .select('*', { count: 'exact', head: true });

    if (error) {
        console.error('❌ Error accessing "uploads" table:');
        console.error(JSON.stringify(error, null, 2));
        if (error.code === '42P01') {
            console.log('\n💡 DIAGNOSIS: The table "uploads" does not exist. You need to run the SQL schema.');
        }
    } else {
        console.log(`✅ SELECT Success! Found "uploads" table with ${count} records.`);

        // Try INSERT
        console.log('Attempting INSERT...');
        const { data, error: insertError } = await supabase
            .from('uploads')
            .insert({ filename: 'test_verify.cvc', status: 'test' })
            .select();

        if (insertError) {
            console.error('❌ INSERT Failed:', insertError.message);
            console.error('Full Error:', JSON.stringify(insertError, null, 2));
        } else {
            console.log('✅ INSERT Success! Created record:', data && data[0] ? data[0].id : 'unknown');
        }
    }
}

check();
