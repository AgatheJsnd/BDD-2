const axios = require('axios');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: './client/.env.local' });

const API_URL = 'http://localhost:5001';
// Hardcode for reliability in test
const SUPABASE_URL = 'https://uisfpkjncmpavrsngwhc.supabase.co';
const SUPABASE_KEY = process.env.REACT_APP_SUPABASE_ANON_KEY || 'sb_publishable_NnMQUqfVcFdDMwflyDDjdw_cMh5RgeF';

async function runTests() {
    console.log("STARTING TESTS");

    // 1. Backend
    try {
        const res = await axios.get(`${API_URL}/api/status`);
        console.log(`1. Backend: ${res.status === 200 ? 'OK' : 'FAIL ' + res.status}`);
    } catch (e) {
        console.log(`1. Backend: FAIL ${e.message}`);
    }

    // 2. Supabase
    try {
        const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
        const { data, error } = await supabase.from('transcriptions').select('count', { count: 'exact', head: true });
        if (error) throw error;
        console.log(`2. Supabase: OK`);
    } catch (e) {
        console.log(`2. Supabase: FAIL ${e.message}`);
    }

    // 3. AI
    try {
        const payload = {
            date_range: "Test 2026",
            current_taxonomy: ["Sac"],
            transcripts: [{ id: 1, date: "2026-02-16", client: "Test", text: "Je veux un sac noir." }]
        };
        const res = await axios.post(`${API_URL}/api/insights`, payload);
        if (res.data.taxonomy_suggestions) {
            console.log("3. AI Analysis: OK");
        } else {
            console.log(`3. AI Analysis: FAIL (Invalid Response: ${JSON.stringify(res.data).substring(0, 50)})`);
        }
    } catch (e) {
        console.log(`3. AI Analysis: FAIL ${e.message}`);
        if (e.response) console.log(`   Response: ${JSON.stringify(e.response.data)}`);
    }
}

runTests();
