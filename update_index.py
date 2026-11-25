import re

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    orig_html = f.read()

# Read the generated SVG map snippet
with open('bihar_map_snippet.html', 'r', encoding='utf-8') as f:
    map_snippet = f.read()

# 1. Update <head> font imports and Tailwind config
head_replacement = '''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bihar Panchayat Nominations 2026 - Executive Dashboard</title>

  <!-- Google Fonts: IBM Plex Sans, IBM Plex Mono, Mukta (Devanagari) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Mukta:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['"IBM Plex Sans"', 'sans-serif'],
            mono: ['"IBM Plex Mono"', 'monospace'],
            hindi: ['"Mukta"', '"IBM Plex Sans"', 'sans-serif']
          },
          colors: {
            appbg: 'var(--bg-page)',
            zp: {
              DEFAULT: '#26407A',
              subtle: '#E6ECF7'
            },
            bp: {
              DEFAULT: '#D8951C',
              subtle: '#FBF3E4'
            },
            alert: {
              DEFAULT: '#B23B26',
              subtle: '#F8E7E4'
            },
            positive: {
              DEFAULT: '#456B4B',
              subtle: '#E8F0EA'
            }
          }
        }
      }
    }
  </script>

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <!-- Editorial Stylesheet: Mithila Ink & War Room Dark -->
  <link rel="stylesheet" href="style.css">
</head>'''

# 2. Update Header actions to include theme switcher
header_new = '''      <!-- TOP HEADER (Overview Title, Filter Pills, Action Buttons) -->
      <header
        class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-[var(--surface-card)] border border-[var(--hairline)] p-3.5 rounded-[6px]">

        <!-- Left: Drawer Toggle (Mobile) + Title & Filter Pills -->
        <div class="flex items-center flex-wrap gap-3">
          <button id="drawer-toggle-btn" onclick="toggleMobileDrawer()"
            class="lg:hidden p-1.5 rounded-[4px] border border-[var(--hairline)] bg-[var(--surface-card)] text-[var(--ink-text)] hover:bg-[var(--surface-hover)] transition-colors"
            title="Open Navigation Menu">
            <i data-lucide="menu" class="w-4 h-4"></i>
          </button>

          <h2 id="page-main-title" class="text-xl sm:text-2xl font-bold font-sans text-[var(--ink-text)] tracking-tight">Overview</h2>

          <!-- Pill Filter Group -->
          <div class="pill-filter-group">
            <button onclick="switchMainTab('hero')" id="pill-all-zones" class="pill-filter-btn pill-filter-btn-active">
              Statewide
            </button>
            <button onclick="switchMainTab('zp')" id="pill-zp-filter" class="pill-filter-btn">
              Zila Parishad
            </button>
            <button onclick="switchMainTab('bp')" id="pill-bp-filter" class="pill-filter-btn">
              Block Pramukh
            </button>
          </div>
        </div>

        <!-- Right: Actions & Theme Switcher -->
        <div class="flex items-center flex-wrap gap-2 w-full sm:w-auto justify-end">

          <!-- Palette / Theme Toggle Button -->
          <button id="theme-toggle-btn" onclick="toggleTheme()" class="theme-switch-btn"
            title="Switch between Palette A (Mithila Ink) and Palette B (War Room Dark)">
            <i data-lucide="moon" id="theme-toggle-icon" class="w-3.5 h-3.5 text-[var(--color-bp)]"></i>
            <span id="theme-toggle-text">War Room</span>
          </button>

          <!-- Sync Now Button -->
          <button id="btn-sync-now" onclick="syncLiveSheetData(true)" class="editorial-btn"
            title="Sync Live with Google Sheet">
            <i data-lucide="refresh-cw" id="sync-icon" class="w-3.5 h-3.5 text-[var(--color-zp)]"></i>
            <span class="hidden md:inline">Sync Sheet</span>
          </button>

          <!-- Export Button -->
          <button onclick="exportTableToCsv('zp-districts')" class="editorial-btn">
            <i data-lucide="download" class="w-3.5 h-3.5 text-[var(--ink-muted)]"></i>
            <span class="hidden md:inline">+ New Report</span>
          </button>

          <!-- Primary CTA Button (Google Sheet) -->
          <a href="https://docs.google.com/spreadsheets/d/1Dr5pYkkBs-nR0cYYod5yLLRChorfvsT7Lp0qtwa1xS8/edit?gid=1080948893#gid=1080948893"
            target="_blank" rel="noopener noreferrer" class="editorial-btn editorial-btn-primary">
            <span>Google Sheet</span>
            <i data-lucide="arrow-up-right" class="w-3.5 h-3.5"></i>
          </a>

        </div>
      </header>'''

# 3. New Editorial Hero Section
new_hero_section = f'''      <!-- ========================================================================= -->
      <!-- SECTION 1: HERO OVERVIEW (Editorial Asymmetrical Hierarchy)               -->
      <!-- ========================================================================= -->
      <section id="section-hero" class="main-section space-y-4">

        <!-- EXECUTIVE OVERVIEW SUBHEADER -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 pt-0.5">
          <div>
            <h3 class="text-base font-bold text-[var(--ink-text)] tracking-tight">Bihar Panchayat 2026 Nominations</h3>
            <p class="text-xs text-[var(--ink-muted)] font-mono mt-0.5">38 Revenue Districts • 43 Reporting Units • 12 Administrative Zones</p>
          </div>
          <div class="flex items-center gap-2 text-xs font-mono">
            <span class="px-2 py-0.5 rounded-[4px] bg-[var(--color-zp-subtle)] text-[var(--color-zp)] font-bold border border-[var(--color-zp)]">
              1,160 ZP Seats
            </span>
            <span class="px-2 py-0.5 rounded-[4px] bg-[var(--color-bp-subtle)] text-[var(--color-bp)] font-bold border border-[var(--color-bp)]">
              534 Blocks
            </span>
            <span class="px-2 py-0.5 rounded-[4px] bg-[var(--color-positive-subtle)] text-[var(--color-positive)] font-semibold border border-[var(--color-positive)] flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-[var(--color-positive)]"></span> Live Sync
            </span>
          </div>
        </div>

        <!-- ASYMMETRICAL HERO KPI CARDS: 3,269 ZP IS THE HERO -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-3.5">

          <!-- Card 1: THE HERO (Zila Parishad - Spans 2 Columns on Desktop) -->
          <div class="sm:col-span-2 xl:col-span-2 editorial-card-hero hero-zp-dominant p-4 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--color-zp)] flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-[2px] bg-[var(--color-zp)]"></span>
                  Zila Parishad (ZP) Identified Candidates
                </span>
                <span class="font-mono text-xs font-bold text-[var(--color-zp)] bg-[var(--color-zp-subtle)] px-2 py-0.5 rounded-[4px] border border-[var(--color-zp)]">
                  96.6% Seats Active
                </span>
              </div>

              <!-- GIANT HERO NUMBER -->
              <div class="flex items-baseline gap-3 my-1">
                <h3 class="font-mono text-5xl lg:text-6xl font-bold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified">3,269</h3>
                <span class="text-xs text-[var(--ink-muted)] font-medium">candidates identified statewide</span>
              </div>

              <!-- Hatched Segment Progress Indicator (Showing 56.4% done & remaining gap) -->
              <div class="mt-2.5 mb-1.5">
                <div class="flex items-center justify-between text-[11px] font-mono text-[var(--ink-muted)] mb-1">
                  <span>Progress to 5x Target: <strong class="text-[var(--ink-text)]" id="hero-zp-coverage-pct">56.4% Done</strong> (5,800 Goal)</span>
                  <span class="text-[var(--color-alert)] font-semibold">Remaining Gap: <strong id="hero-zp-gap">2,531</strong></span>
                </div>
                <div class="gap-progress-bar">
                  <div class="gap-progress-filled-zp" style="width: 56.4%"></div>
                  <div class="gap-progress-remaining" style="width: 43.6%" title="43.6% Remaining Multiplier Gap"></div>
                </div>
              </div>
            </div>

            <!-- Hairline Sub-Stats -->
            <div class="card-divider-line grid grid-cols-2 gap-2 text-center pt-2">
              <div class="card-col-divider pr-2 text-left">
                <span class="submetric-label">Seats Covered (≥1 Candidate)</span>
                <div class="flex items-baseline gap-1 mt-0.5">
                  <span class="font-mono text-lg font-bold text-[var(--color-zp)]" id="hero-zp-seat1">1,120</span>
                  <span class="font-mono text-xs text-[var(--ink-muted)]" id="hero-zp-seat1-pct">(96.6% of 1,160)</span>
                </div>
              </div>
              <div class="pl-2 text-left">
                <span class="submetric-label">Zero-Candidate Seats (GAP 1)</span>
                <div class="flex items-baseline gap-1 mt-0.5">
                  <span class="font-mono text-lg font-bold text-[var(--color-alert)]">40</span>
                  <span class="font-mono text-xs text-[var(--color-alert)]">Seats (3.4% gap)</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Card 2: Block Pramukh (BP) - Turmeric Theme (1 Column) -->
          <div class="editorial-card-hero hero-bp-card p-4 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1.5">
                <span class="font-mono text-xs font-bold uppercase tracking-wider text-[var(--color-bp)] flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-[2px] bg-[var(--color-bp)]"></span>
                  Block Pramukh (BP)
                </span>
                <span class="font-mono text-[10px] font-bold text-[var(--color-bp)] bg-[var(--color-bp-subtle)] px-1.5 py-0.5 rounded-[4px] border border-[var(--color-bp)]">
                  98.7% Active
                </span>
              </div>

              <!-- Prominent BP Number -->
              <div class="my-1">
                <h3 class="font-mono text-4xl font-bold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified">527</h3>
                <span class="text-[11px] text-[var(--ink-muted)]">Pramukhs Identified</span>
              </div>

              <!-- BP Segment Progress -->
              <div class="mt-2 mb-1.5">
                <div class="flex items-center justify-between text-[11px] font-mono text-[var(--ink-muted)] mb-1">
                  <span>Target 3x: <strong class="text-[var(--ink-text)]" id="hero-bp-coverage-pct">32.9% Done</strong></span>
                  <span class="text-[var(--ink-muted)] font-mono">1,602 Goal</span>
                </div>
                <div class="gap-progress-bar">
                  <div class="gap-progress-filled-bp" style="width: 32.9%"></div>
                  <div class="gap-progress-remaining" style="width: 67.1%" title="67.1% Remaining to 3x"></div>
                </div>
              </div>
            </div>

            <!-- Hairline Sub-Stats -->
            <div class="card-divider-line grid grid-cols-2 gap-2 text-left pt-2">
              <div class="card-col-divider pr-1">
                <span class="submetric-label">Active Blocks</span>
                <span class="font-mono text-sm font-bold text-[var(--ink-text)]" id="hero-bp-blocks">534</span>
                <span class="font-mono text-[10px] text-[var(--color-positive)] block">98.7% Covered</span>
              </div>
              <div class="pl-1">
                <span class="submetric-label">Remaining Gap</span>
                <span class="font-mono text-sm font-bold text-[var(--color-bp)]" id="hero-bp-gap">1,075</span>
                <span class="font-mono text-[10px] text-[var(--ink-muted)] block">to 3x mandate</span>
              </div>
            </div>
          </div>

          <!-- Card 3: Demographic Split Card (Minority & Women/Youth) -->
          <div class="editorial-card-hero hero-subcard p-3.5 flex flex-col justify-between">
            <!-- Top Half: Minority Representation -->
            <div class="pb-2.5">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[11px] font-bold text-[var(--ink-text)]">
                  Minority <span class="font-hindi text-[11px] text-[var(--ink-muted)]">(अल्पसंख्यक)</span>
                </span>
                <span class="font-mono text-[10px] font-bold text-[var(--ink-text)] bg-[var(--surface-subtle)] px-1.5 py-0.2 rounded-[3px] border border-[var(--hairline)]" id="hero-minority-share">
                  7.4% Share
                </span>
              </div>
              <div class="flex items-baseline gap-2 mt-1">
                <h4 class="font-mono text-2xl font-bold text-[var(--ink-text)]" id="hero-minority-total">281</h4>
                <div class="text-[10px] font-mono text-[var(--ink-muted)] flex items-center gap-2">
                  <span>ZP: <strong class="text-[var(--color-zp)]" id="hero-zp-minority">275</strong> <span id="hero-zp-minority-pct">(8.4%)</span></span>
                  <span>BP: <strong class="text-[var(--color-bp)]" id="hero-bp-minority">6</strong> <span id="hero-bp-minority-pct">(1.1%)</span></span>
                </div>
              </div>
            </div>

            <!-- Hairline Divider -->
            <div class="border-t border-[var(--hairline)] pt-2.5">
              <div class="flex items-center justify-between">
                <span class="font-mono text-[11px] font-bold text-[var(--ink-text)]">
                  Women & Youth <span class="font-hindi text-[11px] text-[var(--ink-muted)]">(महिला / युवा)</span>
                </span>
                <span class="font-mono text-[10px] font-bold text-[var(--ink-text)] bg-[var(--surface-subtle)] px-1.5 py-0.2 rounded-[3px] border border-[var(--hairline)]" id="hero-diverse-share">
                  47.2% Diverse
                </span>
              </div>
              <div class="flex items-baseline gap-2 mt-1">
                <h4 class="font-mono text-2xl font-bold text-[var(--ink-text)]" id="hero-diverse-total">1,791</h4>
                <div class="text-[10px] font-mono text-[var(--ink-muted)] flex items-center gap-2">
                  <span>Mahila: <strong class="text-[var(--ink-text)]" id="hero-mahila-total">647</strong> <span id="hero-mahila-pct">(17.0%)</span></span>
                  <span>Yuva: <strong class="text-[var(--ink-text)]" id="hero-yuva-total">1,194</strong> <span id="hero-yuva-pct">(31.5%)</span></span>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- MAIN SECTION: 2-COLUMN WORKING GRID (Left 65% Analytics & Map | Right 35% Action List) -->
        <div class="grid grid-cols-1 xl:grid-cols-12 gap-4">

          <!-- LEFT 8 COLUMNS (~66% Width) -->
          <div class="xl:col-span-8 space-y-4">

            <!-- SECTION A: BIHAR DISTRICT COVERAGE MAP & ZERO-SEAT GAPS -->
            <div class="editorial-card p-4 space-y-3">
              <div class="flex items-center justify-between flex-wrap gap-2 pb-2 hairline-b">
                <div>
                  <h4 class="text-sm font-bold text-[var(--ink-text)]">Bihar District Coverage &amp; Zero-Seat Gaps</h4>
                  <p class="text-xs text-[var(--ink-muted)] font-mono">Interactive choropleth of 43 reporting units colored by status</p>
                </div>
                <!-- View Switcher Toggle -->
                <div class="pill-filter-group text-xs">
                  <button id="btn-view-map" onclick="switchMapDisplay('map')" class="pill-filter-btn pill-filter-btn-active">
                    🗺️ Map View
                  </button>
                  <button id="btn-view-table" onclick="switchMapDisplay('table')" class="pill-filter-btn">
                    📋 Ranked Table
                  </button>
                </div>
              </div>

              <!-- 1. MAP VIEW CONTAINER -->
              <div id="bihar-map-wrapper">
{map_snippet}
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
            </div>

            <!-- SECTION B: PENETRATION DEPTH & ZONE PROGRESS (2 Sub-Cards) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

              <!-- Subcard 1: ZP Candidate Depth Progression -->
              <div class="editorial-card p-4 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-mono text-xs font-bold text-[var(--color-zp)] uppercase tracking-wider">Candidate Depth</span>
                    <span class="font-mono text-[10px] text-[var(--ink-muted)]">1,160 Seats</span>
                  </div>
                  <h4 class="text-sm font-bold text-[var(--ink-text)]">Seat Penetration (≥1 to 5+ Candidates)</h4>
                </div>

                <div class="h-44 w-full my-2">
                  <canvas id="chart-hero-progression"></canvas>
                </div>

                <!-- Depth Progression Mono Legend Row -->
                <div class="flex items-center justify-between flex-wrap gap-1 text-[10px] font-mono text-[var(--ink-muted)] pt-2 border-t border-[var(--hairline)]">
                  <span>≥1: <strong class="text-[var(--color-zp)]" id="hero-zp-seat1-sub">1,120</strong></span>
                  <span>≥2: <strong class="text-[var(--color-zp)]" id="hero-zp-seat2">1,031</strong></span>
                  <span>≥3: <strong class="text-[var(--color-zp)]" id="hero-zp-seat3">640</strong></span>
                  <span>≥4: <strong class="text-[var(--color-zp)]" id="hero-zp-seat4">297</strong></span>
                  <span>5+: <strong class="text-[var(--color-zp)]" id="hero-zp-seat5">122</strong></span>
                </div>
              </div>

              <!-- Subcard 2: Zone Comparison (ZP vs BP Coverage) -->
              <div class="editorial-card p-4 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-mono text-xs font-bold text-[var(--color-bp)] uppercase tracking-wider">Zone Comparison</span>
                    <span class="font-mono text-[10px] text-[var(--ink-muted)]">12 Zones</span>
                  </div>
                  <h4 class="text-sm font-bold text-[var(--ink-text)]">ZP vs BP Progress Velocity</h4>
                </div>

                <div class="h-44 w-full my-2">
                  <canvas id="chart-hero-comparison"></canvas>
                </div>

                <!-- Strict 2-Data-Color Indicator -->
                <div class="flex items-center justify-center gap-6 text-[11px] font-mono text-[var(--ink-muted)] pt-2 border-t border-[var(--hairline)]">
                  <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-zp)]"></span> ZP Coverage</span>
                  <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-[2px] bg-[var(--color-bp)]"></span> BP Coverage</span>
                </div>
              </div>

            </div>

            <!-- SECTION C: DEMOGRAPHICS DONUT & PIPELINE SUMMARY -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

              <!-- ZP Demographics Donut (Showing 56.4% done & remaining gap) -->
              <div class="editorial-card p-4 flex flex-col justify-between">
                <div class="flex items-center justify-between">
                  <span class="font-mono text-xs font-bold text-[var(--ink-text)] uppercase">ZP Target Fulfillment</span>
                  <span class="font-mono text-xs text-[var(--color-zp)] font-bold">56.4% Achieved</span>
                </div>

                <div class="my-auto py-2 text-center">
                  <div class="w-28 h-28 mx-auto relative">
                    <canvas id="chart-hero-zp-donut"></canvas>
                    <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                      <span class="font-mono text-base font-bold text-[var(--ink-text)]">56%</span>
                      <span class="font-mono text-[8px] text-[var(--ink-muted)] uppercase">Coverage</span>
                    </div>
                  </div>
                </div>

                <div class="pt-2 border-t border-[var(--hairline)] flex items-center justify-between text-xs font-mono">
                  <div>
                    <span class="text-[var(--ink-muted)] block text-[10px] uppercase">Youth (Yuva)</span>
                    <strong class="text-[var(--color-bp)] font-bold text-sm" id="hero-zp-yuva">1,050</strong>
                  </div>
                  <div class="text-right">
                    <span class="text-[var(--ink-muted)] block text-[10px] uppercase">Women (Female)</span>
                    <strong class="text-[var(--color-zp)] font-bold text-sm" id="hero-zp-female">607</strong>
                  </div>
                </div>
              </div>

              <!-- Pipeline Semi-Donut (Total Identified Pipeline) -->
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
              </div>

            </div>

          </div>

          <!-- RIGHT 4 COLUMNS (~34% Width: Ranked Action List & Zone Summary) -->
          <div class="xl:col-span-4 space-y-4">

            <!-- RANKED EXECUTIVE ACTION LIST (No sparkles, no pastel AI boxes) -->
            <div class="editorial-card p-4 space-y-3">
              <div class="flex items-center justify-between pb-2 hairline-b">
                <div>
                  <h4 class="text-sm font-bold text-[var(--ink-text)] flex items-center gap-1.5">
                    Operational Action Items
                  </h4>
                  <p class="text-[11px] text-[var(--ink-muted)] font-mono">Ranked operational priorities from live audit</p>
                </div>
                <span class="font-mono text-[10px] font-bold text-[var(--color-alert)] bg-[var(--color-alert-subtle)] px-2 py-0.5 rounded-[4px] border border-[var(--color-alert)]">
                  4 Critical
                </span>
              </div>

              <!-- Ranked Action Items List -->
              <div class="space-y-1">

                <!-- Item 1: P0 Alert (Zero-Candidate Seats) -->
                <div class="action-item-row" onclick="navigateFromDrawer('zp', 'zp-district-wise'); setZpDistrictGapFilter(true)">
                  <div class="severity-dot dot-p0"></div>
                  <div class="flex-1 space-y-0.5">
                    <div class="flex items-center justify-between">
                      <span class="tag-p0">P0 CRITICAL</span>
                      <span class="font-mono text-[10px] text-[var(--color-alert)] font-bold">40 Seats</span>
                    </div>
                    <p class="text-xs text-[var(--ink-text)] leading-snug">
                      <strong>40 ZP seats have zero candidates</strong>: Purnia (12), Katihar (10), Patna Gramin (6), Khagaria (4), Madhepura (3), Araria (3).
                    </p>
                    <span class="text-[10px] font-mono text-[var(--color-alert)] font-semibold flex items-center gap-1 pt-0.5">
                      Inspect 40 Zero-Seats →
                    </span>
                  </div>
                </div>

                <!-- Item 2: P1 Capacity Gap (BP Multiplier Gap) -->
                <div class="action-item-row" onclick="navigateFromDrawer('bp', 'bp-progress')">
                  <div class="severity-dot dot-p1"></div>
                  <div class="flex-1 space-y-0.5">
                    <div class="flex items-center justify-between">
                      <span class="tag-p1">P1 GAP</span>
                      <span class="font-mono text-[10px] text-[var(--color-bp)] font-bold">1,075 Needed</span>
                    </div>
                    <p class="text-xs text-[var(--ink-text)] leading-snug">
                      <strong>1,075 Block Pramukh candidates pending</strong> to satisfy 3x multiplier across 534 blocks (527 identified of 1,602 target).
                    </p>
                    <span class="text-[10px] font-mono text-[var(--color-bp)] font-semibold flex items-center gap-1 pt-0.5">
                      Open BP Multiplier Pipeline →
                    </span>
                  </div>
                </div>

                <!-- Item 3: P2 Data Audit (Missing Contacts) -->
                <div class="action-item-row" onclick="filterZpByMissing('phone')">
                  <div class="severity-dot dot-p2"></div>
                  <div class="flex-1 space-y-0.5">
                    <div class="flex items-center justify-between">
                      <span class="tag-p2">P2 AUDIT</span>
                      <span class="font-mono text-[10px] text-[var(--color-zp)] font-bold">213 Records</span>
                    </div>
                    <p class="text-xs text-[var(--ink-text)] leading-snug">
                      <strong>213 candidate records lack valid contact phone numbers</strong>; 96 records lack recorded gender data.
                    </p>
                    <span class="text-[10px] font-mono text-[var(--color-zp)] font-semibold flex items-center gap-1 pt-0.5">
                      Review Incomplete Records →
                    </span>
                  </div>
                </div>

                <!-- Item 4: P3 Velocity (Performance Highlights) -->
                <div class="action-item-row" onclick="navigateFromDrawer('zones')">
                  <div class="severity-dot dot-p3"></div>
                  <div class="flex-1 space-y-0.5">
                    <div class="flex items-center justify-between">
                      <span class="font-mono text-[10px] font-bold text-[var(--color-positive)] uppercase">P3 HEALTH</span>
                      <span class="font-mono text-[10px] text-[var(--color-positive)] font-bold">80% Velocity</span>
                    </div>
                    <p class="text-xs text-[var(--ink-text)] leading-snug">
                      <strong>Magadh (80%) and Sahabad (72%)</strong> exceed target pace; Seemanchal and Patna require field coordination.
                    </p>
                    <span class="text-[10px] font-mono text-[var(--color-positive)] font-semibold flex items-center gap-1 pt-0.5">
                      View Zone Profiles →
                    </span>
                  </div>
                </div>

              </div>

              <!-- Quick Candidate / Seat Search Input -->
              <div class="relative pt-2">
                <input id="quick-intel-search" type="text" placeholder="Search candidate, seat or district..."
                  class="w-full text-xs py-2 pl-8 pr-8 rounded-[4px] bg-[var(--surface-subtle)] border border-[var(--hairline)] focus:outline-none focus:border-[var(--color-zp)] transition-all font-mono">
                <i data-lucide="search" class="w-3.5 h-3.5 text-[var(--ink-muted)] absolute left-2.5 top-4"></i>
                <i data-lucide="corner-down-left" class="w-3.5 h-3.5 text-[var(--ink-faint)] absolute right-2.5 top-4"></i>
              </div>
            </div>

            <!-- ZONE LEADERBOARD SUMMARY -->
            <div class="editorial-card p-4 space-y-3">
              <span class="font-mono text-xs font-bold text-[var(--ink-muted)] block uppercase tracking-wider">Top Zone Pace</span>
              <div class="space-y-2.5 text-xs font-mono">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-[var(--ink-text)]">Magadh Zone</span>
                    <span class="font-bold text-[var(--color-positive)]">80%</span>
                  </div>
                  <div class="w-full bg-[var(--surface-subtle)] border border-[var(--hairline)] rounded-[2px] h-1.5 overflow-hidden">
                    <div class="bg-[var(--color-positive)] h-1.5" style="width: 80%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-[var(--ink-text)]">Sahabad Zone</span>
                    <span class="font-bold text-[var(--color-zp)]">72%</span>
                  </div>
                  <div class="w-full bg-[var(--surface-subtle)] border border-[var(--hairline)] rounded-[2px] h-1.5 overflow-hidden">
                    <div class="bg-[var(--color-zp)] h-1.5" style="width: 72%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-[var(--ink-text)]">Champaran Zone</span>
                    <span class="font-bold text-[var(--color-zp)]">69%</span>
                  </div>
                  <div class="w-full bg-[var(--surface-subtle)] border border-[var(--hairline)] rounded-[2px] h-1.5 overflow-hidden">
                    <div class="bg-[var(--color-zp)] h-1.5" style="width: 69%"></div>
                  </div>
                </div>

                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="font-semibold text-[var(--ink-text)]">Mithilanchal Zone</span>
                    <span class="font-bold text-[var(--color-zp)]">64%</span>
                  </div>
                  <div class="w-full bg-[var(--surface-subtle)] border border-[var(--hairline)] rounded-[2px] h-1.5 overflow-hidden">
                    <div class="bg-[var(--color-zp)] h-1.5" style="width: 64%"></div>
                  </div>
                </div>
              </div>
            </div>

          </div>

        </div>

      </section>'''

# Replace <head>...</head>
updated_html = re.sub(r'<head>.*?</head>', head_replacement, orig_html, flags=re.DOTALL)

# Replace <header ...>...</header>
updated_html = re.sub(r'<header.*?</header>', header_new, updated_html, count=1, flags=re.DOTALL)

# Replace <section id="section-hero" ...>...</section>
updated_html = re.sub(r'<section id="section-hero".*?</section>', new_hero_section, updated_html, count=1, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Updated index.html with new editorial layout and Bihar choropleth map!")
