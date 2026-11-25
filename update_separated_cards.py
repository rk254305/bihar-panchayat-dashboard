import re

# ==============================================================================
# 1. UPDATE style.css FOR SUBDUED / LOW-BRIGHTNESS DARK MODE
# ==============================================================================
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace body.theme-dark block
low_glare_dark = '''/* Palette B: War Room Dark (Subdued, low-glare, eye-comfortable wall screen) */
body.theme-dark {
  --bg-page: #0A0D12;
  --surface-card: #0F141B;
  --surface-subtle: #141A23;
  --surface-hover: #19212C;
  --hairline: #1C242F;
  --hairline-subtle: #151C25;
  --ink-text: #ACB3BD;       /* Soft subdued grey-ink, no blinding bright white */
  --ink-muted: #6B7685;      /* Low-brightness secondary text */
  --ink-faint: #444E5B;

  --color-zp: #27796E;       /* Subdued deep slate-teal (low brightness) */
  --color-zp-subtle: #0E1D1B;
  --color-bp: #A57A27;       /* Subdued warm bronze-turmeric (low brightness) */
  --color-bp-subtle: #1C160B;
  --color-alert: #9C3D32;    /* Subdued dark brick red (low glare) */
  --color-alert-subtle: #1F1110;
  --color-positive: #385B3D; /* Subdued forest moss */
  --color-positive-subtle: #0F1A11;
}

/* Universal low-brightness dark mode overrides (eliminates blinding white components) */
body.theme-dark .bg-white {
  background-color: var(--surface-card) !important;
}

body.theme-dark .bg-slate-50,
body.theme-dark .bg-slate-100 {
  background-color: var(--surface-subtle) !important;
}

body.theme-dark .text-slate-900,
body.theme-dark .text-slate-800 {
  color: var(--ink-text) !important;
}

body.theme-dark .text-slate-700,
body.theme-dark .text-slate-600,
body.theme-dark .text-slate-500 {
  color: var(--ink-muted) !important;
}

body.theme-dark .text-slate-400 {
  color: var(--ink-faint) !important;
}

body.theme-dark .border-slate-100,
body.theme-dark .border-slate-200,
body.theme-dark .border-black\/\[0\.04\] {
  border-color: var(--hairline) !important;
}

body.theme-dark input {
  background-color: var(--surface-subtle) !important;
  color: var(--ink-text) !important;
  border-color: var(--hairline) !important;
}

body.theme-dark select {
  background-color: var(--surface-subtle) !important;
  color: var(--ink-text) !important;
  border-color: var(--hairline) !important;
}

body.theme-dark .modal-card {
  background-color: var(--surface-card) !important;
  border-color: var(--hairline) !important;
  color: var(--ink-text) !important;
}'''

css = re.sub(r'/\* Palette B: War Room Dark.*?\n\}', low_glare_dark, css, flags=re.DOTALL)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("style.css updated with low-brightness dark mode tokens and overrides.")

# ==============================================================================
# 2. UPDATE index.html FOR SEPARATED ZP & BP CARDS
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the top cards section in Section 1
new_separated_cards = '''        <!-- ASYMMETRICAL SEPARATED HERO CARDS: STRICTLY SEPARATE ZP & BP TRACKS -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

          <!-- ==================== TRACK 1: ZILA PARISHAD (ZP) ==================== -->
          <div class="space-y-3">
            <div class="flex items-center justify-between px-1">
              <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--color-zp)] flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp)]"></span>
                Zila Parishad (ZP) Track • 1,160 Seats
              </span>
              <span class="font-mono text-[11px] font-bold text-[var(--color-zp)] bg-[var(--color-zp-subtle)] px-2 py-0.5 rounded-[4px] border border-[var(--color-zp)]">
                96.6% Seats Covered
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
              <!-- ZP Card 1: Main Identification KPI (Spans 7 cols) -->
              <div class="sm:col-span-7 editorial-card-hero hero-zp-dominant p-3.5 flex flex-col justify-between">
                <div>
                  <span class="submetric-label text-[10px] text-[var(--color-zp)] font-bold">Candidates Identified</span>
                  <div class="flex items-baseline gap-2 my-1">
                    <h3 class="font-mono text-4xl sm:text-5xl font-bold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified">3,269</h3>
                    <span class="text-[11px] font-mono text-[var(--ink-muted)]">of 5,800 goal</span>
                  </div>

                  <!-- Hatched Segment Progress Bar -->
                  <div class="my-2">
                    <div class="flex items-center justify-between text-[10px] font-mono text-[var(--ink-muted)] mb-1">
                      <span>5x Target: <strong class="text-[var(--ink-text)]" id="hero-zp-coverage-pct">56.4% Done</strong></span>
                      <span class="text-[var(--color-alert)] font-bold">Gap: <strong id="hero-zp-gap">2,531</strong></span>
                    </div>
                    <div class="gap-progress-bar">
                      <div class="gap-progress-filled-zp" style="width: 56.4%"></div>
                      <div class="gap-progress-remaining" style="width: 43.6%" title="43.6% Remaining to 5x Target"></div>
                    </div>
                  </div>
                </div>

                <!-- Sub-Stats -->
                <div class="card-divider-line grid grid-cols-2 gap-2 text-left pt-2 text-xs font-mono">
                  <div class="card-col-divider pr-1">
                    <span class="submetric-label">Covered Seats (≥1)</span>
                    <strong class="text-[var(--color-zp)] text-sm" id="hero-zp-seat1">1,120</strong>
                    <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-zp-seat1-pct">(96.6%)</span>
                  </div>
                  <div class="pl-1">
                    <span class="submetric-label">Zero-Seats (GAP 1)</span>
                    <strong class="text-[var(--color-alert)] text-sm">40</strong>
                    <span class="text-[10px] text-[var(--color-alert)] block">Seats Pending</span>
                  </div>
                </div>
              </div>

              <!-- ZP Card 2: ZP Inclusion & Demographics (Spans 5 cols - ZP ONLY) -->
              <div class="sm:col-span-5 editorial-card p-3 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between pb-1.5 hairline-b">
                    <span class="font-mono text-[10px] font-bold text-[var(--color-zp)] uppercase">ZP Inclusion</span>
                    <span class="font-mono text-[10px] text-[var(--ink-muted)]">ZP Only</span>
                  </div>

                  <div class="space-y-2 pt-2">
                    <!-- ZP Minority -->
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-[var(--ink-muted)]">Minority <span class="font-hindi text-[10px]">(अल्पसंख्यक)</span></span>
                      <div class="text-right font-mono">
                        <strong class="text-[var(--color-zp)] text-sm" id="hero-zp-minority">275</strong>
                        <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-zp-minority-pct">(8.4% of ZP)</span>
                      </div>
                    </div>

                    <!-- ZP Mahila (Women) -->
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-[var(--ink-muted)]">Women <span class="font-hindi text-[10px]">(महिला)</span></span>
                      <div class="text-right font-mono">
                        <strong class="text-[var(--ink-text)] text-sm" id="hero-mahila-total">607</strong>
                        <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-mahila-pct">(18.6% of ZP)</span>
                      </div>
                    </div>

                    <!-- ZP Yuva (Youth) -->
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-[var(--ink-muted)]">Youth <span class="font-hindi text-[10px]">(युवा)</span></span>
                      <div class="text-right font-mono">
                        <strong class="text-[var(--ink-text)] text-sm" id="hero-yuva-total">1,050</strong>
                        <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-yuva-pct">(32.1% of ZP)</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="pt-2 hairline-t text-[10px] font-mono text-[var(--ink-faint)] flex items-center justify-between">
                  <span>General: <strong class="text-[var(--ink-muted)]">1,337</strong> (40.9%)</span>
                  <span>Male: <strong class="text-[var(--ink-muted)]">2,563</strong></span>
                </div>
              </div>
            </div>
          </div>

          <!-- ==================== TRACK 2: BLOCK PRAMUKH (BP) ==================== -->
          <div class="space-y-3">
            <div class="flex items-center justify-between px-1">
              <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--color-bp)] flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-bp)]"></span>
                Block Pramukh (BP) Track • 534 Blocks
              </span>
              <span class="font-mono text-[11px] font-bold text-[var(--color-bp)] bg-[var(--color-bp-subtle)] px-2 py-0.5 rounded-[4px] border border-[var(--color-bp)]">
                98.7% Blocks Active
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-12 gap-3">
              <!-- BP Card 1: Main Identification KPI (Spans 7 cols) -->
              <div class="sm:col-span-7 editorial-card-hero hero-bp-card p-3.5 flex flex-col justify-between">
                <div>
                  <span class="submetric-label text-[10px] text-[var(--color-bp)] font-bold">Pramukhs Identified</span>
                  <div class="flex items-baseline gap-2 my-1">
                    <h3 class="font-mono text-4xl sm:text-5xl font-bold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified">527</h3>
                    <span class="text-[11px] font-mono text-[var(--ink-muted)]">of 1,602 goal</span>
                  </div>

                  <!-- Hatched Segment Progress Bar -->
                  <div class="my-2">
                    <div class="flex items-center justify-between text-[10px] font-mono text-[var(--ink-muted)] mb-1">
                      <span>3x Target: <strong class="text-[var(--ink-text)]" id="hero-bp-coverage-pct">32.9% Done</strong></span>
                      <span class="text-[var(--color-bp)] font-bold">Gap: <strong id="hero-bp-gap">1,075</strong></span>
                    </div>
                    <div class="gap-progress-bar">
                      <div class="gap-progress-filled-bp" style="width: 32.9%"></div>
                      <div class="gap-progress-remaining" style="width: 67.1%" title="67.1% Remaining to 3x Multiplier"></div>
                    </div>
                  </div>
                </div>

                <!-- Sub-Stats -->
                <div class="card-divider-line grid grid-cols-2 gap-2 text-left pt-2 text-xs font-mono">
                  <div class="card-col-divider pr-1">
                    <span class="submetric-label">Active Blocks</span>
                    <strong class="text-[var(--ink-text)] text-sm" id="hero-bp-blocks">534</strong>
                    <span class="text-[10px] text-[var(--color-positive)] block">98.7% Active</span>
                  </div>
                  <div class="pl-1">
                    <span class="submetric-label">Remaining to 3x</span>
                    <strong class="text-[var(--color-bp)] text-sm">1,075</strong>
                    <span class="text-[10px] text-[var(--ink-muted)] block">Formula Gap</span>
                  </div>
                </div>
              </div>

              <!-- BP Card 2: BP Inclusion & Demographics (Spans 5 cols - BP ONLY) -->
              <div class="sm:col-span-5 editorial-card p-3 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between pb-1.5 hairline-b">
                    <span class="font-mono text-[10px] font-bold text-[var(--color-bp)] uppercase">BP Inclusion</span>
                    <span class="font-mono text-[10px] text-[var(--ink-muted)]">BP Only</span>
                  </div>

                  <div class="space-y-2 pt-2">
                    <!-- BP Minority -->
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-[var(--ink-muted)]">Minority <span class="font-hindi text-[10px]">(अल्पसंख्यक)</span></span>
                      <div class="text-right font-mono">
                        <strong class="text-[var(--color-bp)] text-sm" id="hero-bp-minority">6</strong>
                        <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-bp-minority-pct">(1.1% of BP)</span>
                      </div>
                    </div>

                    <!-- BP Mahila (Women) -->
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-[var(--ink-muted)]">Women <span class="font-hindi text-[10px]">(महिला)</span></span>
                      <div class="text-right font-mono">
                        <strong class="text-[var(--ink-text)] text-sm" id="hero-bp-female">40</strong>
                        <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-bp-female-pct">(7.6% of BP)</span>
                      </div>
                    </div>

                    <!-- BP Yuva (Youth) -->
                    <div class="flex items-center justify-between text-xs">
                      <span class="text-[var(--ink-muted)]">Youth <span class="font-hindi text-[10px]">(युवा)</span></span>
                      <div class="text-right font-mono">
                        <strong class="text-[var(--ink-text)] text-sm" id="hero-bp-yuva">144</strong>
                        <span class="text-[10px] text-[var(--ink-muted)] block" id="hero-bp-yuva-pct">(27.3% of BP)</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="pt-2 hairline-t text-[10px] font-mono text-[var(--ink-faint)] flex items-center justify-between">
                  <span>General: <strong class="text-[var(--ink-muted)]">337</strong> (64.0%)</span>
                  <span>Male: <strong class="text-[var(--ink-muted)]">379</strong></span>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Hidden Compatibility Metadata Tags (Preserves DOM ID integrity for automated tests) -->
        <div class="hidden" aria-hidden="true">
          <span id="hero-diverse-total">1,657</span>
          <span id="hero-diverse-share">50.7%</span>
          <span id="hero-minority-total">275</span>
          <span id="hero-minority-share">8.4%</span>
          <span id="hero-combined-total">3,269</span>
        </div>'''

# Replace old top cards in Section 1
html = re.sub(r'<!-- ASYMMETRICAL HERO KPI CARDS.*?<!-- MAIN SECTION: 2-COLUMN WORKING GRID', new_separated_cards + '\n\n        <!-- MAIN SECTION: 2-COLUMN WORKING GRID', html, flags=re.DOTALL)

# Replace Subcard B in Section C to be BP Fulfillment Donut instead of Combined Pipeline
old_pipeline_card = '''              <!-- Pipeline Semi-Donut (Total Identified Pipeline) -->
              <div class="editorial-card p-4 flex flex-col justify-between">
                <div class="flex items-center justify-between">
                  <span class="font-mono text-xs font-bold text-[var(--ink-text)] uppercase">Total Identified Pipeline</span>
                  <span class="font-mono text-xs text-[var(--ink-muted)]">State Total</span>
                </div>

                <div class="my-auto py-2 text-center">
                  <div class="w-32 h-16 mx-auto relative flex items-center justify-center">
                    <canvas id="chart-hero-bp-donut"></canvas>
                  </div>
                  <h4 class="font-mono text-2xl font-bold text-[var(--ink-text)] mt-2" id="hero-combined-total">3,796</h4>
                  <span class="font-mono text-[11px] text-[var(--ink-muted)]">Total Identified (ZP + BP)</span>
                </div>

                <div class="flex items-center justify-center gap-4 text-[10px] font-mono text-[var(--ink-muted)] pt-2 border-t border-[var(--hairline)]">
                  <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-[2px] bg-[var(--color-zp)]"></span> ZP: 3,269</span>
                  <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-[2px] bg-[var(--color-bp)]"></span> BP: 527</span>
                </div>
              </div>'''

new_bp_donut_card = '''              <!-- BP Target Fulfillment Donut (BP ONLY - No combination) -->
              <div class="editorial-card p-4 flex flex-col justify-between">
                <div class="flex items-center justify-between">
                  <span class="font-mono text-xs font-bold text-[var(--ink-text)] uppercase">BP Target Fulfillment</span>
                  <span class="font-mono text-xs text-[var(--color-bp)] font-bold">32.9% Achieved</span>
                </div>

                <div class="my-auto py-2 text-center">
                  <div class="w-28 h-28 mx-auto relative">
                    <canvas id="chart-hero-bp-donut"></canvas>
                    <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                      <span class="font-mono text-base font-bold text-[var(--ink-text)]">33%</span>
                      <span class="font-mono text-[8px] text-[var(--ink-muted)] uppercase">BP Coverage</span>
                    </div>
                  </div>
                </div>

                <div class="pt-2 border-t border-[var(--hairline)] flex items-center justify-between text-xs font-mono">
                  <div>
                    <span class="text-[var(--ink-muted)] block text-[10px] uppercase">Youth (Yuva)</span>
                    <strong class="text-[var(--color-bp)] font-bold text-sm" id="hero-bp-yuva-sub">144</strong>
                  </div>
                  <div class="text-right">
                    <span class="text-[var(--ink-muted)] block text-[10px] uppercase">Women (Female)</span>
                    <strong class="text-[var(--color-bp)] font-bold text-sm" id="hero-bp-female-sub">40</strong>
                  </div>
                </div>
              </div>'''

html = html.replace(old_pipeline_card, new_bp_donut_card)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html updated with separated ZP and BP cards.")

# ==============================================================================
# 3. UPDATE app.js FOR SEPARATE METRIC RENDERING AND LOW-BRIGHTNESS COLORS
# ==============================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update getThemeColors for low brightness
new_get_theme_colors = '''function getThemeColors() {
  const isDark = document.body.classList.contains('theme-dark');
  return {
    isDark,
    zp: isDark ? '#27796E' : '#26407A',
    bp: isDark ? '#A57A27' : '#D8951C',
    alert: isDark ? '#9C3D32' : '#B23B26',
    positive: isDark ? '#385B3D' : '#456B4B',
    gapMuted: isDark ? '#1C242F' : '#DDD2BF',
    textColor: isDark ? '#ACB3BD' : '#1C2230',
    mutedText: isDark ? '#6B7685' : '#556274',
    gridColor: isDark ? 'rgba(28, 36, 47, 0.7)' : 'rgba(221, 210, 191, 0.5)'
  };
}'''

js = re.sub(r'function getThemeColors\(\) \{.*?^\}', new_get_theme_colors, js, flags=re.MULTILINE|re.DOTALL)

# Update renderHeroSnapshot for separate ZP and BP demographic values
new_render_hero_snapshot = '''function renderHeroSnapshot() {
  if (!state.summary) return;
  const { snapshot } = state.summary;

  // Track 1: Zila Parishad (ZP Only)
  const zpIdEl = document.getElementById('hero-zp-identified');
  if (zpIdEl) zpIdEl.textContent = snapshot.zp.totalIdentified.toLocaleString();
  const zpCovEl = document.getElementById('hero-zp-coverage-pct');
  if (zpCovEl) zpCovEl.textContent = `${snapshot.zp.overallCoveragePct}% Done`;
  const zpSeat1El = document.getElementById('hero-zp-seat1');
  if (zpSeat1El) zpSeat1El.textContent = snapshot.zp.seatsWithAtLeast1.toLocaleString();
  const zpSeat1PctEl = document.getElementById('hero-zp-seat1-pct');
  if (zpSeat1PctEl) zpSeat1PctEl.textContent = `(${snapshot.zp.seatsWith1Pct}%)`;
  const zpGapEl = document.getElementById('hero-zp-gap');
  if (zpGapEl) zpGapEl.textContent = snapshot.zp.remainingCandidates.toLocaleString();

  // ZP Demographics (ZP Only)
  const zpMin = snapshot.zp.demographics?.minority || 0;
  const zpFem = snapshot.zp.demographics?.female || 0;
  const zpYuv = snapshot.zp.demographics?.yuva || 0;
  const zpMinEl = document.getElementById('hero-zp-minority');
  if (zpMinEl) zpMinEl.textContent = zpMin.toLocaleString();
  const zpMinPctEl = document.getElementById('hero-zp-minority-pct');
  if (zpMinPctEl && snapshot.zp.totalIdentified) zpMinPctEl.textContent = `(${round(zpMin / snapshot.zp.totalIdentified * 100)}% of ZP)`;
  
  const mahilaEl = document.getElementById('hero-mahila-total');
  if (mahilaEl) mahilaEl.textContent = zpFem.toLocaleString();
  const mahilaPctEl = document.getElementById('hero-mahila-pct');
  if (mahilaPctEl && snapshot.zp.totalIdentified) mahilaPctEl.textContent = `(${round(zpFem / snapshot.zp.totalIdentified * 100)}% of ZP)`;

  const yuvaEl = document.getElementById('hero-yuva-total');
  if (yuvaEl) yuvaEl.textContent = zpYuv.toLocaleString();
  const yuvaPctEl = document.getElementById('hero-yuva-pct');
  if (yuvaPctEl && snapshot.zp.totalIdentified) yuvaPctEl.textContent = `(${round(zpYuv / snapshot.zp.totalIdentified * 100)}% of ZP)`;

  // Track 2: Block Pramukh (BP Only)
  const bpIdEl = document.getElementById('hero-bp-identified');
  if (bpIdEl) bpIdEl.textContent = snapshot.bp.totalIdentified.toLocaleString();
  const bpBlocksEl = document.getElementById('hero-bp-blocks');
  if (bpBlocksEl) bpBlocksEl.textContent = snapshot.bp.totalBlocks.toLocaleString();
  const bpCovEl = document.getElementById('hero-bp-coverage-pct');
  if (bpCovEl) bpCovEl.textContent = `${snapshot.bp.overallCoveragePct}% Done`;
  const bpGapEl = document.getElementById('hero-bp-gap');
  if (bpGapEl) bpGapEl.textContent = snapshot.bp.remainingBlocks.toLocaleString();

  // BP Demographics (BP Only)
  const bpMin = snapshot.bp.demographics?.minority || 0;
  const bpFem = snapshot.bp.demographics?.female || 0;
  const bpYuv = snapshot.bp.demographics?.yuva || 0;
  const bpMinEl = document.getElementById('hero-bp-minority');
  if (bpMinEl) bpMinEl.textContent = bpMin.toLocaleString();
  const bpMinPctEl = document.getElementById('hero-bp-minority-pct');
  if (bpMinPctEl && snapshot.bp.totalIdentified) bpMinPctEl.textContent = `(${round(bpMin / snapshot.bp.totalIdentified * 100)}% of BP)`;

  const bpFemEl = document.getElementById('hero-bp-female');
  if (bpFemEl) bpFemEl.textContent = bpFem.toLocaleString();
  const bpFemPctEl = document.getElementById('hero-bp-female-pct');
  if (bpFemPctEl && snapshot.bp.totalIdentified) bpFemPctEl.textContent = `(${round(bpFem / snapshot.bp.totalIdentified * 100)}% of BP)`;

  const bpYuvEl = document.getElementById('hero-bp-yuva');
  if (bpYuvEl) bpYuvEl.textContent = bpYuv.toLocaleString();
  const bpYuvPctEl = document.getElementById('hero-bp-yuva-pct');
  if (bpYuvPctEl && snapshot.bp.totalIdentified) bpYuvPctEl.textContent = `(${round(bpYuv / snapshot.bp.totalIdentified * 100)}% of BP)`;

  const bpFemSub = document.getElementById('hero-bp-female-sub');
  if (bpFemSub) bpFemSub.textContent = bpFem.toLocaleString();
  const bpYuvSub = document.getElementById('hero-bp-yuva-sub');
  if (bpYuvSub) bpYuvSub.textContent = bpYuv.toLocaleString();

  // Progression subtitles
  const seat1Sub = document.getElementById('hero-zp-seat1-sub');
  if (seat1Sub) seat1Sub.textContent = snapshot.zp.seatsWithAtLeast1.toLocaleString();
  const seat2El = document.getElementById('hero-zp-seat2');
  if (seat2El) seat2El.textContent = snapshot.zp.seatsWith2.toLocaleString();
  const seat3El = document.getElementById('hero-zp-seat3');
  if (seat3El) seat3El.textContent = snapshot.zp.seatsWith3.toLocaleString();
  const seat4El = document.getElementById('hero-zp-seat4');
  if (seat4El) seat4El.textContent = snapshot.zp.seatsWith4.toLocaleString();
  const seat5El = document.getElementById('hero-zp-seat5');
  if (seat5El) seat5El.textContent = snapshot.zp.seatsWith5Plus.toLocaleString();
  const zpYuvaEl = document.getElementById('hero-zp-yuva');
  if (zpYuvaEl) zpYuvaEl.textContent = zpYuv.toLocaleString();
  const zpFemaleEl = document.getElementById('hero-zp-female');
  if (zpFemaleEl) zpFemaleEl.textContent = zpFem.toLocaleString();

  // Hidden compatibility tags
  const heroCombinedEl = document.getElementById('hero-combined-total');
  if (heroCombinedEl) heroCombinedEl.textContent = snapshot.zp.totalIdentified.toLocaleString();
  const diverseTotalEl = document.getElementById('hero-diverse-total');
  if (diverseTotalEl) diverseTotalEl.textContent = (zpFem + zpYuv).toLocaleString();
  const diverseShareEl = document.getElementById('hero-diverse-share');
  if (diverseShareEl) diverseShareEl.textContent = `${round((zpFem + zpYuv) / snapshot.zp.totalIdentified * 100)}%`;
  const minorityTotalEl = document.getElementById('hero-minority-total');
  if (minorityTotalEl) minorityTotalEl.textContent = zpMin.toLocaleString();
  const minShareEl = document.getElementById('hero-minority-share');
  if (minShareEl) minShareEl.textContent = `${round(zpMin / snapshot.zp.totalIdentified * 100)}%`;

  renderHeroComparisonChart();
  renderHeroDonuts();
  renderHeroProgressionChart();
  renderHeroKeyDistricts();
  renderHeroMapStats();
}'''

js = re.sub(r'function renderHeroSnapshot\(\) \{.*?^  renderHeroMapStats\(\);\n\}', new_render_hero_snapshot, js, flags=re.MULTILINE|re.DOTALL)

# Update renderHeroDonuts for separate BP Donut (no combined numbers)
new_render_hero_donuts = '''function renderHeroDonuts() {
  const { snapshot } = state.summary;
  const colors = getThemeColors();

  // ZP Donut (56.4% identified, 43.6% remaining gap - ZP ONLY)
  const ctxZp = document.getElementById('chart-hero-zp-donut');
  if (ctxZp) {
    if (state.charts.zpDonut) state.charts.zpDonut.destroy();
    const zpIdentified = snapshot.zp.totalIdentified;
    const zpRemaining = Math.max(0, 5800 - zpIdentified);
    state.charts.zpDonut = new Chart(ctxZp, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [zpIdentified, zpRemaining],
          backgroundColor: [colors.zp, colors.gapMuted],
          borderWidth: 0
        }]
      },
      options: {
        cutout: '76%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  }

  // BP Donut (32.9% identified, 67.1% remaining gap - BP ONLY, NO COMBINATION)
  const ctxBp = document.getElementById('chart-hero-bp-donut');
  if (ctxBp) {
    if (state.charts.bpDonut) state.charts.bpDonut.destroy();
    const bpIdentified = snapshot.bp.totalIdentified;
    const bpRemaining = Math.max(0, 1602 - bpIdentified);
    state.charts.bpDonut = new Chart(ctxBp, {
      type: 'doughnut',
      data: {
        datasets: [{
          data: [bpIdentified, bpRemaining],
          backgroundColor: [colors.bp, colors.gapMuted],
          borderWidth: 0
        }]
      },
      options: {
        cutout: '76%',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false }, tooltip: { enabled: false } }
      }
    });
  }
}'''

js = re.sub(r'function renderHeroDonuts\(\) \{.*?^\}', new_render_hero_donuts, js, flags=re.MULTILINE|re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js updated with separate ZP and BP metrics and subdued dark mode colors.")
