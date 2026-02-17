const { createClient } = require('@supabase/supabase-js');
const fs = require('fs');
require('dotenv').config({ path: './.env.local' });

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
const supabaseKey = process.env.REACT_APP_SUPABASE_ANON_KEY;

if (!supabaseUrl || !supabaseKey) {
    console.error("❌ Missing environment variables!");
    process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function inspectTags() {
    console.log("🔍 Scanning 'tags' table...");

    // Fetch ALL tags
    const { data, error } = await supabase
        .from('tags')
        .select('tag_name');

    if (error) {
        console.error("Error fetching tags:", error);
        return;
    }

    // Count frequencies
    const counts = {};
    data.forEach(row => {
        // Normalize: Trim and Capitalize first letter? Or keep raw?
        // Let's keep raw for now to match exact DB strings
        const t = row.tag_name;
        if (t) counts[t] = (counts[t] || 0) + 1;
    });

    // Sort by frequency
    const sorted = Object.entries(counts)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 50); // Top 50

    // Write to JSON file
    fs.writeFileSync('tags_output.json', JSON.stringify(sorted, null, 2));
    console.log("✅ Written top 50 tags to tags_output.json");
}

inspectTags();
