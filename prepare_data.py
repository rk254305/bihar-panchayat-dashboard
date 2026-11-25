import json
import csv
import os

def clean_val(v):
    if v is None:
        return ""
    return str(v).strip().replace('\r', '')

def parse_num(v, default=0):
    if not v:
        return default
    v_clean = str(v).replace(',', '').replace('%', '').strip()
    try:
        if '.' in v_clean:
            return float(v_clean)
        return int(v_clean)
    except:
        return default

# 1. ZP District-Wise
zp_districts = []
with open('data/csv/District Wise Report ZP.csv', 'r', encoding='utf-8') as f:
    rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]

# Row 2 is Total, Row 3 is Header, Row 4+ is Districts
for r in rows[4:]:
    zone = clean_val(r[0])
    district = clean_val(r[2])
    if not district or district.lower() in ('district', 'total'):
        continue
    seats = parse_num(r[3])
    s1 = parse_num(r[4])
    s2 = parse_num(r[5])
    s3 = parse_num(r[6])
    s4 = parse_num(r[7])
    s5 = parse_num(r[8])
    total_id = parse_num(r[9])
    g1 = parse_num(r[10])
    g2 = parse_num(r[11])
    g3 = parse_num(r[12])
    g4 = parse_num(r[13])
    g5 = parse_num(r[14])
    pct = clean_val(r[15])
    
    zp_districts.append({
        'zone': zone,
        'mapping': clean_val(r[1]),
        'district': district,
        'seats': seats,
        'seatsWith1': s1,
        'seatsWith2': s2,
        'seatsWith3': s3,
        'seatsWith4': s4,
        'seatsWith5': s5,
        'totalIdentified': total_id,
        'gap1': g1,
        'gap2': g2,
        'gap3': g3,
        'gap4': g4,
        'gap5': g5,
        'progressPct': pct,
        'coverage1Pct': round((s1 / seats * 100), 1) if seats > 0 else 0
    })

# 2. BP District-Wise
bp_districts = []
with open('data/csv/District Wise Report BP.csv', 'r', encoding='utf-8') as f:
    rows_bp = [r for r in csv.reader(f) if any(c.strip() for c in r)]

for r in rows_bp[3:]:
    zone = clean_val(r[0])
    district = clean_val(r[2])
    if not district or district.lower() in ('district', 'total'):
        continue
    blocks = parse_num(r[3])
    b1 = parse_num(r[4])
    b2 = parse_num(r[5])
    b3 = parse_num(r[6])
    total_id = parse_num(r[7])
    g1 = parse_num(r[8])
    g2 = parse_num(r[9])
    g3 = parse_num(r[10])
    
    bp_districts.append({
        'zone': zone,
        'mapping': clean_val(r[1]),
        'district': district,
        'blocks': blocks,
        'blocksWith1': b1,
        'blocksWith2': b2,
        'blocksWith3': b3,
        'totalIdentified': total_id,
        'gap1': g1,
        'gap2': g2,
        'gap3': g3,
        'coverage1Pct': round((b1 / blocks * 100), 1) if blocks > 0 else 0
    })

# 3. ZP Progress Zones (from Progress Report ZP.csv)
zp_progress_zones = [
    {'zone': 'Magadh', 'seats': 96, 'target5x': 480, 'identified': 385, 'remaining': 95, 'coveragePct': '80%'},
    {'zone': 'Sahabad', 'seats': 103, 'target5x': 515, 'identified': 373, 'remaining': 142, 'coveragePct': '72%'},
    {'zone': 'Champaran', 'seats': 98, 'target5x': 490, 'identified': 337, 'remaining': 153, 'coveragePct': '69%'},
    {'zone': 'Saran', 'seats': 121, 'target5x': 605, 'identified': 370, 'remaining': 235, 'coveragePct': '61%'},
    {'zone': 'Munger', 'seats': 90, 'target5x': 450, 'identified': 262, 'remaining': 188, 'coveragePct': '58%'},
    {'zone': 'Mithilanchal', 'seats': 103, 'target5x': 515, 'identified': 283, 'remaining': 232, 'coveragePct': '55%'},
    {'zone': 'Nalanda', 'seats': 77, 'target5x': 385, 'identified': 205, 'remaining': 180, 'coveragePct': '53%'},
    {'zone': 'Samastipur', 'seats': 127, 'target5x': 635, 'identified': 328, 'remaining': 307, 'coveragePct': '52%'},
    {'zone': 'Koshi', 'seats': 87, 'target5x': 435, 'identified': 218, 'remaining': 217, 'coveragePct': '50%'},
    {'zone': 'Tirhut', 'seats': 98, 'target5x': 490, 'identified': 241, 'remaining': 249, 'coveragePct': '49%'},
    {'zone': 'Seemanchal', 'seats': 115, 'target5x': 575, 'identified': 197, 'remaining': 378, 'coveragePct': '34%'},
    {'zone': 'Patna', 'seats': 45, 'target5x': 225, 'identified': 70, 'remaining': 155, 'coveragePct': '31%'},
]

# 4. BP Progress Zones (from Progress Report BP.csv)
bp_progress_zones = [
    {'zone': 'Koshi', 'blocks': 41, 'target3x': 123, 'identified': 63, 'remaining': 60, 'coveragePct': '51.2%'},
    {'zone': 'Seemanchal', 'blocks': 46, 'target3x': 138, 'identified': 65, 'remaining': 73, 'coveragePct': '47.1%'},
    {'zone': 'Samastipur', 'blocks': 38, 'target3x': 114, 'identified': 47, 'remaining': 67, 'coveragePct': '41.2%'},
    {'zone': 'Magadh', 'blocks': 47, 'target3x': 141, 'identified': 54, 'remaining': 87, 'coveragePct': '38.3%'},
    {'zone': 'Nalanda', 'blocks': 47, 'target3x': 141, 'identified': 51, 'remaining': 90, 'coveragePct': '36.2%'},
    {'zone': 'Saran', 'blocks': 53, 'target3x': 159, 'identified': 49, 'remaining': 110, 'coveragePct': '30.8%'},
    {'zone': 'Sahabad', 'blocks': 55, 'target3x': 165, 'identified': 51, 'remaining': 114, 'coveragePct': '30.9%'},
    {'zone': 'Tirhut', 'blocks': 54, 'target3x': 162, 'identified': 48, 'remaining': 114, 'coveragePct': '29.6%'},
    {'zone': 'Munger', 'blocks': 46, 'target3x': 138, 'identified': 38, 'remaining': 100, 'coveragePct': '27.5%'},
    {'zone': 'Mithilanchal', 'blocks': 39, 'target3x': 117, 'identified': 28, 'remaining': 89, 'coveragePct': '23.9%'},
    {'zone': 'Champaran', 'blocks': 45, 'target3x': 135, 'identified': 27, 'remaining': 108, 'coveragePct': '20.0%'},
    {'zone': 'Patna', 'blocks': 23, 'target3x': 69, 'identified': 6, 'remaining': 63, 'coveragePct': '8.7%'},
]

# 5. Bifurcation Totals
zp_bifurcation_totals = {
    'total': 3269,
    'male': 2563,
    'female': 607,
    'yuva': 1050,
    'minority': 275,
    'general': 1337
}

bp_bifurcation_totals = {
    'total': 527,
    'male': 379,
    'female': 40,
    'yuva': 144,
    'minority': 6,
    'general': 337
}

# 6. Parse ZP Candidates
zp_candidates = []
with open('data/csv/Final Candidate List.csv', 'r', encoding='utf-8') as f:
    fc_rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]

for idx, r in enumerate(fc_rows[2:]):
    name = clean_val(r[12]) if len(r) > 12 else ''
    if not name:
        continue
    zp_candidates.append({
        'id': f"ZP-{idx+1:04d}",
        'zone': clean_val(r[0]) if len(r) > 0 else '',
        'district': clean_val(r[1]) if len(r) > 1 else '',
        'pc': clean_val(r[2]) if len(r) > 2 else '',
        'ac': clean_val(r[3]) if len(r) > 3 else '',
        'block': clean_val(r[4]) if len(r) > 4 else '',
        'panchayat': clean_val(r[5]) if len(r) > 5 else '',
        'zpSeat': clean_val(r[6]) if len(r) > 6 else '',
        'seatReservation': clean_val(r[7]) if len(r) > 7 else '',
        'chairman': clean_val(r[8]) if len(r) > 8 else '',
        'viceChairman': clean_val(r[9]) if len(r) > 9 else '',
        'jsptPoc': clean_val(r[10]) if len(r) > 10 else '',
        'name': name,
        'contact': clean_val(r[13]) if len(r) > 13 else '',
        'category': clean_val(r[14]) if len(r) > 14 else '',
        'caste': clean_val(r[15]) if len(r) > 15 else '',
        'gender': clean_val(r[16]) if len(r) > 16 else '',
        'age': clean_val(r[17]) if len(r) > 17 else '',
        'briefProfile': clean_val(r[18]) if len(r) > 18 else '',
        'jsDesignation': clean_val(r[19]) if len(r) > 19 else '',
        'recommendation': clean_val(r[20]) if len(r) > 20 else '',
        'remarks': clean_val(r[21]) if len(r) > 21 else '',
        'wantsContest': clean_val(r[22]) if len(r) > 22 else '',
        'priority': clean_val(r[23]) if len(r) > 23 else ''
    })

# 7. Parse BP Candidates
bp_candidates = []
with open('data/csv/Block Pramukh.csv', 'r', encoding='utf-8') as f:
    bp_rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]

for idx, r in enumerate(bp_rows[2:]):
    name = clean_val(r[13]) if len(r) > 13 else ''
    if not name:
        continue
    bp_candidates.append({
        'id': f"BP-{idx+1:04d}",
        'zone': clean_val(r[0]) if len(r) > 0 else '',
        'district': clean_val(r[1]) if len(r) > 1 else '',
        'pc': clean_val(r[2]) if len(r) > 2 else '',
        'ac': clean_val(r[3]) if len(r) > 3 else '',
        'block': clean_val(r[4]) if len(r) > 4 else '',
        'panchayat': clean_val(r[5]) if len(r) > 5 else '',
        'zpSeat': clean_val(r[6]) if len(r) > 6 else '',
        'seatReservation': clean_val(r[7]) if len(r) > 7 else '',
        'chairman': clean_val(r[8]) if len(r) > 8 else '',
        'viceChairman': clean_val(r[9]) if len(r) > 9 else '',
        'candidateCategory': clean_val(r[10]) if len(r) > 10 else '',
        'jsptPoc': clean_val(r[11]) if len(r) > 11 else '',
        'name': name,
        'contact': clean_val(r[14]) if len(r) > 14 else '',
        'gender': clean_val(r[15]) if len(r) > 15 else '',
        'age': clean_val(r[16]) if len(r) > 16 else '',
        'caste': clean_val(r[17]) if len(r) > 17 else '',
        'category': clean_val(r[18]) if len(r) > 18 else '',
        'briefProfile': clean_val(r[19]) if len(r) > 19 else '',
        'wantsContest': clean_val(r[20]) if len(r) > 20 else '',
        'remarks': clean_val(r[21]) if len(r) > 21 else '',
        'jsDesignation': clean_val(r[22]) if len(r) > 22 else '',
        'pkMeetingStatus': clean_val(r[23]) if len(r) > 23 else '',
        'meetingDate': clean_val(r[24]) if len(r) > 24 else ''
    })

zones = sorted(list(set([d['zone'] for d in zp_districts if d['zone']])))

# Master output dictionary
dashboard_data = {
    'meta': {
        'title': 'Bihar Panchayat Candidate Identification Dashboard 2026',
        'subtitle': 'Executive Tracking System: Zila Parishad & Block Pramukh',
        'reportDate': '24 November 2026',
        'sourceSpreadsheetId': '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8',
        'zonesCount': len(zones),
        'zonesList': zones
    },
    'snapshot': {
        'zp': {
            'title': 'Zila Parishad (ZP)',
            'totalSeats': 1160,
            'targetMultiplier': 5,
            'targetCandidates': 5800,
            'totalIdentified': 3269,
            'remainingCandidates': 2531,
            'overallCoveragePct': 56.4,
            'seatsWithAtLeast1': 1120,
            'seatsWith1Pct': 96.6,
            'seatsWith2': 1031,
            'seatsWith3': 640,
            'seatsWith4': 297,
            'seatsWith5Plus': 122,
            'gaps': {
                'gap1': 40,
                'gap2': 129,
                'gap3': 520,
                'gap4': 863,
                'gap5': 1038
            },
            'demographics': zp_bifurcation_totals,
            'candidateRecordsCount': len(zp_candidates)
        },
        'bp': {
            'title': 'Block Pramukh (BP)',
            'totalBlocks': 534,
            'targetMultiplier': 3,
            'targetCandidates': 1602,
            'totalIdentified': 527,
            'remainingBlocks': 1075,
            'overallCoveragePct': 32.9,
            'blocksWithAtLeast1': 527,
            'gaps': {
                'gap1': 1075,
                'gap2': 1075,
                'gap3': 1075
            },
            'demographics': bp_bifurcation_totals,
            'candidateRecordsCount': len(bp_candidates)
        }
    },
    'zp': {
        'districtWise': zp_districts,
        'progressByZone': zp_progress_zones,
        'bifurcationTotals': zp_bifurcation_totals,
        'candidates': zp_candidates
    },
    'bp': {
        'districtWise': bp_districts,
        'progressByZone': bp_progress_zones,
        'bifurcationTotals': bp_bifurcation_totals,
        'candidates': bp_candidates
    }
}

os.makedirs('public', exist_ok=True)
with open('public/dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, indent=2)

print(f"Done! public/dashboard_data.json created: {os.path.getsize('public/dashboard_data.json') / 1024:.1f} KB")
print(f"ZP candidates: {len(zp_candidates)}, BP candidates: {len(bp_candidates)}")
print(f"ZP districts: {len(zp_districts)}, BP districts: {len(bp_districts)}")
