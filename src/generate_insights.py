import sys
import json
import os
import re
from mistralai import Mistral
from dotenv import load_dotenv
import concurrent.futures

# Force UTF-8
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

BATCH_SIZE = 25

def log_debug(msg):
    with open(os.path.join(os.path.dirname(__file__), 'ai_debug.log'), 'a', encoding='utf-8') as f:
        f.write(msg + "\n")

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def call_mistral(mistral, prompt):
    try:
        log_debug("Sending chunk request...")
        chat_response = mistral.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": prompt}]
        )
        content = chat_response.choices[0].message.content
        cleaned = clean_json_response(content)
        return json.loads(cleaned)
    except Exception as e:
        log_debug(f"Mistral Call Error: {e}")
        return None

def clean_json_response(content):
    content = content.strip()
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    if not content.startswith("{"):
        match = re.search(r'(\{.*\})', content, re.DOTALL)
        if match:
            content = match.group(1)
    return content

def generate_insights(data):
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return {"error": "MISTRAL_API_KEY not found"}

    mistral = Mistral(api_key=api_key)
    transcripts = data.get("transcripts", [])
    date_range = data.get("date_range", "N/A")
    current_taxonomy = data.get("current_taxonomy", [])

    log_debug(f"Starting analysis for {len(transcripts)} transcripts (Batch Size: {BATCH_SIZE})")

    # 1. Chunking & Parallel Execution - ULTRA FAST MODE
    BATCH_SIZE_OPTIMIZED = 100 # Maximize Context Window Usage (1 call > many calls)
    batches = list(chunk_list(transcripts, BATCH_SIZE_OPTIMIZED))
    batch_results = []

    def process_batch(batch_data):
        batch_index, batch_items = batch_data
        log_debug(f"Processing Batch {batch_index+1}/{len(batches)} ({len(batch_items)} items) - FAST MODE...")
        
        # Truncate slightly less aggressively to keep context, but enough for speed
        batch_short = [
            {k: (v[:400] + "...") if k == 'text' and len(v) > 400 else v for k, v in t.items()}
            for t in batch_items
        ]

        prompt = f"""
Rôle : Analyste Expert Luxe LVMH.
Tâche : Analyse RAPIDE de ce lot de {len(batch_items)} transcriptions.

Instructions Tags (STYLE STRICT : Pascal_Case, ex: "Sac_Main", "Client_VIP") :
- Extrais les thèmes clés et opportunités.
- Pas de visuel/couleur sauf emblématique.
- Inspire-toi de : {', '.join(current_taxonomy[:30])}...

Instructions Marketing :
- 2-3 Actions concrètes à fort impact.

Format JSON STRICT :
{{
  "taxonomy_suggestions": [ {{ "term": "...", "reason": "...", "category": "..." }} ],
  "marketing_actions": [ {{ "insight": "...", "suggested_action": "...", "priority": "High" }} ],
  "graph_data": {{
    "top_tags_global": [ {{ "tag": "...", "count": 1 }} ],
    "top_tags_by_language": {{ "fr": ["..."], "en": ["..."] }}
  }}
}}

Transcriptions :
{json.dumps(batch_short, indent=0, ensure_ascii=False)}

RÈGLE : JSON RAW UNIQUEMENT.
"""
        return call_mistral(mistral, prompt)

    # Run in parallel with high concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_batch = {executor.submit(process_batch, (i, b)): i for i, b in enumerate(batches)}
        for future in concurrent.futures.as_completed(future_to_batch):
            try:
                res = future.result()
                if res:
                    batch_results.append(res)
            except Exception as exc:
                log_debug(f"Batch execution failed: {exc}")

    # 2. Aggregation
    log_debug("Aggregating results...")
    aggregated = {
        "analysis_period": date_range,
        "taxonomy_suggestions": [],
        "marketing_actions": [],
        "graph_data": {
            "top_tags_global": [],
            "top_tags_by_language": {}
        }
    }

    # Simple merging strategy
    tag_counts = {}
    language_tags_acc = {} # Structure: {"fr": set(), "en": set(), ...}
    
    for res in batch_results:
        # Merge taxonomy suggestions
        if "taxonomy_suggestions" in res:
            aggregated["taxonomy_suggestions"].extend(res["taxonomy_suggestions"])
        
        # Merge marketing actions
        if "marketing_actions" in res:
            aggregated["marketing_actions"].extend(res["marketing_actions"])
            
        # Merge Tags counts
        if "graph_data" in res:
            if "top_tags_global" in res["graph_data"]:
                for item in res["graph_data"]["top_tags_global"]:
                    tag = item.get("tag")
                    count = item.get("count", 1)
                    tag_counts[tag] = tag_counts.get(tag, 0) + count
            
            # Merge Language Tags
            if "top_tags_by_language" in res["graph_data"]:
                for lang, tags in res["graph_data"]["top_tags_by_language"].items():
                    if lang not in language_tags_acc:
                        language_tags_acc[lang] = set()
                    for t in tags:
                        language_tags_acc[lang].add(t)

    # Form final top tags from aggregation
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    aggregated["graph_data"]["top_tags_global"] = [{"tag": t, "count": c} for t, c in sorted_tags]
    
    # Finalize language tags (convert sets to lists)
    for lang, tags in language_tags_acc.items():
        aggregated["graph_data"]["top_tags_by_language"][lang] = list(tags)[:10] # Top 10 per language

    # 3. Final Synthesis & Deduplication
    
    # Deduplicate taxonomy suggestions by term
    seen_terms = set()
    unique_suggestions = []
    for item in aggregated["taxonomy_suggestions"]:
        if item["term"].lower() not in seen_terms:
            seen_terms.add(item["term"].lower())
            unique_suggestions.append(item)
    aggregated["taxonomy_suggestions"] = unique_suggestions[:10] 

    # Synthesize Marketing Actions if too many
    all_actions = aggregated["marketing_actions"]
    TARGET_LIMIT = 15 # "Moins de 20"
    
    if len(all_actions) > TARGET_LIMIT: 
        log_debug(f"Synthesizing {len(all_actions)} marketing actions into top {TARGET_LIMIT}...")
        
        synthesis_prompt = f"""
Rôle : Directeur Marketing Luxe.
Tâche : Synthétiser cette liste brute d'actions marketing identifiées.
Objectif : Sélectionner et fusionner pour ne garder que les {TARGET_LIMIT} actions les plus impactantes.

Liste brute :
{json.dumps(all_actions, ensure_ascii=False)}

Format de sortie JSON :
[
  {{ "insight": "...", "suggested_action": "...", "priority": "High" }}
]
"""
        synthesis_res = call_mistral(mistral, synthesis_prompt)
        
        # Handle potential wrapped response
        final_actions = []
        if isinstance(synthesis_res, list):
            final_actions = synthesis_res
        elif isinstance(synthesis_res, dict):
            # Try to find the list in values
            for v in synthesis_res.values():
                if isinstance(v, list):
                    final_actions = v
                    break
        
        if final_actions:
             aggregated["marketing_actions"] = final_actions[:TARGET_LIMIT]
        else:
             # Fallback: simple sort
             aggregated["marketing_actions"] = sorted(all_actions, key=lambda x: 0 if x.get('priority') == 'High' else 1)[:TARGET_LIMIT]
    else:
        aggregated["marketing_actions"] = all_actions

    log_debug("Analysis complete.")
    return aggregated

if __name__ == "__main__":
    try:
        input_data = sys.stdin.read()
        if not input_data:
            print(json.dumps({"error": "No input provided"}))
            sys.exit(1)
        data = json.loads(input_data)
        result = generate_insights(data)
        print(json.dumps(result))
    except Exception as e:
        log_debug(f"Fatal Error: {e}")
        print(json.dumps({"error": str(e)}))
