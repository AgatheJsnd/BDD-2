const axios = require('axios');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config({ path: './client/.env.local' }); // Load frontend env for supabase

const API_URL = 'http://localhost:5001';
const SUPABASE_URL = 'https://uisfpkjncmpavrsngwhc.supabase.co'; // Hardcoded from previous context
const SUPABASE_KEY = process.env.REACT_APP_SUPABASE_ANON_KEY || 'sb_publishable_NnMQUqfVcFdDMwflyDDjdw_cMh5RgeF';

async function runTests() {
    console.log("🚀 Starting Comprehensive System Test...\n");
    let failed = false;

    // TEST 1: Backend Health
    try {
        process.stdout.write("1. Testing Backend Connectivity... ");
        const res = await axios.get(`${API_URL}/api/status`);
        if (res.status === 200) console.log("✅ OK");
        else { console.log("❌ FAILED (Status " + res.status + ")"); failed = true; }
    } catch (e) {
        console.log("❌ FAILED (Server not reachable)");
        console.error(e.message);
        failed = true;
    }

    // TEST 2: Supabase Connection
    try {
        process.stdout.write("2. Testing Supabase Connection... ");
        const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);
        const { data, error } = await supabase.from('transcriptions').select('count', { count: 'exact', head: true });

        if (error) throw error;
        console.log(`✅ OK (Found records)`);
    } catch (e) {
        console.log("❌ FAILED");
        console.error(e.message);
        failed = true;
    }

    // TEST 3: AI Insights Endpoint (End-to-End)
    try {
        process.stdout.write("3. Testing AI Analysis Pipeline (Mock Data)... ");

        const mockPayload = {
            date_range: "Test 2026",
            current_taxonomy: ["Sac", "Luxe"],
            transcripts: [
                { id: 1, date: "2026-02-16", client: "TestUser", text: "Je cherche un sac en cuir vegan rose pour ma femme." }
            ]
        };

        // Increase timeout for AI processing
        const res = await axios.post(`${API_URL}/api/insights`, mockPayload, { timeout: 30000 });

        if (res.data.error) {
            console.log("❌ FAILED (API returned error)");
            console.error(res.data.error);
            failed = true;
        } else if (res.data.taxonomy_suggestions) {
            console.log("✅ OK (AI returned JSON)");
            // console.log("Sample Insight:", res.data.marketing_actions[0]?.insight);
        } else {
            console.log("❌ FAILED (Invalid format)");
            console.log(JSON.stringify(res.data).substring(0, 200));
            failed = true;
        }

    } catch (e) {
        console.log("❌ FAILED");
        if (e.response) {
            console.error(`Status: ${e.response.status}`);
            console.error(`Data: ${JSON.stringify(e.response.data)}`);
        } else {
            console.error(e.message);
        }
        failed = true;
    }

    console.log("\n" + "=".repeat(30));
    if (failed) {
        console.log("🔴 TESTS COMPLETED WITH ERRORS");
        process.exit(1);
    } else {
        console.log("🟢 ALL SYSTEM TESTS PASSED");
        process.exit(0);
    }
}

runTests();
