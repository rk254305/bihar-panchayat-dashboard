import json
import csv
import glob
import os

with open('data/summary_meta.json', 'r', encoding='utf-8') as f:
    meta = json.load(f)

print("="*60)
print("ANALYSIS OF KEY SHEETS")
print("="*60)

for name, info in meta.items():
    print(f"\n--- {name} (gid: {info['gid']}, rows: {info['rows']}, cols: {info['cols']}) ---")
    for idx, r in enumerate(info['preview'][:4]):
        clean_row = [c.strip().replace('\n', ' ') for c in r if c.strip()]
        print(f"  Row {idx}: {clean_row[:8]}")
