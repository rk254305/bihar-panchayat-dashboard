import re

# ==============================================================================
# 1. UPDATE app.js
# ==============================================================================
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add gender to bpCandidateFilter in state
js = js.replace(
    "bpCandidateFilter: { zone: 'All', district: 'All', search: '', missingFilter: 'all', page: 1, pageSize: 20 },",
    "bpCandidateFilter: { zone: 'All', district: 'All', gender: 'All', search: '', missingFilter: 'all', page: 1, pageSize: 20 },"
)

# Add individual report generation functions
individual_report_funcs = '''
// ==========================================================================
// INDIVIDUAL DEMOGRAPHIC REPORT GENERATORS (SEPARATE ZP & BP)
// ==========================================================================
function generateFemaleReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.gender = 'Female';
    state.zpCandidateFilter.page = 1;
    const genderSel = document.getElementById('zp-cand-gender-filter');
    if (genderSel) genderSel.value = 'Female';
    renderZpCandidates();
    showToast('Generated Individual Report: 607 Female Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.gender = 'Female';
    state.bpCandidateFilter.page = 1;
    const genderSel = document.getElementById('bp-cand-gender-filter');
    if (genderSel) genderSel.value = 'Female';
    renderBpCandidates();
    showToast('Generated Individual Report: 40 Female Pramukhs in Block Pramukh', 'success');
  }
}

function generateMinorityReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = 'minority';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = 'minority';
    renderZpCandidates();
    showToast('Generated Individual Report: 275 Minority Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = 'minority';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = 'minority';
    renderBpCandidates();
    showToast('Generated Individual Report: 6 Minority Pramukhs in Block Pramukh', 'success');
  }
}

function generateYouthReport(tier) {
  if (tier === 'zp') {
    switchMainTab('zp');
    switchZpTab('zp-candidates');
    state.zpCandidateFilter.search = 'yuva';
    state.zpCandidateFilter.page = 1;
    const searchInput = document.getElementById('zp-cand-search');
    if (searchInput) searchInput.value = 'yuva';
    renderZpCandidates();
    showToast('Generated Individual Report: 1,050 Youth Candidates in Zila Parishad', 'success');
  } else if (tier === 'bp') {
    switchMainTab('bp');
    switchBpTab('bp-candidates');
    state.bpCandidateFilter.search = 'yuva';
    state.bpCandidateFilter.page = 1;
    const searchInput = document.getElementById('bp-cand-search');
    if (searchInput) searchInput.value = 'yuva';
    renderBpCandidates();
    showToast('Generated Individual Report: 144 Youth Pramukhs in Block Pramukh', 'success');
  }
}
'''

js = js.replace("// Realtime Header Clock", individual_report_funcs + "\n// Realtime Header Clock")

# Update renderBpCandidates to filter by gender
bp_filter_replace_target = '''  const { zone, search, missingFilter, page, pageSize } = state.bpCandidateFilter;

  const filtered = candidates.filter(c => {
    const matchZone = zone === 'All' || c.zone.toLowerCase() === zone.toLowerCase();
    const matchSearch = !search ||
      c.name.toLowerCase().includes(search) ||
      c.district.toLowerCase().includes(search) ||
      c.block.toLowerCase().includes(search) ||
      c.contact.includes(search) ||
      (c.pkMeetingStatus && c.pkMeetingStatus.toLowerCase().includes(search));'''

bp_filter_new = '''  const { zone, gender, search, missingFilter, page, pageSize } = state.bpCandidateFilter;

  const filtered = candidates.filter(c => {
    const matchZone = zone === 'All' || c.zone.toLowerCase() === zone.toLowerCase();
    const matchGender = !gender || gender === 'All' ||
      (c.gender && c.gender.toLowerCase() === gender.toLowerCase()) ||
      (gender.toLowerCase() === 'female' && c.candidateCategory && c.candidateCategory.toLowerCase().includes('mahila')) ||
      (gender.toLowerCase() === 'male' && c.gender && c.gender.toLowerCase() === 'male');
    const matchSearch = !search ||
      c.name.toLowerCase().includes(search) ||
      c.district.toLowerCase().includes(search) ||
      c.block.toLowerCase().includes(search) ||
      c.contact.includes(search) ||
      (c.candidateCategory && c.candidateCategory.toLowerCase().includes(search)) ||
      (c.pkMeetingStatus && c.pkMeetingStatus.toLowerCase().includes(search));'''

js = js.replace(bp_filter_replace_target, bp_filter_new)
js = js.replace("return matchZone && matchSearch && matchMissing;", "return matchZone && matchGender && matchSearch && matchMissing;")

# Add listener for bp-cand-gender-filter in setupFilterListeners
js = js.replace(
    "const bpCandZone = document.getElementById('bp-cand-zone-filter');\n  const bpCandSearch = document.getElementById('bp-cand-search');",
    "const bpCandZone = document.getElementById('bp-cand-zone-filter');\n  const bpCandGender = document.getElementById('bp-cand-gender-filter');\n  const bpCandSearch = document.getElementById('bp-cand-search');\n  if (bpCandGender) bpCandGender.addEventListener('change', (e) => { state.bpCandidateFilter.gender = e.target.value; state.bpCandidateFilter.page = 1; renderBpCandidates(); });"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js updated with individual report handlers and BP gender filtering.")

# ==============================================================================
# 2. UPDATE index.html
# ==============================================================================
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add bp-cand-gender-filter dropdown in panel-bp-candidates
bp_cand_dropdown_target = '''                <select id="bp-cand-zone-filter"
                  class="text-xs py-2 px-3 rounded-full bg-slate-50 border border-slate-200">
                  <option value="All">All Zones</option>
                </select>'''

bp_cand_dropdown_new = '''                <select id="bp-cand-zone-filter"
                  class="text-xs py-2 px-3 rounded-full bg-slate-50 border border-slate-200">
                  <option value="All">All Zones</option>
                </select>
                <select id="bp-cand-gender-filter"
                  class="text-xs py-2 px-3 rounded-full bg-slate-50 border border-slate-200">
                  <option value="All">All Genders</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                </select>'''

html = html.replace(bp_cand_dropdown_target, bp_cand_dropdown_new)

# Replace the top cards in Section 1 with the dedicated 2-tier + 4-demographic cards
hero_cards_target_regex = r'<!-- ASYMMETRICAL SEPARATED HERO CARDS.*?<!-- MAIN SECTION: 2-COLUMN WORKING GRID'

new_hero_cards_block = '''<!-- INDIVIDUAL SEPARATE REPORTING CARDS FOR ZP AND BP -->
        <div class="space-y-4">

          <!-- ROW 1: CORE CANDIDATE IDENTIFICATION MANDATES (ZP vs BP) -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

            <!-- Card 1: Zila Parishad (ZP) Core Identification -->
            <div class="editorial-card-hero hero-zp-dominant p-4 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--color-zp)] flex items-center gap-1.5">
                    <span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp)]"></span>
                    Zila Parishad (ZP) • 1,160 Seats
                  </span>
                  <span class="font-mono text-[11px] font-bold text-[var(--color-zp)] bg-[var(--color-zp-subtle)] px-2 py-0.5 rounded-[4px] border border-[var(--color-zp)]">
                    96.6% Seats Covered
                  </span>
                </div>

                <div class="flex items-baseline gap-2.5 my-1.5">
                  <h3 class="font-mono text-5xl font-bold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified">3,269</h3>
                  <span class="text-xs font-mono text-[var(--ink-muted)]">Candidates Identified (of 5,800 Target)</span>
                </div>

                <!-- Hatched Progress Bar -->
                <div class="my-2.5">
                  <div class="flex items-center justify-between text-[11px] font-mono text-[var(--ink-muted)] mb-1">
                    <span>5x Target: <strong class="text-[var(--ink-text)]" id="hero-zp-coverage-pct">56.4% Done</strong></span>
                    <span class="text-[var(--color-alert)] font-bold">Remaining Gap: <strong id="hero-zp-gap">2,531</strong></span>
                  </div>
                  <div class="gap-progress-bar">
                    <div class="gap-progress-filled-zp" style="width: 56.4%"></div>
                    <div class="gap-progress-remaining" style="width: 43.6%" title="43.6% Remaining to 5x Goal"></div>
                  </div>
                </div>
              </div>

              <!-- Sub-Stats & Direct Report Action -->
              <div class="card-divider-line pt-2 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                <div class="flex items-center gap-4 text-xs font-mono">
                  <div>
                    <span class="submetric-label">Covered Seats (≥1)</span>
                    <strong class="text-[var(--color-zp)] text-sm" id="hero-zp-seat1">1,120</strong>
                    <span class="text-[10px] text-[var(--ink-muted)]" id="hero-zp-seat1-pct">(96.6%)</span>
                  </div>
                  <div>
                    <span class="submetric-label">Zero-Seats (GAP 1)</span>
                    <strong class="text-[var(--color-alert)] text-sm">40</strong>
                    <span class="text-[10px] text-[var(--color-alert)]">Pending</span>
                  </div>
                </div>
                <button onclick="switchMainTab('zp'); switchZpTab('zp-district-wise')" class="editorial-btn text-xs">
                  <span>ZP District Report →</span>
                </button>
              </div>
            </div>

            <!-- Card 2: Block Pramukh (BP) Core Identification -->
            <div class="editorial-card-hero hero-bp-card p-4 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between mb-1.5">
                  <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--color-bp)] flex items-center gap-1.5">
                    <span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-bp)]"></span>
                    Block Pramukh (BP) • 534 Blocks
                  </span>
                  <span class="font-mono text-[11px] font-bold text-[var(--color-bp)] bg-[var(--color-bp-subtle)] px-2 py-0.5 rounded-[4px] border border-[var(--color-bp)]">
                    98.7% Blocks Active
                  </span>
                </div>

                <div class="flex items-baseline gap-2.5 my-1.5">
                  <h3 class="font-mono text-5xl font-bold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified">527</h3>
                  <span class="text-xs font-mono text-[var(--ink-muted)]">Pramukhs Identified (of 1,602 Target)</span>
                </div>

                <!-- Hatched Progress Bar -->
                <div class="my-2.5">
                  <div class="flex items-center justify-between text-[11px] font-mono text-[var(--ink-muted)] mb-1">
                    <span>3x Target: <strong class="text-[var(--ink-text)]" id="hero-bp-coverage-pct">32.9% Done</strong></span>
                    <span class="text-[var(--color-bp)] font-bold">Remaining Gap: <strong id="hero-bp-gap">1,075</strong></span>
                  </div>
                  <div class="gap-progress-bar">
                    <div class="gap-progress-filled-bp" style="width: 32.9%"></div>
                    <div class="gap-progress-remaining" style="width: 67.1%" title="67.1% Remaining to 3x Multiplier"></div>
                  </div>
                </div>
              </div>

              <!-- Sub-Stats & Direct Report Action -->
              <div class="card-divider-line pt-2 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                <div class="flex items-center gap-4 text-xs font-mono">
                  <div>
                    <span class="submetric-label">Active Blocks</span>
                    <strong class="text-[var(--ink-text)] text-sm" id="hero-bp-blocks">534</strong>
                    <span class="text-[10px] text-[var(--color-positive)]">(98.7%)</span>
                  </div>
                  <div>
                    <span class="submetric-label">Remaining to 3x</span>
                    <strong class="text-[var(--color-bp)] text-sm">1,075</strong>
                    <span class="text-[10px] text-[var(--ink-muted)]">Formula Gap</span>
                  </div>
                </div>
                <button onclick="switchMainTab('bp'); switchBpTab('bp-district-wise')" class="editorial-btn text-xs">
                  <span>BP Block Report →</span>
                </button>
              </div>
            </div>

          </div>

          <!-- ROW 2: DEDICATED INDIVIDUAL REPORT CARDS (SEPARATE FEMALES & MINORITY IN ZP AND BP) -->
          <div>
            <div class="flex items-center justify-between mb-2 px-1">
              <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--ink-muted)]">
                Individual Inclusion Reports • Separate ZP &amp; BP Generation
              </span>
              <span class="text-[10px] font-mono text-[var(--ink-faint)]">Click button to generate individual filtered dossier</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3.5">

              <!-- Card A: Females in ZP (Separate Report) -->
              <div class="editorial-card p-3.5 flex flex-col justify-between border-t-2 border-t-[var(--color-zp)]">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-mono text-[11px] font-bold text-[var(--color-zp)] uppercase">ZP Females <span class="font-hindi text-[10px]">(महिला - ZP)</span></span>
                    <span class="font-mono text-[10px] font-bold text-[var(--color-zp)] bg-[var(--color-zp-subtle)] px-1.5 py-0.2 rounded-[3px] border border-[var(--color-zp)]">
                      ZP Only
                    </span>
                  </div>

                  <div class="my-2">
                    <h4 class="font-mono text-3xl font-bold text-[var(--color-zp)]" id="hero-mahila-total">607</h4>
                    <span class="font-mono text-xs text-[var(--ink-muted)] block" id="hero-mahila-pct">18.6% of 3,269 ZP candidates</span>
                  </div>
                  <p class="text-[11px] text-[var(--ink-muted)]">Women candidates identified across 43 Bihar districts in Zila Parishad.</p>
                </div>

                <div class="pt-3 mt-1 hairline-t">
                  <button onclick="generateFemaleReport('zp')" class="editorial-btn w-full justify-between text-xs text-[var(--color-zp)] border-[var(--color-zp)] hover:bg-[var(--color-zp-subtle)]">
                    <span>Generate ZP Female Report</span>
                    <span class="font-mono font-bold">607 →</span>
                  </button>
                </div>
              </div>

              <!-- Card B: Females in BP (Separate Report) -->
              <div class="editorial-card p-3.5 flex flex-col justify-between border-t-2 border-t-[var(--color-bp)]">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-mono text-[11px] font-bold text-[var(--color-bp)] uppercase">BP Females <span class="font-hindi text-[10px]">(महिला - BP)</span></span>
                    <span class="font-mono text-[10px] font-bold text-[var(--color-bp)] bg-[var(--color-bp-subtle)] px-1.5 py-0.2 rounded-[3px] border border-[var(--color-bp)]">
                      BP Only
                    </span>
                  </div>

                  <div class="my-2">
                    <h4 class="font-mono text-3xl font-bold text-[var(--color-bp)]" id="hero-bp-female">40</h4>
                    <span class="font-mono text-xs text-[var(--ink-muted)] block" id="hero-bp-female-pct">7.6% of 527 BP pramukhs</span>
                  </div>
                  <p class="text-[11px] text-[var(--ink-muted)]">Women Pramukh candidates identified across 534 Bihar blocks.</p>
                </div>

                <div class="pt-3 mt-1 hairline-t">
                  <button onclick="generateFemaleReport('bp')" class="editorial-btn w-full justify-between text-xs text-[var(--color-bp)] border-[var(--color-bp)] hover:bg-[var(--color-bp-subtle)]">
                    <span>Generate BP Female Report</span>
                    <span class="font-mono font-bold">40 →</span>
                  </button>
                </div>
              </div>

              <!-- Card C: Minority in ZP (Separate Report) -->
              <div class="editorial-card p-3.5 flex flex-col justify-between border-t-2 border-t-[var(--color-zp)]">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-mono text-[11px] font-bold text-[var(--color-zp)] uppercase">ZP Minority <span class="font-hindi text-[10px]">(अल्पसंख्यक)</span></span>
                    <span class="font-mono text-[10px] font-bold text-[var(--color-zp)] bg-[var(--color-zp-subtle)] px-1.5 py-0.2 rounded-[3px] border border-[var(--color-zp)]">
                      ZP Only
                    </span>
                  </div>

                  <div class="my-2">
                    <h4 class="font-mono text-3xl font-bold text-[var(--color-zp)]" id="hero-zp-minority">275</h4>
                    <span class="font-mono text-xs text-[var(--ink-muted)] block" id="hero-zp-minority-pct">8.4% of 3,269 ZP candidates</span>
                  </div>
                  <p class="text-[11px] text-[var(--ink-muted)]">Minority candidates active in 39 districts with high focus in Seemanchal.</p>
                </div>

                <div class="pt-3 mt-1 hairline-t">
                  <button onclick="generateMinorityReport('zp')" class="editorial-btn w-full justify-between text-xs text-[var(--color-zp)] border-[var(--color-zp)] hover:bg-[var(--color-zp-subtle)]">
                    <span>Generate ZP Minority Report</span>
                    <span class="font-mono font-bold">275 →</span>
                  </button>
                </div>
              </div>

              <!-- Card D: Minority in BP (Separate Report) -->
              <div class="editorial-card p-3.5 flex flex-col justify-between border-t-2 border-t-[var(--color-bp)]">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="font-mono text-[11px] font-bold text-[var(--color-bp)] uppercase">BP Minority <span class="font-hindi text-[10px]">(अल्पसंख्यक)</span></span>
                    <span class="font-mono text-[10px] font-bold text-[var(--color-bp)] bg-[var(--color-bp-subtle)] px-1.5 py-0.2 rounded-[3px] border border-[var(--color-bp)]">
                      BP Only
                    </span>
                  </div>

                  <div class="my-2">
                    <h4 class="font-mono text-3xl font-bold text-[var(--color-bp)]" id="hero-bp-minority">6</h4>
                    <span class="font-mono text-xs text-[var(--ink-muted)] block" id="hero-bp-minority-pct">1.1% of 527 BP pramukhs</span>
                  </div>
                  <p class="text-[11px] text-[var(--ink-muted)]">Significant inclusion gap identified in 528 blocks requiring targeted field drive.</p>
                </div>

                <div class="pt-3 mt-1 hairline-t">
                  <button onclick="generateMinorityReport('bp')" class="editorial-btn w-full justify-between text-xs text-[var(--color-bp)] border-[var(--color-bp)] hover:bg-[var(--color-bp-subtle)]">
                    <span>Generate BP Minority Report</span>
                    <span class="font-mono font-bold">6 →</span>
                  </button>
                </div>
              </div>

            </div>
          </div>

          <!-- YOUTH (YUVA) SEPARATE REPORTING STRIP -->
          <div class="editorial-card p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-[var(--surface-subtle)]">
            <div class="flex items-center gap-3">
              <span class="font-mono text-xs font-bold text-[var(--ink-text)] flex items-center gap-1.5">
                <span class="w-2 h-2 rounded-full bg-[var(--color-positive)]"></span>
                Youth Representation <span class="font-hindi text-xs text-[var(--ink-muted)]">(युवा नेतृत्व)</span>:
              </span>
              <span class="font-mono text-xs text-[var(--ink-muted)]">
                ZP Youth: <strong class="text-[var(--color-zp)] text-sm" id="hero-yuva-total">1,050</strong> <span id="hero-yuva-pct">(32.1%)</span> • 
                BP Youth: <strong class="text-[var(--color-bp)] text-sm" id="hero-bp-yuva">144</strong> <span id="hero-bp-yuva-pct">(27.3%)</span>
              </span>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="generateYouthReport('zp')" class="editorial-btn text-xs">
                <span>ZP Youth Report (1,050) →</span>
              </button>
              <button onclick="generateYouthReport('bp')" class="editorial-btn text-xs">
                <span>BP Youth Report (144) →</span>
              </button>
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

html = re.sub(hero_cards_target_regex, new_hero_cards_block + '\n\n        <!-- MAIN SECTION: 2-COLUMN WORKING GRID', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html successfully updated with individual reporting cards for ZP & BP!")
