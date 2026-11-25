import json
import os

with open('public/dashboard_data.json', 'r', encoding='utf-8') as f:
    full_data = json.load(f)

# Extract summary without heavy candidate lists
summary = {
    'meta': full_data['meta'],
    'snapshot': full_data['snapshot'],
    'zp': {
        'districtWise': full_data['zp']['districtWise'],
        'progressByZone': full_data['zp']['progressByZone'],
        'bifurcationTotals': full_data['zp']['bifurcationTotals'],
        'candidatesCount': len(full_data['zp']['candidates'])
    },
    'bp': {
        'districtWise': full_data['bp']['districtWise'],
        'progressByZone': full_data['bp']['progressByZone'],
        'bifurcationTotals': full_data['bp']['bifurcationTotals'],
        'candidatesCount': len(full_data['bp']['candidates'])
    }
}

with open('public/dashboard_summary.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2)

with open('public/zp_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(full_data['zp']['candidates'], f)

with open('public/bp_candidates.json', 'w', encoding='utf-8') as f:
    json.dump(full_data['bp']['candidates'], f)

print(f"Summary size: {os.path.getsize('public/dashboard_summary.json') / 1024:.1f} KB")
print(f"ZP candidates size: {os.path.getsize('public/zp_candidates.json') / 1024:.1f} KB")
print(f"BP candidates size: {os.path.getsize('public/bp_candidates.json') / 1024:.1f} KB")
