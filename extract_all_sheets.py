import urllib.request
import re
import json
import csv
import io
import os

sheet_id = '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

tab_buttons = re.findall(r'id="sheet-button-([^"]+)"[^>]*>.*?class="[^"]*docs-sheet-tab-caption[^"]*">([^<]+)<', html, re.DOTALL)
print(f"Tab buttons found via regex 1: {len(tab_buttons)}")

if not tab_buttons:
    button_ids = re.findall(r'id="sheet-button-([^"]+)"', html)
    captions = re.findall(r'class="[^"]*docs-sheet-tab-caption[^"]*">([^<]+)<', html)
    print(f"Button IDs: {button_ids}")
    print(f"Captions: {captions}")
    if len(button_ids) == len(captions):
        tab_buttons = list(zip(button_ids, captions))

sheets = {}
for gid, name in tab_buttons:
    sheets[gid] = name.strip()

print("\nFinal Sheets Mapping:")
for gid, name in sheets.items():
    print(f"  GID: {gid} -> {name}")

os.makedirs('data_sheets', exist_ok=True)
manifest = []

for gid, name in sheets.items():
    csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
    safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in name).strip()
    file_path = os.path.join('data_sheets', f'{safe_name}_{gid}.csv')
    
    try:
        r = urllib.request.Request(csv_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(r) as res:
            content = res.read().decode('utf-8', errors='ignore')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            reader = list(csv.reader(io.StringIO(content)))
            manifest.append({
                'gid': gid,
                'name': name,
                'filename': file_path,
                'rows': len(reader),
                'cols': len(reader[0]) if reader else 0,
                'header_preview': reader[:5] if len(reader) >= 5 else reader
            })
            print(f"Downloaded '{name}' ({gid}): {len(reader)} rows, {len(reader[0]) if reader else 0} cols")
    except Exception as e:
        print(f"Failed to download {name} ({gid}): {e}")

with open('sheets_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)

print("\nSaved manifest to sheets_manifest.json")
