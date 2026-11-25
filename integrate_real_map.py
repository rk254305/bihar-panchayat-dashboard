import json, re

# Read the generated real SVG snippet
with open('bihar_real_svg_snippet.html', 'r', encoding='utf-8') as f:
    real_svg = f.read()

# ==============================================================================
# 1. UPDATE style.css WITH REAL MAP STYLES
# ==============================================================================
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

map_css_addition = '''
/* Real Geographic Boundary Map */
.bihar-district-boundary {
  stroke: var(--hairline);
  stroke-width: 1.2;
  cursor: pointer;
  transition: all 0.15s ease;
}

.bihar-district-boundary:hover,
.bihar-district-boundary.active-selected {
  stroke: var(--ink-text) !important;
  stroke-width: 2.2 !important;
  filter: brightness(0.92);
}

body.theme-dark .bihar-district-boundary:hover,
body.theme-dark .bihar-district-boundary.active-selected {
  stroke: #E8E3D8 !important;
  stroke-width: 2.2 !important;
  filter: brightness(1.15);
}

.bihar-geo-label {
  pointer-events: none;
  font-family: var(--font-mono);
  font-size: 8px;
  font-weight: 700;
  fill: var(--ink-text);
}

body.theme-dark .bihar-geo-label {
  fill: #8E9AA8;
}

.district-inspector-card {
  background-color: var(--surface-card);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-md);
  padding: 0.875rem;
}
'''

if '.bihar-district-boundary' not in css:
    css += map_css_addition
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("style.css updated with real geographic map styles.")

# ==============================================================================
# 2. UPDATE index.html WITH MAP + LIVE DISTRICT INSPECTOR
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build the complete new Map Section
new_map_section = f'''            <!-- SECTION A: BIHAR GEOGRAPHIC DISTRICT MAP & LIVE DISTRICT INSPECTOR -->
            <div class="editorial-card p-4 space-y-3">
              <div class="flex items-center justify-between flex-wrap gap-2 pb-2 hairline-b">
                <div>
                  <h4 class="text-sm font-bold text-[var(--ink-text)] flex items-center gap-2">
                    <span>Bihar Geographic District Map</span>
                    <span class="font-mono text-[10px] font-semibold text-[var(--ink-muted)]">38 Geographic Districts • 43 Units</span>
                  </h4>
                  <p class="text-xs text-[var(--ink-muted)] font-mono">Real district boundaries • Click any district to inspect dossiers</p>
                </div>

                <!-- Map Overlay Metrics & View Switcher -->
                <div class="flex items-center flex-wrap gap-2 text-xs">
                  <!-- Mode Switcher -->
                  <div class="pill-filter-group text-xs">
                    <button id="map-mode-zp" onclick="setGeoMapMetric('zp')" class="pill-filter-btn pill-filter-btn-active">
                      ZP Progress
                    </button>
                    <button id="map-mode-bp" onclick="setGeoMapMetric('bp')" class="pill-filter-btn">
                      BP Progress
                    </button>
                    <button id="map-mode-females" onclick="setGeoMapMetric('females')" class="pill-filter-btn">
                      Females
                    </button>
                    <button id="map-mode-gap" onclick="setGeoMapMetric('gap')" class="pill-filter-btn text-[var(--color-alert)]">
                      GAP 1 Alerts
                    </button>
                  </div>

                  <!-- View Switcher -->
                  <div class="pill-filter-group text-xs">
                    <button id="btn-view-map" onclick="switchMapDisplay('map')" class="pill-filter-btn pill-filter-btn-active">
                      🗺️ Map
                    </button>
                    <button id="btn-view-table" onclick="switchMapDisplay('table')" class="pill-filter-btn">
                      📋 Table
                    </button>
                  </div>
                </div>
              </div>

              <!-- 1. MAP VIEW CONTAINER (GIS Map + Live District Inspector) -->
              <div id="bihar-map-wrapper">
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-3.5">

                  <!-- Left 7 Cols: Real SVG Map Canvas -->
                  <div class="lg:col-span-7 bihar-map-container p-2 border border-[var(--hairline)] rounded-[6px] relative select-none flex flex-col justify-between">
                    <!-- Floating Map Tooltip -->
                    <div id="bihar-map-tooltip" class="map-tooltip"></div>

                    <!-- SVG Canvas -->
{real_svg}

                    <!-- Dynamic Map Legend Footer -->
                    <div class="flex items-center justify-between flex-wrap gap-2 pt-2 px-1 border-t border-[var(--hairline)] text-[10px] text-[var(--ink-muted)] font-mono">
                      <div id="geo-map-legend" class="flex items-center gap-2.5">
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp-subtle)] border border-[var(--color-zp)]"></span> On Target (≥60%)</span>
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--surface-subtle)] border border-[var(--hairline)]"></span> In Progress</span>
                        <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-alert-subtle)] border border-[var(--color-alert)]"></span> <strong class="text-[var(--color-alert)]">● GAP 1 (Zero Seats)</strong></span>
                      </div>
                      <span class="text-[var(--ink-faint)]">Click district to lock inspection</span>
                    </div>
                  </div>

                  <!-- Right 5 Cols: Live District Inspector & Action Dossier -->
                  <div class="lg:col-span-5 district-inspector-card flex flex-col justify-between space-y-3" id="district-inspector-panel">
                    <div>
                      <!-- Inspector Header -->
                      <div class="flex items-start justify-between pb-2 hairline-b">
                        <div>
                          <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-[var(--color-zp)]" id="inspect-indicator"></span>
                            <h4 class="font-mono text-base font-bold text-[var(--ink-text)]" id="inspect-district-name">Purnia</h4>
                          </div>
                          <span class="font-mono text-xs text-[var(--ink-muted)]" id="inspect-zone-name">Seemanchal Zone</span>
                        </div>
                        <span class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-[4px] bg-[var(--color-alert-subtle)] text-[var(--color-alert)] border border-[var(--color-alert)]" id="inspect-status-badge">
                          🚨 GAP 1 (12 Seats)
                        </span>
                      </div>

                      <!-- Sub-Reporting Units Note (for merged districts like Bagaha/Bettiah or Patna Gramin/Barh) -->
                      <div id="inspect-units-note" class="text-[10px] font-mono text-[var(--ink-faint)] pt-1.5 pb-0.5">
                        Reporting Unit: Purnia (34 seats)
                      </div>

                      <!-- Track 1: Zila Parishad Metrics -->
                      <div class="p-2.5 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)] space-y-1.5 mt-2">
                        <div class="flex items-center justify-between text-[11px] font-mono font-bold text-[var(--color-zp)]">
                          <span>Zila Parishad (ZP)</span>
                          <span id="inspect-zp-pct">20.6% Covered</span>
                        </div>
                        <div class="grid grid-cols-3 gap-2 text-xs font-mono">
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

                      <!-- Track 2: Block Pramukh Metrics -->
                      <div class="p-2.5 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)] space-y-1.5 mt-2">
                        <div class="flex items-center justify-between text-[11px] font-mono font-bold text-[var(--color-bp)]">
                          <span>Block Pramukh (BP)</span>
                          <span id="inspect-bp-pct">33.3% Covered</span>
                        </div>
                        <div class="grid grid-cols-2 gap-2 text-xs font-mono">
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

                      <!-- Demographics in this District -->
                      <div class="grid grid-cols-2 gap-2 mt-2 pt-2 hairline-t text-xs font-mono">
                        <div class="p-2 rounded-[4px] border border-[var(--hairline)]">
                          <span class="text-[10px] text-[var(--ink-muted)] block">Females (महिलाएं)</span>
                          <div class="flex items-baseline gap-2 mt-0.5">
                            <span class="text-xs">ZP: <strong class="text-[var(--color-zp)]" id="inspect-zp-fem">4</strong></span>
                            <span class="text-xs">BP: <strong class="text-[var(--color-bp)]" id="inspect-bp-fem">1</strong></span>
                          </div>
                        </div>
                        <div class="p-2 rounded-[4px] border border-[var(--hairline)]">
                          <span class="text-[10px] text-[var(--ink-muted)] block">Minority (अल्पसंख्यक)</span>
                          <div class="flex items-baseline gap-2 mt-0.5">
                            <span class="text-xs">ZP: <strong class="text-[var(--color-zp)]" id="inspect-zp-min">11</strong></span>
                            <span class="text-xs">BP: <strong class="text-[var(--color-bp)]" id="inspect-bp-min">0</strong></span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Direct District Actions -->
                    <div class="space-y-1.5 pt-2 hairline-t">
                      <button id="inspect-btn-zp-filter" onclick="inspectDistrictFilter('zp')" class="editorial-btn w-full justify-between text-xs text-[var(--color-zp)] border-[var(--color-zp)]">
                        <span>View ZP Candidates in <span id="inspect-btn-dist-label">Purnia</span></span>
                        <span class="font-mono">→</span>
                      </button>
                      <button id="inspect-btn-bp-filter" onclick="inspectDistrictFilter('bp')" class="editorial-btn w-full justify-between text-xs text-[var(--color-bp)] border-[var(--color-bp)]">
                        <span>View BP Pramukhs in <span id="inspect-btn-dist-label-bp">Purnia</span></span>
                        <span class="font-mono">→</span>
                      </button>
                    </div>

                  </div>

                </div>
              </div>

              <!-- 2. TABLE VIEW CONTAINER (Preserves hero-key-districts-body for seamless integrity) -->
              <div id="bihar-table-view" class="hidden overflow-x-auto">
                <table class="editorial-table">
                  <thead>
                    <tr>
                      <th>District</th>
                      <th class="text-center">ZP Seats (5x Target)</th>
                      <th class="text-right">Status</th>
                    </tr>
                  </thead>
                  <tbody id="hero-key-districts-body" class="text-xs font-mono">
                    <!-- Populated dynamically by app.js -->
                  </tbody>
                </table>
                <div class="pt-2 text-right">
                  <button onclick="switchMainTab('zp'); switchZpTab('zp-district-wise')"
                    class="editorial-btn text-xs">
                    View All 43 Districts Detailed Report →
                  </button>
                </div>
              </div>
            </div>'''

# Replace Section A in index.html
html = re.sub(r'<!-- SECTION A: BIHAR DISTRICT COVERAGE MAP.*?<!-- SECTION B: PENETRATION DEPTH', new_map_section + '\n\n            <!-- SECTION B: PENETRATION DEPTH', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html updated with GIS map and Live District Inspector.")
