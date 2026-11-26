import urllib.request
import concurrent.futures
import csv
import io
import json
import os
import time
from datetime import datetime, timezone

SHEET_ID = '1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8'
ZP_MASTER_SHEET_ID = '1vr-jXwkeaDZ700FMsJ0ZLkuEp7HgAuGrVThpE-2403s'

SHEET_GIDS = {
    'District Wise Report ZP': (SHEET_ID, '1080948893'),
    'District Wise Report BP': (SHEET_ID, '1882208574'),
    'Progress Report ZP': (SHEET_ID, '158363757'),
    'Progress Report BP': (SHEET_ID, '1179274087'),
    'Bifurcation Report ZP': (SHEET_ID, '1111122327'),
    'Bifurcation Report BP': (SHEET_ID, '363657193'),
    'Final Candidate List': (ZP_MASTER_SHEET_ID, '1040425931'),
    'Block Pramukh': (SHEET_ID, '2018617771')
}

_cache = {
    'last_synced': None,
    'summary': None,
    'zp_candidates': None,
    'bp_candidates': None,
    'is_syncing': False
}

def clean_val(v):
    if v is None:
        return ""
    return str(v).strip().replace('\r', '')

def parse_num(v, default=0):
    if v is None or v == '':
        return default
    v_clean = str(v).replace(',', '').replace('%', '').strip()
    try:
        if '.' in v_clean:
            return float(v_clean)
        return int(v_clean)
    except Exception:
        return default

def fetch_single_sheet(name, gid, spreadsheet_id=SHEET_ID):
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        rows = list(csv.reader(io.StringIO(content)))
        return name, rows

def fetch_all_live_sheets():
    t0 = time.time()
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_name = {
            executor.submit(fetch_single_sheet, name, gid, sid): name
            for name, (sid, gid) in SHEET_GIDS.items()
        }
        for future in concurrent.futures.as_completed(future_to_name):
            name = future_to_name[future]
            try:
                sheet_name, rows = future.result()
                results[sheet_name] = [r for r in rows if any(c.strip() for c in r)]
            except Exception as e:
                print(f"Error fetching live sheet {name}: {e}")
                results[name] = []
    print(f"Parallel fetch of {len(results)} sheets completed in {time.time() - t0:.2f}s")
    return results

def _try_write_json(rel_path, payload, indent=None):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=indent, ensure_ascii=False)
    except OSError:
        # Vercel serverless environment has a read-only filesystem outside /tmp
        pass

def process_live_data(sheets_data, persist=True):
    # 1. ZP District-Wise
    zp_districts = []
    rows_zp_dw = sheets_data.get('District Wise Report ZP', [])
    for r in rows_zp_dw[4:]:
        zone = clean_val(r[0]) if len(r) > 0 else ''
        district = clean_val(r[2]) if len(r) > 2 else ''
        if not district or district.lower() in ('district', 'total'):
            continue
        seats = parse_num(r[3]) if len(r) > 3 else 0
        s1 = parse_num(r[4]) if len(r) > 4 else 0
        zp_districts.append({
            'zone': zone,
            'mapping': clean_val(r[1]) if len(r) > 1 else '',
            'district': district,
            'seats': seats,
            'seatsWith1': s1,
            'seatsWith2': parse_num(r[5]) if len(r) > 5 else 0,
            'seatsWith3': parse_num(r[6]) if len(r) > 6 else 0,
            'seatsWith4': parse_num(r[7]) if len(r) > 7 else 0,
            'seatsWith5': parse_num(r[8]) if len(r) > 8 else 0,
            'totalIdentified': parse_num(r[9]) if len(r) > 9 else 0,
            'gap1': parse_num(r[10]) if len(r) > 10 else 0,
            'gap2': parse_num(r[11]) if len(r) > 11 else 0,
            'gap3': parse_num(r[12]) if len(r) > 12 else 0,
            'gap4': parse_num(r[13]) if len(r) > 13 else 0,
            'gap5': parse_num(r[14]) if len(r) > 14 else 0,
            'progressPct': clean_val(r[15]) if len(r) > 15 else '0%',
            'coverage1Pct': round((s1 / seats * 100), 1) if seats > 0 else 0
        })

    # 2. BP District-Wise (col 4 = Block With 0 Members; cols 5..11 = 1/2/3/Total/GAP1/GAP2/GAP3)
    bp_districts = []
    rows_bp_dw = sheets_data.get('District Wise Report BP', [])
    for r in rows_bp_dw[3:]:
        zone = clean_val(r[0]) if len(r) > 0 else ''
        district = clean_val(r[2]) if len(r) > 2 else ''
        if not district or district.lower() in ('district', 'total'):
            continue
        blocks = parse_num(r[3]) if len(r) > 3 else 0
        b0 = parse_num(r[4]) if len(r) > 4 else 0
        b1 = parse_num(r[5]) if len(r) > 5 else 0
        bp_districts.append({
            'zone': zone,
            'mapping': clean_val(r[1]) if len(r) > 1 else '',
            'district': district,
            'blocks': blocks,
            'blocksWith0': b0,
            'blocksWith1': b1,
            'blocksWith2': parse_num(r[6]) if len(r) > 6 else 0,
            'blocksWith3': parse_num(r[7]) if len(r) > 7 else 0,
            'totalIdentified': parse_num(r[8]) if len(r) > 8 else 0,
            'gap1': parse_num(r[9]) if len(r) > 9 else 0,
            'gap2': parse_num(r[10]) if len(r) > 10 else 0,
            'gap3': parse_num(r[11]) if len(r) > 11 else 0,
            'coverage1Pct': round((b1 / blocks * 100), 1) if blocks > 0 else 0
        })

    # 3. Parse ZP Progress Report dynamically (top summary table only: rows[:18])
    zp_progress_zones = []
    zp_snap_vals = {}
    for r in sheets_data.get('Progress Report ZP', [])[:18]:
        lbl = clean_val(r[0]).lower() if len(r) > 0 else ''
        val_c = clean_val(r[2]) if len(r) > 2 else ''
        if lbl and val_c:
            if 'total zp seats' in lbl: zp_snap_vals['totalSeats'] = parse_num(val_c)
            elif lbl.startswith('1 candidate'): zp_snap_vals['seats1'] = parse_num(val_c)
            elif lbl.startswith('2 candidate'): zp_snap_vals['seats2'] = parse_num(val_c)
            elif lbl.startswith('3'): zp_snap_vals['seats3'] = parse_num(val_c)
            elif lbl.startswith('4 candidate'): zp_snap_vals['seats4'] = parse_num(val_c)
            elif lbl.startswith('5 candidate'): zp_snap_vals['seats5'] = parse_num(val_c)
            elif 'total identified candidate' in lbl: zp_snap_vals['totalIdentified'] = parse_num(val_c)
        z_name = clean_val(r[3]) if len(r) > 3 else ''
        if z_name and z_name.lower() not in ('zone', 'total', '12') and not z_name.isdigit() and 'candidate' not in z_name.lower():
            seats_z = parse_num(r[5]) if len(r) > 5 else 0
            tgt_z = parse_num(r[7]) if len(r) > 7 else seats_z * 5
            id_z = parse_num(r[9]) if len(r) > 9 else 0
            rem_z = parse_num(r[11]) if len(r) > 11 else max(0, tgt_z - id_z)
            cov_z = clean_val(r[13]) if len(r) > 13 else (f"{round(id_z / tgt_z * 100)}%" if tgt_z else '0%')
            if seats_z > 0:
                zp_progress_zones.append({
                    'zone': z_name, 'seats': seats_z, 'target5x': tgt_z,
                    'identified': id_z, 'remaining': rem_z, 'coveragePct': cov_z
                })

    # 4. Parse BP Progress Report dynamically (top summary table only: rows[:18])
    bp_progress_zones = []
    bp_snap_vals = {}
    for r in sheets_data.get('Progress Report BP', [])[:18]:
        lbl = clean_val(r[0]).lower() if len(r) > 0 else ''
        val_c = clean_val(r[2]) if len(r) > 2 else ''
        if lbl and val_c:
            if 'total block pramukh seats' in lbl: bp_snap_vals['totalBlocks'] = parse_num(val_c)
            elif lbl.startswith('block pramukh candidates required'): bp_snap_vals['target3x'] = parse_num(val_c)
            elif lbl.startswith('0 candidate'): bp_snap_vals['blocks0'] = parse_num(val_c)
            elif lbl.startswith('1 candidate'): bp_snap_vals['blocks1'] = parse_num(val_c)
            elif lbl.startswith('2 candidate'): bp_snap_vals['blocks2'] = parse_num(val_c)
            elif lbl.startswith('3 candidate'): bp_snap_vals['blocks3'] = parse_num(val_c)
        z_name = clean_val(r[4]) if len(r) > 4 else ''
        if z_name and z_name.lower() not in ('zone', 'total', '12') and not z_name.isdigit() and 'candidate' not in z_name.lower():
            blks_z = parse_num(r[7]) if len(r) > 7 else 0
            tgt_z = parse_num(r[9]) if len(r) > 9 else blks_z * 3
            id_z = parse_num(r[11]) if len(r) > 11 else 0
            rem_z = parse_num(r[13]) if len(r) > 13 else max(0, tgt_z - id_z)
            if blks_z > 0:
                cov_pct = f"{round((id_z / tgt_z * 100), 1)}%" if tgt_z > 0 else "0.0%"
                bp_progress_zones.append({
                    'zone': z_name, 'blocks': blks_z, 'target3x': tgt_z,
                    'identified': id_z, 'remaining': rem_z, 'coveragePct': cov_pct
                })

    # 5. Dynamic Bifurcation Totals
    zp_bifurcation_totals = {'total': 0, 'male': 0, 'female': 0, 'yuva': 0, 'minority': 0, 'general': 0}
    for r in sheets_data.get('Bifurcation Report ZP', [])[:6]:
        if r and clean_val(r[0]).lower() == 'total':
            zp_bifurcation_totals = {
                'total': parse_num(r[3]) if len(r) > 3 else 0,
                'male': parse_num(r[4]) if len(r) > 4 else 0,
                'female': parse_num(r[5]) if len(r) > 5 else 0,
                'yuva': parse_num(r[6]) if len(r) > 6 else 0,
                'minority': parse_num(r[7]) if len(r) > 7 else 0,
                'general': parse_num(r[8]) if len(r) > 8 else 0,
            }
            break

    bp_bifurcation_totals = {'total': 0, 'male': 0, 'female': 0, 'yuva': 0, 'minority': 0, 'general': 0}
    for r in sheets_data.get('Bifurcation Report BP', [])[:6]:
        if r and clean_val(r[0]).lower() == 'total':
            bp_bifurcation_totals = {
                'total': parse_num(r[3]) if len(r) > 3 else 0,
                'male': parse_num(r[4]) if len(r) > 4 else 0,
                'female': parse_num(r[5]) if len(r) > 5 else 0,
                'yuva': parse_num(r[6]) if len(r) > 6 else 0,
                'minority': parse_num(r[7]) if len(r) > 7 else 0,
                'general': parse_num(r[8]) if len(r) > 8 else 0,
            }
            break

    # 6. Parse ZP Candidates (auto-detect schema between 1vr FCL [col 11] and 1Dr5p FCL [col 12])
    zp_candidates = []
    fcl_rows = sheets_data.get('Final Candidate List', [])
    fcl_hdr = next((r for r in fcl_rows[:3] if any('candidate name' in clean_val(c).lower() for c in r)), [])
    has_poc_col = any('poc' in clean_val(c).lower() for c in fcl_hdr)
    start_row = 2 if (fcl_rows and 'zone details' in clean_val(fcl_rows[0][0]).lower()) else 1
    for idx, r in enumerate(fcl_rows[start_row:]):
        if has_poc_col:
            name = clean_val(r[12]) if len(r) > 12 else ''
            poc = clean_val(r[10]) if len(r) > 10 else ''
            off = 13
        else:
            name = clean_val(r[11]) if len(r) > 11 else ''
            poc = ''
            off = 12
        if not name or 'probable zp candidate' in name.lower():
            continue
        zp_candidates.append({
            'id': f"ZP-{len(zp_candidates)+1:04d}",
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
            'jsptPoc': poc,
            'name': name,
            'contact': clean_val(r[off]) if len(r) > off else '',
            'category': clean_val(r[off+1]) if len(r) > off+1 else '',
            'caste': clean_val(r[off+2]) if len(r) > off+2 else '',
            'gender': clean_val(r[off+3]) if len(r) > off+3 else '',
            'age': clean_val(r[off+4]) if len(r) > off+4 else '',
            'briefProfile': clean_val(r[off+5]) if len(r) > off+5 else '',
            'jsDesignation': clean_val(r[off+6]) if len(r) > off+6 else '',
            'recommendation': clean_val(r[off+7]) if len(r) > off+7 else '',
            'remarks': clean_val(r[off+8]) if len(r) > off+8 else '',
            'wantsContest': clean_val(r[off+9]) if len(r) > off+9 else '',
            'priority': clean_val(r[off+10]) if len(r) > off+10 else ''
        })

    # 7. Parse BP Candidates
    bp_candidates = []
    for idx, r in enumerate(sheets_data.get('Block Pramukh', [])[2:]):
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

    zp_audit = {
        'missingPhone': sum(1 for c in zp_candidates if not c['contact']),
        'missingGender': sum(1 for c in zp_candidates if not c['gender']),
        'missingCategory': sum(1 for c in zp_candidates if not c['category']),
        'missingAny': sum(1 for c in zp_candidates if not c['contact'] or not c['gender'] or not c['category']),
    }
    bp_audit = {
        'missingPhone': sum(1 for c in bp_candidates if not c['contact']),
        'missingGender': sum(1 for c in bp_candidates if not c['gender']),
        'missingCategory': sum(1 for c in bp_candidates if not c['category'] and not c['candidateCategory']),
        'missingAny': sum(1 for c in bp_candidates if not c['contact'] or not c['gender'] or (not c['category'] and not c['candidateCategory'])),
    }

    zones = sorted(list(set([d['zone'] for d in zp_districts if d['zone']])))
    now_iso = datetime.now(timezone.utc).isoformat()

    total_zp_seats = zp_snap_vals.get('totalSeats', 1160)
    zp_target = total_zp_seats * 5
    zp_identified = (
        zp_snap_vals.get('totalIdentified')
        or sum(z['identified'] for z in zp_progress_zones)
        or len(zp_candidates)
    )
    s1 = zp_snap_vals.get('seats1', sum(d['seatsWith1'] for d in zp_districts))
    s2 = zp_snap_vals.get('seats2', sum(d['seatsWith2'] for d in zp_districts))
    s3 = zp_snap_vals.get('seats3', sum(d['seatsWith3'] for d in zp_districts))
    s4 = zp_snap_vals.get('seats4', sum(d['seatsWith4'] for d in zp_districts))
    s5 = zp_snap_vals.get('seats5', sum(d['seatsWith5'] for d in zp_districts))

    total_bp_blocks = bp_snap_vals.get('totalBlocks', 534)
    bp_target = bp_snap_vals.get('target3x', total_bp_blocks * 3)
    bp_identified = sum(z['identified'] for z in bp_progress_zones) or len(bp_candidates)
    b0 = bp_snap_vals.get('blocks0', sum(d['blocksWith0'] for d in bp_districts))
    b1 = bp_snap_vals.get('blocks1', sum(d['blocksWith1'] for d in bp_districts))
    b2 = bp_snap_vals.get('blocks2', sum(d['blocksWith2'] for d in bp_districts))
    b3 = bp_snap_vals.get('blocks3', sum(d['blocksWith3'] for d in bp_districts))

    summary = {
        'meta': {
            'title': 'Bihar Panchayat Candidate Identification Dashboard 2026',
            'subtitle': 'Executive Tracking System: Zila Parishad & Block Pramukh',
            'reportDate': datetime.now().strftime('%d %B %Y'),
            'lastSynced': now_iso,
            'isLiveLinked': True,
            'sourceSpreadsheetId': SHEET_ID,
            'zonesCount': len(zones),
            'zonesList': zones
        },
        'snapshot': {
            'zp': {
                'title': 'Zila Parishad (ZP)',
                'totalSeats': total_zp_seats,
                'targetMultiplier': 5,
                'targetCandidates': zp_target,
                'totalIdentified': zp_identified,
                'remainingCandidates': max(0, zp_target - zp_identified),
                'overallCoveragePct': round(zp_identified / zp_target * 100, 1) if zp_target else 0,
                'seatsWithAtLeast1': s1,
                'seatsWith1Pct': round(s1 / total_zp_seats * 100, 1) if total_zp_seats else 0,
                'seatsWith2': s2,
                'seatsWith3': s3,
                'seatsWith4': s4,
                'seatsWith5Plus': s5,
                'gaps': {
                    'gap1': max(0, total_zp_seats - s1),
                    'gap2': max(0, total_zp_seats - s2),
                    'gap3': max(0, total_zp_seats - s3),
                    'gap4': max(0, total_zp_seats - s4),
                    'gap5': max(0, total_zp_seats - s5)
                },
                'demographics': zp_bifurcation_totals,
                'candidateRecordsCount': len(zp_candidates),
                'audit': zp_audit
            },
            'bp': {
                'title': 'Block Pramukh (BP)',
                'totalBlocks': total_bp_blocks,
                'targetMultiplier': 3,
                'targetCandidates': bp_target,
                'totalIdentified': bp_identified,
                'remainingBlocks': max(0, bp_target - bp_identified),
                'overallCoveragePct': round(bp_identified / bp_target * 100, 1) if bp_target else 0,
                'blocksWith0': b0,
                'blocksWithAtLeast1': b1,
                'blocksWith1Pct': round(b1 / total_bp_blocks * 100, 1) if total_bp_blocks else 0,
                'blocksWith2': b2,
                'blocksWith3': b3,
                'gaps': {
                    'gap1': max(0, total_bp_blocks - b1),
                    'gap2': max(0, total_bp_blocks - b2),
                    'gap3': max(0, total_bp_blocks - b3)
                },
                'demographics': bp_bifurcation_totals,
                'candidateRecordsCount': len(bp_candidates),
                'audit': bp_audit
            }
        },
        'zp': {
            'districtWise': zp_districts,
            'progressByZone': zp_progress_zones,
            'bifurcationTotals': zp_bifurcation_totals,
            'candidatesCount': len(zp_candidates)
        },
        'bp': {
            'districtWise': bp_districts,
            'progressByZone': bp_progress_zones,
            'bifurcationTotals': bp_bifurcation_totals,
            'candidatesCount': len(bp_candidates)
        }
    }

    if persist:
        _try_write_json('data/dashboard_summary.json', summary, indent=2)
        _try_write_json('data/zp_candidates.json', zp_candidates)
        _try_write_json('data/bp_candidates.json', bp_candidates)

    _cache['last_synced'] = now_iso
    _cache['summary'] = summary
    _cache['zp_candidates'] = zp_candidates
    _cache['bp_candidates'] = bp_candidates

    return summary, zp_candidates, bp_candidates

def sync_now(persist=True):
    print("Initiating Live Google Sheet Synchronization...")
    sheets_data = fetch_all_live_sheets()
    summary, zp_cands, bp_cands = process_live_data(sheets_data, persist=persist)
    print(f"Sync complete! Processed {len(zp_cands)} ZP candidates and {len(bp_cands)} BP candidates.")
    return {
        'status': 'success',
        'lastSynced': _cache['last_synced'],
        'zpCandidateCount': len(zp_cands),
        'bpCandidateCount': len(bp_cands),
        'summary': summary,
        'zpCandidates': zp_cands,
        'bpCandidates': bp_cands
    }

if __name__ == '__main__':
    res = sync_now(persist=True)
    print("Test run result:", res['status'], "at", res['lastSynced'])
