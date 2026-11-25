import urllib.request
import re
import json

sheet_id = '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

captions = ['Master Links', 'Bifurcation Report ZP', 'Progress Report ZP', 'District Wise Report ZP', 'Final Candidate List', 'Bifurcation Report BP', 'Progress Report BP', 'Block Pramukh', 'District Wise Report BP', 'Koshi', 'Champaran', 'Magadh', 'Mithilanchal', 'Munger', 'Nalanda', 'Patna', 'Tirhut', 'Saran', 'Samastipur', 'Sahabad', 'Seemanchal']

sheet_map = {}
for cap in captions:
    # Look for caption in html and see surrounding text
    pos = 0
    found_gids = []
    while True:
        pos = html.find(cap, pos)
        if pos == -1:
            break
        # Look backwards and forwards 300 characters
        snippet = html[max(0, pos-200):min(len(html), pos+200)]
        # Search for number like gid
        # In our earlier snippet:
        # [2,0,\"158363757\",[{\"1\":[[0,0,\"Progress Report ZP\"]
        # [3,0,\"1080948893\",[{\"1\":[[0,0,\"District Wise Report ZP\"]
        # [4,0,\"1838483440\",[{\"1\":[[0,0,\"Final Candidate List\"]
        m = re.findall(r'\"(\d+)\",\[\{\"1\":\[\[0,0,\"' + re.escape(cap) + r'\"', snippet)
        if m:
            found_gids.extend(m)
        else:
            # Also check if pattern is [index, 0, "gid", [{"1":[[0,0,"caption"
            # or in general any digits near it
            m2 = re.findall(r'(\d{5,})', snippet)
            # filter out non-gids if needed
            # print snippet for debugging if needed
        pos += len(cap)
    if found_gids:
        sheet_map[cap] = found_gids[0]
        print(f"Matched {cap} -> {found_gids[0]}")
    else:
        print(f"NOT matched: {cap}")

print("\nFull search for pattern [\\d+, 0, \\\"gid\\\":")
all_pairs = re.findall(r'\[\d+,0,\\\"(\d+)\\\",\[\{\\\"1\\\":\[\[0,0,\\\"([^\\\"]+)\\\"', html)
print(f"Found with triple backslash: {len(all_pairs)}")
for gid, name in all_pairs:
    sheet_map[name] = gid
    print(f"  {name} -> {gid}")

# Try another escape level
if len(all_pairs) < 5:
    all_pairs2 = re.findall(r'\"(\d{5,11})\",\[\{\"1\":\[\[0,0,\"([^\"]+)\"', html)
    print(f"Found with single escape: {len(all_pairs2)}")
    for gid, name in all_pairs2:
        sheet_map[name] = gid
        print(f"  {name} -> {gid}")

with open('discovered_gids.json', 'w') as f:
    json.dump(sheet_map, f, indent=2)
