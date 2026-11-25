import urllib.request
import json
import csv
import io
import os
import time

sheet_id = '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8'

with open('discovered_gids.json', 'r', encoding='utf-8') as f:
    sheet_map = json.load(f)

os.makedirs('data/csv', exist_ok=True)
os.makedirs('data/json', exist_ok=True)

meta = {}

for name, gid in sheet_map.items():
    csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
    safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name).strip()
    csv_path = os.path.join('data', 'csv', f'{safe_name}.csv')
    json_path = os.path.join('data', 'json', f'{safe_name}.json')
    
    print(f"Downloading '{name}' (gid: {gid})...")
    try:
        req = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Read rows
            rows = list(csv.reader(io.StringIO(content)))
            
            # Save raw rows to JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'title': name,
                    'gid': gid,
                    'rowCount': len(rows),
                    'colCount': max(len(r) for r in rows) if rows else 0,
                    'rows': rows
                }, f, indent=2)
                
            meta[name] = {
                'gid': gid,
                'rows': len(rows),
                'cols': max(len(r) for r in rows) if rows else 0,
                'preview': rows[:6] if len(rows) >= 6 else rows
            }
            print(f"  OK: {len(rows)} rows, {max(len(r) for r in rows) if rows else 0} cols")
    except Exception as e:
        print(f"  ERROR {name}: {e}")
    time.sleep(0.3)

with open('data/summary_meta.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, indent=2)

print("\nDone downloading all sheets! Summary saved to data/summary_meta.json")
