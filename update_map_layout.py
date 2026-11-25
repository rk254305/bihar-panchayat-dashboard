import json

with open('index.html', encoding='utf-8') as f:
    html = f.read()

with open('bihar_real_svg_snippet.html', encoding='utf-8') as f:
    svg_snippet = f.read()

start_marker = '<!-- 1. MAP VIEW CONTAINER (GIS Map + Live District Inspector) -->'
end_marker = '<!-- 2. TABLE VIEW CONTAINER (Preserves hero-key-districts-body for seamless integrity) -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Error finding markers: start_idx={start_idx}, end_idx={end_idx}")
    exit(1)

new_content = f'''<!-- 1. MAP VIEW CONTAINER (GIS Map + Live District Inspector) -->
              <div id="bihar-map-wrapper" class="space-y-3.5">

                <!-- Geographic SVG Map Canvas (Full Width) -->
                <div class="w-full bihar-map-container p-3 border border-[var(--hairline)] rounded-[6px] relative select-none flex flex-col justify-between">
                  <!-- Floating Map Tooltip -->
                  <div id="bihar-map-tooltip" class="map-tooltip"></div>

                  <!-- SVG Canvas (Full Width & Clean Aspect Ratio) -->
{svg_snippet}

                  <!-- Dynamic Map Legend Footer -->
                  <div class="flex items-center justify-between flex-wrap gap-2 pt-2.5 px-1 border-t border-[var(--hairline)] text-[11px] text-[var(--ink-muted)] font-mono mt-2">
                    <div id="geo-map-legend" class="flex items-center gap-3">
                      <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp-subtle)] border border-[var(--color-zp)]"></span> On Target (≥60%)</span>
                      <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--surface-subtle)] border border-[var(--hairline)]"></span> In Progress</span>
                      <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-alert-subtle)] border border-[var(--color-alert)]"></span> <strong class="text-[var(--color-alert)]">● GAP 1 (Zero Seats)</strong></span>
                    </div>
                    <span class="text-[var(--ink-faint)]">Click any district to lock / view detailed dossier below</span>
                  </div>
                </div>

                <!-- Bottom: Live District Inspector & Action Dossier (Full Width Multi-Column) -->
                <div class="w-full district-inspector-card p-3.5 border border-[var(--hairline)] rounded-[6px] bg-[var(--surface-card)]" id="district-inspector-panel">
                  <div class="grid grid-cols-1 md:grid-cols-12 gap-3.5 items-stretch">

                    <!-- Col 1: District Identity & Quick Action Buttons (md:col-span-4) -->
                    <div class="md:col-span-4 flex flex-col justify-between p-2.5 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)]">
                      <div>
                        <!-- Inspector Header -->
                        <div class="flex items-center justify-between pb-1.5 hairline-b">
                          <div class="flex items-center gap-2">
                            <span class="w-2.5 h-2.5 rounded-full bg-[var(--color-zp)]" id="inspect-indicator"></span>
                            <h4 class="font-mono text-base font-bold text-[var(--ink-text)]" id="inspect-district-name">Purnia</h4>
                          </div>
                          <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-[4px] bg-[var(--color-alert-subtle)] text-[var(--color-alert)] border border-[var(--color-alert)]" id="inspect-status-badge">
                            🚨 GAP 1 (12 Seats)
                          </span>
                        </div>
                        <div class="flex items-center justify-between pt-1">
                          <span class="font-mono text-xs text-[var(--ink-muted)]" id="inspect-zone-name">Seemanchal Zone</span>
                          <span id="inspect-units-note" class="text-[10px] font-mono text-[var(--ink-faint)]">Reporting Unit: Purnia (34 seats)</span>
                        </div>
                      </div>

                      <!-- Direct District Actions -->
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 pt-2 mt-2 hairline-t">
                        <button id="inspect-btn-zp-filter" onclick="inspectDistrictFilter('zp')" class="editorial-btn justify-between text-xs text-[var(--color-zp)] border-[var(--color-zp)]">
                          <span>ZP Candidates in <span id="inspect-btn-dist-label">Purnia</span></span>
                          <span class="font-mono font-bold">→</span>
                        </button>
                        <button id="inspect-btn-bp-filter" onclick="inspectDistrictFilter('bp')" class="editorial-btn justify-between text-xs text-[var(--color-bp)] border-[var(--color-bp)]">
                          <span>BP Pramukhs in <span id="inspect-btn-dist-label-bp">Purnia</span></span>
                          <span class="font-mono font-bold">→</span>
                        </button>
                      </div>
                    </div>

                    <!-- Col 2: Track 1 - Zila Parishad Metrics (md:col-span-3) -->
                    <div class="md:col-span-3 p-2.5 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)] flex flex-col justify-between">
                      <div class="flex items-center justify-between text-[11px] font-mono font-bold text-[var(--color-zp)] pb-1 hairline-b">
                        <span class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-[var(--color-zp)]"></span> Zila Parishad (ZP)</span>
                        <span id="inspect-zp-pct">20.6% Covered</span>
                      </div>
                      <div class="grid grid-cols-3 gap-2 text-xs font-mono pt-1.5">
                        <div>
                          <span class="text-[9px] text-[var(--ink-muted)] uppercase block">Identified</span>
                          <strong class="text-[var(--ink-text)] text-sm" id="inspect-zp-identified">35</strong>
                          <span class="text-[9px] text-[var(--ink-faint)] block">of <span id="inspect-zp-target">170</span> goal</span>
                        </div>
                        <div>
                          <span class="text-[9px] text-[var(--ink-muted)] uppercase block">Seats</span>
                          <strong class="text-[var(--ink-text)] text-sm" id="inspect-zp-seats">34</strong>
                          <span class="text-[9px] text-[var(--ink-faint)] block">Total Seats</span>
                        </div>
                        <div>
                          <span class="text-[9px] text-[var(--color-alert)] uppercase font-bold block">Zero-Seats</span>
                          <strong class="text-[var(--color-alert)] text-sm" id="inspect-zp-gap1">12</strong>
                          <span class="text-[9px] text-[var(--color-alert)] block">GAP 1</span>
                        </div>
                      </div>
                    </div>

                    <!-- Col 3: Track 2 - Block Pramukh Metrics (md:col-span-3) -->
                    <div class="md:col-span-3 p-2.5 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)] flex flex-col justify-between">
                      <div class="flex items-center justify-between text-[11px] font-mono font-bold text-[var(--color-bp)] pb-1 hairline-b">
                        <span class="flex items-center gap-1.5"><span class="w-1.5 h-1.5 rounded-full bg-[var(--color-bp)]"></span> Block Pramukh (BP)</span>
                        <span id="inspect-bp-pct">33.3% Covered</span>
                      </div>
                      <div class="grid grid-cols-2 gap-2 text-xs font-mono pt-1.5">
                        <div>
                          <span class="text-[9px] text-[var(--ink-muted)] uppercase block">Pramukhs Identified</span>
                          <strong class="text-[var(--ink-text)] text-sm" id="inspect-bp-identified">14</strong>
                          <span class="text-[9px] text-[var(--ink-faint)] block">of <span id="inspect-bp-target">42</span> goal</span>
                        </div>
                        <div>
                          <span class="text-[9px] text-[var(--ink-muted)] uppercase block">Active Blocks</span>
                          <strong class="text-[var(--ink-text)] text-sm" id="inspect-bp-blocks">14</strong>
                          <span class="text-[9px] text-[var(--color-positive)] block">100% active</span>
                        </div>
                      </div>
                    </div>

                    <!-- Col 4: Track 3 - Inclusion Demographics (md:col-span-2) -->
                    <div class="md:col-span-2 p-2.5 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)] flex flex-col justify-between">
                      <div class="text-[11px] font-mono font-bold text-[var(--ink-muted)] uppercase tracking-wider pb-1 hairline-b">
                        Inclusion
                      </div>
                      <div class="space-y-1.5 pt-1 text-xs font-mono">
                        <div>
                          <span class="text-[10px] text-[var(--ink-muted)] block">Females:</span>
                          <div class="flex items-baseline gap-2">
                            <span class="text-xs">ZP: <strong class="text-[var(--color-zp)]" id="inspect-zp-fem">4</strong></span>
                            <span class="text-xs">BP: <strong class="text-[var(--color-bp)]" id="inspect-bp-fem">1</strong></span>
                          </div>
                        </div>
                        <div>
                          <span class="text-[10px] text-[var(--ink-muted)] block">Minority:</span>
                          <div class="flex items-baseline gap-2">
                            <span class="text-xs">ZP: <strong class="text-[var(--color-zp)]" id="inspect-zp-min">11</strong></span>
                            <span class="text-xs">BP: <strong class="text-[var(--color-bp)]" id="inspect-bp-min">0</strong></span>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                </div>

              </div>

              '''

updated_html = html[:start_idx] + new_content + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("SUCCESS: index.html updated with full-width map at top and inspector card at bottom!")
