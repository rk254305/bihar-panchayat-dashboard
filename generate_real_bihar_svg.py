import json

with open('public/bihar_districts.geojson', encoding='utf-8') as f:
    geo = json.load(f)

with open('public/dashboard_summary.json', encoding='utf-8') as f:
    summary = json.load(f)

with open('public/zp_candidates.json', encoding='utf-8') as f:
    zp_cands = json.load(f)

with open('public/bp_candidates.json', encoding='utf-8') as f:
    bp_cands = json.load(f)

# Build district lookup from dashboard summary
zp_dist_map = {}
for d in summary['zp']['districtWise']:
    zp_dist_map[d['district']] = d

bp_dist_map = {}
for d in summary['bp']['districtWise']:
    bp_dist_map[d['district']] = d

# Map 38 geo districts to dashboard reporting units
geo_to_units = {
    'West Champaran': ['Bagaha', 'Bettiah'],
    'Patna': ['Patna Gramin', 'Patna Barh'],
    'Madhubani': ['Madhubani', 'Jhanjharpur'],
    'Bhagalpur': ['Bhagalpur', 'Naugachhiya'],
    'Samastipur': ['Samastipur', 'Rosera'],
    'Kaimur': ['Kaimur (Bhabhua)']
}

# 3-letter codes for map display & element IDs
district_codes = {
    'West Champaran': 'WCH', 'East Champaran': 'ECH', 'Sitamarhi': 'STM', 'Sheohar': 'SHR',
    'Gopalganj': 'GPG', 'Siwan': 'SWN', 'Saran': 'SRN', 'Muzaffarpur': 'MZP',
    'Vaishali': 'VSH', 'Darbhanga': 'DBG', 'Madhubani': 'MDB', 'Samastipur': 'SMS',
    'Begusarai': 'BGS', 'Supaul': 'SPL', 'Saharsa': 'SHS', 'Madhepura': 'MDP',
    'Khagaria': 'KHG', 'Araria': 'ARR', 'Kishanganj': 'KSG', 'Purnia': 'PRN',
    'Katihar': 'KTH', 'Buxar': 'BXR', 'Bhojpur': 'BHJ', 'Patna': 'PAT',
    'Nalanda': 'NAL', 'Lakhisarai': 'LKH', 'Sheikhpura': 'SHK', 'Munger': 'MNG',
    'Bhagalpur': 'BGL', 'Kaimur': 'KMR', 'Rohtas': 'RHT', 'Arwal': 'ARW',
    'Jehanabad': 'JHN', 'Aurangabad': 'AUR', 'Gaya': 'GAY', 'Nawada': 'NWD',
    'Jamui': 'JMU', 'Banka': 'BNK'
}

# Calculate female and minority candidates per district from raw records
district_females_zp = {}
district_minority_zp = {}
for c in zp_cands:
    dist = c.get('district', '')
    if c.get('gender', '').lower() in ['female', 'f', 'mahila']:
        district_females_zp[dist] = district_females_zp.get(dist, 0) + 1
    if c.get('category', '').lower() == 'minority' or 'minority' in c.get('candidateCategory', '').lower():
        district_minority_zp[dist] = district_minority_zp.get(dist, 0) + 1

district_females_bp = {}
district_minority_bp = {}
for c in bp_cands:
    dist = c.get('district', '')
    if c.get('gender', '').lower() in ['female', 'f', 'mahila'] or 'mahila' in c.get('candidateCategory', '').lower():
        district_females_bp[dist] = district_females_bp.get(dist, 0) + 1
    if 'minority' in c.get('candidateCategory', '').lower() or 'minority' in c.get('category', '').lower():
        district_minority_bp[dist] = district_minority_bp.get(dist, 0) + 1

# Bounding box & Projection
min_lng, max_lng = 83.320238, 88.299546
min_lat, max_lat = 24.286327, 27.521347

width = 720
height = 440
padding = 20

def project(lng, lat):
    x = padding + (lng - min_lng) / (max_lng - min_lng) * (width - 2 * padding)
    y = height - padding - (lat - min_lat) / (max_lat - min_lat) * (height - 2 * padding)
    return round(x, 1), round(y, 1)

svg_paths = []
district_info_json = {}

for feat in geo['features']:
    name = feat['properties']['district']
    geom = feat['geometry']
    coords = geom['coordinates']
    
    # SVG path string
    d_parts = []
    polys = [coords] if geom['type'] == 'Polygon' else coords
    all_pts = []
    for poly in polys:
        ring = poly[0]
        pts = [project(pt[0], pt[1]) for pt in ring]
        all_pts.extend(pts)
        path_str = 'M ' + ' L '.join(f'{p[0]},{p[1]}' for p in pts) + ' Z'
        d_parts.append(path_str)
    full_d = ' '.join(d_parts)
    
    # Calculate centroid
    cx = round(sum(p[0] for p in all_pts) / len(all_pts), 1)
    cy = round(sum(p[1] for p in all_pts) / len(all_pts), 1)
    
    # Centroid manual adjustments for small or irregular districts to optimize text placement
    if name == 'Sheohar':
        cx -= 5; cy -= 4
    elif name == 'Patna':
        cx += 12; cy -= 4
    elif name == 'Lakhisarai':
        cy += 4
    elif name == 'Sheikhpura':
        cx -= 3
    elif name == 'Gopalganj':
        cy -= 2
    elif name == 'Bhojpur':
        cy -= 2
    elif name == 'Kaimur':
        cy -= 5
    elif name == 'Jamui':
        cy -= 5
    
    # Aggregate data
    reporting_units = geo_to_units.get(name, [name])
    seats_zp = 0
    identified_zp = 0
    gap1_zp = 0
    zone_zp = 'Unknown'
    blocks_bp = 0
    identified_bp = 0
    females_zp = 0
    minority_zp = 0
    females_bp = 0
    minority_bp = 0
    
    for u in reporting_units:
        if u in zp_dist_map:
            zd = zp_dist_map[u]
            seats_zp += zd.get('seats', 0)
            identified_zp += zd.get('totalIdentified', 0)
            gap1_zp += zd.get('gap1', 0)
            zone_zp = zd.get('zone', zone_zp)
        if u in bp_dist_map:
            bd = bp_dist_map[u]
            blocks_bp += bd.get('blocks', 0)
            identified_bp += bd.get('totalIdentified', 0)
        females_zp += district_females_zp.get(u, 0)
        minority_zp += district_minority_zp.get(u, 0)
        females_bp += district_females_bp.get(u, 0)
        minority_bp += district_minority_bp.get(u, 0)
        
    target5x_zp = seats_zp * 5
    pct_zp = round((identified_zp / target5x_zp * 100), 1) if target5x_zp > 0 else 0
    target3x_bp = blocks_bp * 3
    pct_bp = round((identified_bp / target3x_bp * 100), 1) if target3x_bp > 0 else 0
    
    code = district_codes.get(name, name[:3].upper())
    
    district_info_json[name] = {
        'district': name,
        'code': code,
        'zone': zone_zp,
        'units': reporting_units,
        'seatsZp': seats_zp,
        'identifiedZp': identified_zp,
        'target5xZp': target5x_zp,
        'pctZp': pct_zp,
        'gap1Zp': gap1_zp,
        'blocksBp': blocks_bp,
        'identifiedBp': identified_bp,
        'target3xBp': target3x_bp,
        'pctBp': pct_bp,
        'femalesZp': females_zp,
        'minorityZp': minority_zp,
        'femalesBp': females_bp,
        'minorityBp': minority_bp
    }
    
    # Label formatting with full name
    if name == 'West Champaran':
        label_html = f'<text x="{cx}" y="{cy - 4}" class="bihar-geo-label pointer-events-none" text-anchor="middle" font-size="8"><tspan x="{cx}" dy="0">West</tspan><tspan x="{cx}" dy="8.5">Champaran</tspan></text>'
    elif name == 'East Champaran':
        label_html = f'<text x="{cx}" y="{cy - 4}" class="bihar-geo-label pointer-events-none" text-anchor="middle" font-size="8"><tspan x="{cx}" dy="0">East</tspan><tspan x="{cx}" dy="8.5">Champaran</tspan></text>'
    else:
        # Scale font size based on district size
        if name in ['Sheohar', 'Arwal', 'Sheikhpura', 'Lakhisarai', 'Jehanabad']:
            fsize = '6.5'
        elif name in ['Khagaria', 'Munger', 'Saharsa', 'Madhepura', 'Buxar', 'Vaishali']:
            fsize = '7'
        else:
            fsize = '8'
        label_html = f'<text x="{cx}" y="{cy + 2.5}" class="bihar-geo-label pointer-events-none" text-anchor="middle" font-size="{fsize}">{name}</text>'
    
    # SVG element
    svg_paths.append(f'''    <g class="bihar-district-group cursor-pointer" data-district="{name}" onclick="selectDistrictGeo('{name}')" onmouseenter="hoverDistrictGeo(event, '{name}')" onmouseleave="leaveDistrictGeo()">
      <path d="{full_d}" id="geo-district-{code.lower()}" class="bihar-district-boundary" data-district="{name}" fill="var(--surface-subtle)" stroke="var(--hairline)" stroke-width="1.2" />
      {label_html}
    </g>''')

# Write district data to public/bihar_district_map_data.json
with open('public/bihar_district_map_data.json', 'w', encoding='utf-8') as f:
    json.dump(district_info_json, f, indent=2)

print("Generated public/bihar_district_map_data.json with all 38 districts.")

# Generate real SVG snippet
svg_output = [
  '<!-- Real Geographic Boundary SVG Map of Bihar -->',
  '<svg viewBox="0 0 720 440" class="w-full h-auto select-none" id="bihar-real-svg-map" xmlns="http://www.w3.org/2000/svg">',
  '  <defs>',
  '    <pattern id="gapHatch" width="6" height="6" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">',
  '      <line x1="0" y1="0" x2="0" y2="6" stroke="var(--color-alert)" stroke-width="1.8" opacity="0.4" />',
  '    </pattern>',
  '  </defs>',
  '  <!-- Orientation and River -->',
  '  <text x="30" y="24" fill="var(--ink-faint)" font-size="9" font-family="var(--font-mono)">↑ NORTH (NEPAL)</text>',
  '  <text x="600" y="24" fill="var(--ink-faint)" font-size="9" font-family="var(--font-mono)">EAST (BENGAL) →</text>',
  '  <!-- Ganges River Accurate Vector Path Crossing Bihar -->',
  '  <path d="M 99,258 Q 181,248 249,251 T 318,264 T 386,280 T 454,285 T 522,301 T 605,292" fill="none" stroke="var(--hairline)" stroke-width="2.2" stroke-dasharray="4,4" opacity="0.8" />',
  '  <text x="535" y="295" fill="var(--ink-faint)" font-size="7.5" font-family="var(--font-sans)" font-style="italic">Ganga River ~</text>'
]
svg_output.extend(svg_paths)
svg_output.append('</svg>')

with open('bihar_real_svg_snippet.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg_output))

print("Generated bihar_real_svg_snippet.html successfully with full district names!")
