import json
import re

with open('public/zp_candidates.json', 'r', encoding='utf-8') as f:
    zp_cands = json.load(f)

with open('public/bp_candidates.json', 'r', encoding='utf-8') as f:
    bp_cands = json.load(f)

print(f"Total ZP Candidates: {len(zp_cands)}")
missing_phone_zp = [c for c in zp_cands if not c.get('contact') or not c['contact'].strip()]
invalid_phone_zp = []
for c in zp_cands:
    p = c.get('contact', '').strip().replace('\n', ' ')
    if p:
        digits = re.findall(r'\d', p)
        if len(digits) < 10:
            invalid_phone_zp.append((c['name'], p))

missing_gender_zp = [c for c in zp_cands if not c.get('gender') or not c['gender'].strip()]
missing_category_zp = [c for c in zp_cands if not c.get('category') or not c['category'].strip()]
missing_profile_zp = [c for c in zp_cands if not c.get('briefProfile') or not c['briefProfile'].strip()]

print(f"ZP Missing Phone: {len(missing_phone_zp)}")
print(f"ZP Invalid Phone (<10 digits): {len(invalid_phone_zp)} (examples: {invalid_phone_zp[:5]})")
print(f"ZP Missing Gender: {len(missing_gender_zp)}")
print(f"ZP Missing Category: {len(missing_category_zp)}")
print(f"ZP Missing Profile: {len(missing_profile_zp)}")

print(f"\nTotal BP Candidates: {len(bp_cands)}")
missing_phone_bp = [c for c in bp_cands if not c.get('contact') or not c['contact'].strip()]
missing_meeting_bp = [c for c in bp_cands if not c.get('pkMeetingStatus') or not c['pkMeetingStatus'].strip()]
print(f"BP Missing Phone: {len(missing_phone_bp)}")
print(f"BP Missing PK Meeting Status: {len(missing_meeting_bp)}")
