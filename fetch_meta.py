import urllib.request
import re
import json

sheet_id = '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8'
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit'

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    print(f"HTML downloaded: {len(html)} bytes")
    
    # Save a snippet or search for sheetsData / bootstrap data
    # Look for bootstrapData or WIZ_global_data
    sheet_matches = []
    
    # Check for sheet names and ids
    for match in re.finditer(r'\[(\d+),0,"([^"]+)",', html):
        sheet_matches.append((match.group(1), match.group(2)))
        
    # Another common Google sheets pattern:
    # "gid":"1080948893","name":"ZP Snapshot" or similar
    matches2 = re.findall(r'\[(?:\d+),\"([^\"]+)\",(?:\d+),(\d+),', html)
    
    # Look for tab info JSON pattern
    # e.g. "sheets":[ ... ]
    m_sheets = re.search(r'var bootstrapData = (.*?);</script>', html)
    if m_sheets:
        print("Found bootstrapData!")
    
    # Let's search broadly for 1080948893 in html to see surrounding structure
    idx = html.find('1080948893')
    if idx != -1:
        start = max(0, idx - 500)
        end = min(len(html), idx + 500)
        print("Context around 1080948893:")
        print(html[start:end])
    else:
        print("gid 1080948893 not found directly in html")

except Exception as e:
    print('Error:', e)
