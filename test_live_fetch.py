import urllib.request
import time

sheet_id = '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8'
gid_zp = '1080948893'

t0 = time.time()
url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid_zp}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read()
        print(f"Direct fetch success! Fetched {len(data)} bytes in {time.time() - t0:.2f}s")
        print("Header snippet:", data[:150].decode('utf-8', errors='ignore'))
except Exception as e:
    print("Fetch error:", e)
