import re
import json

print("=== CHECKING DOM INTEGRITY BETWEEN index.html AND app.js ===")

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Check all getElementById in JS
get_by_id_matches = re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", js)
unique_ids_in_js = sorted(list(set(get_by_id_matches)))

missing_ids = []
for el_id in unique_ids_in_js:
    if f'id="{el_id}"' not in html and f"id='{el_id}'" not in html:
        missing_ids.append(el_id)

print(f"Total getElementById calls: {len(get_by_id_matches)} ({len(unique_ids_in_js)} unique)")
if missing_ids:
    print(f"WARNING: IDs in app.js not found in index.html ({len(missing_ids)}):", missing_ids)
else:
    print("ALL IDs in app.js successfully exist in index.html!")

# 2. Check all onclick functions in HTML
onclick_matches = re.findall(r"onclick=[\"']([^\"'\(]+)", html)
unique_onclicks = sorted(list(set(onclick_matches)))

missing_funcs = []
for fn in unique_onclicks:
    fn_clean = fn.strip()
    if 'document.' in fn_clean or 'event.' in fn_clean or not fn_clean:
        continue
    # check if function definition exists in js
    if f"function {fn_clean}" not in js and f"{fn_clean} = " not in js and f"const {fn_clean}" not in js:
        missing_funcs.append(fn_clean)

print(f"\nTotal onclick handlers: {len(onclick_matches)} ({len(unique_onclicks)} unique)")
if missing_funcs:
    print(f"WARNING: Functions in index.html not found in app.js ({len(missing_funcs)}):", missing_funcs)
else:
    print("ALL onclick functions in index.html exist in app.js!")

# 3. Check JSON files
print("\n=== VERIFYING JSON DATASETS ===")
try:
    with open('public/dashboard_summary.json', 'r', encoding='utf-8') as f:
        summary = json.load(f)
    print("dashboard_summary.json is valid JSON.")
    print("  Meta:", summary['meta']['title'])
    print("  ZP Seats:", summary['snapshot']['zp']['totalSeats'], "Identified:", summary['snapshot']['zp']['totalIdentified'])
    print("  BP Blocks:", summary['snapshot']['bp']['totalBlocks'], "Identified:", summary['snapshot']['bp']['totalIdentified'])
    print("  ZP Districts Count:", len(summary['zp']['districtWise']))
    print("  BP Districts Count:", len(summary['bp']['districtWise']))
except Exception as e:
    print("ERROR in dashboard_summary.json:", e)

try:
    with open('public/zp_candidates.json', 'r', encoding='utf-8') as f:
        zp_cands = json.load(f)
    print(f"zp_candidates.json is valid JSON with {len(zp_cands)} candidates.")
except Exception as e:
    print("ERROR in zp_candidates.json:", e)

try:
    with open('public/bp_candidates.json', 'r', encoding='utf-8') as f:
        bp_cands = json.load(f)
    print(f"bp_candidates.json is valid JSON with {len(bp_cands)} candidates.")
except Exception as e:
    print("ERROR in bp_candidates.json:", e)

# 4. Check syntax of app.js using node
import subprocess
result = subprocess.run(["node", "--check", "app.js"], capture_output=True, text=True)
if result.returncode == 0:
    print("\napp.js syntax is 100% VALID (node --check passed)!")
else:
    print("\napp.js syntax error:", result.stderr)
