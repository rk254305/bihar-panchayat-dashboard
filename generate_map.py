import json

districts_geo = [
  # Champaran
  ('Bagaha', 'Champaran', 60, 25, 62, 42, 'BGH'),
  ('Bettiah', 'Champaran', 125, 45, 62, 42, 'BTH'),
  ('East Champaran', 'Champaran', 190, 35, 76, 45, 'ECH'),
  
  # Tirhut
  ('Sheohar', 'Tirhut', 255, 45, 48, 35, 'SHR'),
  ('Sitamarhi', 'Tirhut', 295, 30, 68, 42, 'STM'),
  ('Muzaffarpur', 'Tirhut', 265, 88, 76, 46, 'MZP'),
  
  # Saran
  ('Gopalganj', 'Saran', 120, 95, 66, 42, 'GPG'),
  ('Siwan', 'Saran', 115, 142, 66, 42, 'SWN'),
  ('Saran', 'Saran', 185, 138, 72, 42, 'SRN'),
  
  # Mithilanchal
  ('Madhubani', 'Mithilanchal', 368, 28, 72, 42, 'MDB'),
  ('Jhanjharpur', 'Mithilanchal', 432, 42, 66, 42, 'JJR'),
  ('Darbhanga', 'Mithilanchal', 348, 78, 76, 45, 'DBG'),
  
  # Samastipur
  ('Vaishali', 'Samastipur', 258, 140, 68, 42, 'VSH'),
  ('Samastipur', 'Samastipur', 330, 130, 72, 42, 'SMS'),
  ('Rosera', 'Samastipur', 404, 130, 58, 42, 'RSR'),
  ('Begusarai', 'Samastipur', 448, 168, 72, 42, 'BGS'),
  
  # Koshi
  ('Supaul', 'Koshi', 502, 38, 66, 42, 'SPL'),
  ('Saharsa', 'Koshi', 488, 90, 66, 42, 'SHS'),
  ('Madhepura', 'Koshi', 548, 90, 66, 42, 'MDP'),
  ('Khagaria', 'Koshi', 525, 148, 66, 42, 'KHG'),
  
  # Seemanchal
  ('Araria', 'Seemanchal', 605, 42, 68, 42, 'ARR'),
  ('Kishanganj', 'Seemanchal', 670, 52, 62, 42, 'KSG'),
  ('Purnia', 'Seemanchal', 618, 98, 72, 45, 'PRN'),
  ('Katihar', 'Seemanchal', 668, 148, 68, 48, 'KTH'),
  
  # Patna
  ('Patna Gramin', 'Patna', 255, 195, 78, 44, 'PAT-G'),
  ('Patna Barh', 'Patna', 336, 188, 68, 44, 'PAT-B'),
  
  # Sahabad
  ('Buxar', 'Sahabad', 80, 200, 66, 44, 'BXR'),
  ('Bhojpur', 'Sahabad', 152, 192, 72, 44, 'BHJ'),
  ('Kaimur (Bhabhua)', 'Sahabad', 65, 255, 78, 52, 'KMR'),
  ('Rohtas', 'Sahabad', 138, 250, 76, 52, 'RHT'),
  
  # Magadh
  ('Arwal', 'Magadh', 212, 248, 56, 38, 'ARW'),
  ('Jehanabad', 'Magadh', 268, 248, 58, 38, 'JHN'),
  ('Aurangabad', 'Magadh', 178, 310, 76, 48, 'AUR'),
  ('Gaya', 'Magadh', 255, 305, 82, 54, 'GAY'),
  
  # Nalanda
  ('Nalanda', 'Nalanda', 328, 242, 68, 44, 'NAL'),
  ('Nawada', 'Nalanda', 338, 298, 68, 48, 'NWD'),
  ('Sheikhpura', 'Nalanda', 395, 242, 58, 38, 'SHK'),
  ('Lakhisarai', 'Nalanda', 445, 222, 62, 42, 'LKH'),
  
  # Munger
  ('Munger', 'Munger', 505, 205, 66, 42, 'MNG'),
  ('Naugachhiya', 'Munger', 578, 198, 66, 40, 'NGC'),
  ('Bhagalpur', 'Munger', 575, 248, 76, 46, 'BGL'),
  ('Jamui', 'Munger', 478, 268, 76, 52, 'JMU'),
  ('Banka', 'Munger', 558, 302, 76, 52, 'BNK')
]

with open('public/dashboard_summary.json', 'r', encoding='utf-8') as f:
  summary = json.load(f)
district_data = {d['district']: d for d in summary['zp']['districtWise']}

svg = [
  '<!-- Bihar 43 Reporting Units Choropleth Map -->',
  '<div class="bihar-map-container p-3 border border-[var(--hairline)] rounded-[6px] relative select-none">',
  '  <!-- Floating Map Tooltip -->',
  '  <div id="bihar-map-tooltip" class="map-tooltip"></div>',
  '  ',
  '  <!-- SVG Canvas -->',
  '  <svg viewBox="0 0 760 375" class="w-full h-auto" xmlns="http://www.w3.org/2000/svg">',
  '    <!-- North Indicator & Ganga River Guide -->',
  '    <text x="75" y="15" fill="var(--ink-faint)" font-size="9" font-family="var(--font-mono)" letter-spacing="0.05em">↑ NORTH (NEPAL BORDER)</text>',
  '    <text x="610" y="15" fill="var(--ink-faint)" font-size="9" font-family="var(--font-mono)">EAST (BENGAL) →</text>',
  '    ',
  '    <!-- Ganges River Path (Splitting North and South Bihar) -->',
  '    <path d="M 40,215 Q 160,185 245,182 T 435,185 T 570,225 T 750,215" fill="none" stroke="var(--hairline)" stroke-width="2.5" stroke-dasharray="5,4" opacity="0.8"/>',
  '    <text x="630" y="212" fill="var(--ink-faint)" font-size="8" font-family="var(--font-sans)" font-style="italic">Ganga River ~</text>'
]

for name, zone, x, y, w, h, code in districts_geo:
  d = district_data.get(name, {})
  gap1 = d.get('gap1', 0)
  total_id = d.get('totalIdentified', 0)
  seats = d.get('seats', 0)
  target5x = seats * 5
  pct = round((total_id / target5x * 100), 1) if target5x > 0 else 0
  
  # Status colors according to Mithila Ink Palette rules:
  # Red only for gaps/problems; ZP is always Indigo; BP is Turmeric
  if gap1 > 0:
    fill_color = "var(--color-alert-subtle)"
    stroke_color = "var(--color-alert)"
    badge_fill = "var(--color-alert)"
    stat_text = f"Gap {gap1}"
    stat_class = "fill-[var(--color-alert)] font-bold"
  elif pct >= 65:
    fill_color = "var(--color-zp-subtle)"
    stroke_color = "var(--color-zp)"
    badge_fill = "var(--color-zp)"
    stat_text = f"{pct}%"
    stat_class = "fill-[var(--color-zp)] font-semibold"
  else:
    fill_color = "var(--surface-subtle)"
    stroke_color = "var(--hairline)"
    badge_fill = "var(--ink-muted)"
    stat_text = f"{total_id}/{seats}"
    stat_class = "fill-[var(--ink-muted)]"
    
  node = f'''    <g class="bihar-map-node cursor-pointer" data-district="{name}" data-zone="{zone}" data-seats="{seats}" data-identified="{total_id}" data-gap1="{gap1}" data-target="{target5x}" data-pct="{pct}%" onclick="onDistrictMapClick('{name}')" onmouseenter="onDistrictMapHover(event, '{name}')" onmouseleave="onDistrictMapLeave()">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" class="bihar-district-path" fill="{fill_color}" stroke="{stroke_color}" stroke-width="1.2"/>
      <circle cx="{x + 8}" cy="{y + 9}" r="3" fill="{badge_fill}"/>
      <text x="{x + w/2 + 2}" y="{y + 14}" class="font-mono text-[9px] font-bold" text-anchor="middle" fill="var(--ink-text)">{code}</text>
      <text x="{x + w/2}" y="{y + h - 8}" class="font-mono text-[8px] {stat_class}" text-anchor="middle">{stat_text}</text>
    </g>'''
  svg.append(node)

svg.append('  </svg>')
svg.append('  <!-- Map Legend Footer -->')
svg.append('  <div class="flex items-center justify-between flex-wrap gap-2 pt-2 px-2 border-t border-[var(--hairline)] text-[10px] text-[var(--ink-muted)]">')
svg.append('    <div class="flex items-center gap-3">')
svg.append('      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp-subtle)] border border-[var(--color-zp)]"></span> On Target (≥65%)</span>')
svg.append('      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--surface-subtle)] border border-[var(--hairline)]"></span> Moderate Coverage</span>')
svg.append('      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-alert-subtle)] border border-[var(--color-alert)]"></span> <strong class="text-[var(--color-alert)]">● GAP 1 (Zero-Candidate Seats)</strong></span>')
svg.append('    </div>')
svg.append('    <span class="font-mono text-[10px] text-[var(--ink-faint)]">Click any district to inspect</span>')
svg.append('  </div>')
svg.append('</div>')

with open('bihar_map_snippet.html', 'w', encoding='utf-8') as f:
  f.write('\n'.join(svg))

print("bihar_map_snippet.html generated successfully!")
