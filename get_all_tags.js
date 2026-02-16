const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: '.env' });

const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);

async function getAllTags() {
    const { data, error } = await supabase
        .from('tags')
        .select('tag_name');

    if (error) {
        console.error(error);
        return;
    }

    const uniqueTags = [...new Set(data.map(t => t.tag_name))].sort();
    console.log(JSON.stringify(uniqueTags, null, 2));
}

getAllTags();
