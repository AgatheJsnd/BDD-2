const { createClient } = require('@supabase/supabase-js');

// Hardcoded for debug (from .env.local)
const supabaseUrl = 'https://uisfpkjncmpavrsngwhc.supabase.co';
const supabaseKey = 'sb_publishable_NnMQUqfVcFdDMwflyDDjdw_cMh5RgeF';

const supabase = createClient(supabaseUrl, supabaseKey);

async function main() {
    console.log('Fetching last 5 transcriptions...');
    const { data, error } = await supabase
        .from('transcriptions')
        .select('id, client_name, raw_text')
        .order('created_at', { ascending: false })
        .limit(5);

    if (error) {
        console.error('Error:', error);
        return;
    }

    console.log(`Found ${data.length} records.`);
    data.forEach((t, i) => {
        console.log(`\n[${i}] Client: ${t.client_name}`);
        console.log(`Text Length: ${t.raw_text ? t.raw_text.length : 0}`);
        console.log(`Sample: ${t.raw_text ? t.raw_text.substring(0, 100) : 'N/A'}`);
    });
}

main();
