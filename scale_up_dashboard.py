import re

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Sidebar width & padding
html = html.replace(
    'class="fixed inset-y-0 left-0 z-50 w-64 bg-[var(--surface-card)] border-r border-[var(--hairline)] p-3.5',
    'class="fixed inset-y-0 left-0 z-50 w-72 lg:w-76 xl:w-80 bg-[var(--surface-card)] border-r border-[var(--hairline)] p-4 sm:p-5'
)

# 2. Main title
html = html.replace(
    'id="page-main-title" class="text-xl sm:text-2xl font-bold font-sans',
    'id="page-main-title" class="text-2xl sm:text-3xl font-bold font-sans'
)

# 3. Subheader
html = html.replace(
    '<h3 class="text-base font-bold text-[var(--ink-text)] tracking-tight">Bihar Panchayat 2026 Nominations</h3>',
    '<h3 class="text-lg sm:text-xl font-bold text-[var(--ink-text)] tracking-tight">Bihar Panchayat 2026 Nominations</h3>'
)
html = html.replace(
    '<p class="text-xs text-[var(--ink-muted)] font-mono mt-0.5">38 Revenue Districts • 43 Reporting Units • 12 Administrative Zones</p>',
    '<p class="text-xs sm:text-sm text-[var(--ink-muted)] font-mono mt-0.5">38 Revenue Districts • 43 Reporting Units • 12 Administrative Zones</p>'
)

# 4. Hero KPI cards padding & numbers
html = html.replace(
    'editorial-card-hero hero-zp-dominant p-4 flex flex-col justify-between',
    'editorial-card-hero hero-zp-dominant p-5 sm:p-6 flex flex-col justify-between'
)
html = html.replace(
    'editorial-card-hero hero-bp-card p-4 flex flex-col justify-between',
    'editorial-card-hero hero-bp-card p-5 sm:p-6 flex flex-col justify-between'
)
html = html.replace(
    'class="font-mono text-5xl font-bold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified"',
    'class="font-mono text-5xl sm:text-6xl font-bold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified"'
)
html = html.replace(
    'class="font-mono text-5xl font-bold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified"',
    'class="font-mono text-5xl sm:text-6xl font-bold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified"'
)

# Progress bars in hero cards
html = html.replace(
    'class="gap-progress-bar"',
    'class="gap-progress-bar h-3.5"'
)

# Hero submetrics
html = html.replace(
    '<strong class="text-[var(--color-zp)] text-sm" id="hero-zp-seat1">1,120</strong>',
    '<strong class="text-[var(--color-zp)] text-base sm:text-lg" id="hero-zp-seat1">1,120</strong>'
)
html = html.replace(
    '<strong class="text-[var(--color-alert)] text-sm">40</strong>',
    '<strong class="text-[var(--color-alert)] text-base sm:text-lg">40</strong>'
)
html = html.replace(
    '<strong class="text-[var(--ink-text)] text-sm" id="hero-bp-blocks">534</strong>',
    '<strong class="text-[var(--ink-text)] text-base sm:text-lg" id="hero-bp-blocks">534</strong>'
)
html = html.replace(
    '<strong class="text-[var(--color-bp)] text-sm">1,075</strong>',
    '<strong class="text-[var(--color-bp)] text-base sm:text-lg">1,075</strong>'
)

# 5. Inclusion cards (Row 2)
html = html.replace(
    'editorial-card p-3.5 flex flex-col justify-between border-t-2',
    'editorial-card p-4 sm:p-5 flex flex-col justify-between border-t-2'
)
html = html.replace(
    'class="font-mono text-3xl font-bold text-[var(--color-zp)]" id="hero-mahila-total"',
    'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-zp)]" id="hero-mahila-total"'
)
html = html.replace(
    'class="font-mono text-3xl font-bold text-[var(--color-bp)]" id="hero-bp-female"',
    'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-bp)]" id="hero-bp-female"'
)
html = html.replace(
    'class="font-mono text-3xl font-bold text-[var(--color-zp)]" id="hero-zp-minority"',
    'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-zp)]" id="hero-zp-minority"'
)
html = html.replace(
    'class="font-mono text-3xl font-bold text-[var(--color-bp)]" id="hero-bp-minority"',
    'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-bp)]" id="hero-bp-minority"'
)

# Subtitle labels in inclusion cards
html = html.replace(
    'class="text-[11px] text-[var(--ink-muted)]">Women candidates identified',
    'class="text-xs sm:text-sm text-[var(--ink-muted)]">Women candidates identified'
)
html = html.replace(
    'class="text-[11px] text-[var(--ink-muted)]">Women Pramukh candidates identified',
    'class="text-xs sm:text-sm text-[var(--ink-muted)]">Women Pramukh candidates identified'
)
html = html.replace(
    'class="text-[11px] text-[var(--ink-muted)]">Minority candidates active',
    'class="text-xs sm:text-sm text-[var(--ink-muted)]">Minority candidates active'
)
html = html.replace(
    'class="text-[11px] text-[var(--ink-muted)]">Significant inclusion gap',
    'class="text-xs sm:text-sm text-[var(--ink-muted)]">Significant inclusion gap'
)

# 6. Youth strip
html = html.replace(
    'editorial-card p-3 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-[var(--surface-subtle)]',
    'editorial-card p-4 sm:p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 bg-[var(--surface-subtle)]'
)
html = html.replace(
    'ZP Youth: <strong class="text-[var(--color-zp)] text-sm" id="hero-yuva-total">1,050</strong>',
    'ZP Youth: <strong class="text-[var(--color-zp)] text-base sm:text-lg" id="hero-yuva-total">1,050</strong>'
)
html = html.replace(
    'BP Youth: <strong class="text-[var(--color-bp)] text-sm" id="hero-bp-yuva">144</strong>',
    'BP Youth: <strong class="text-[var(--color-bp)] text-base sm:text-lg" id="hero-bp-yuva">144</strong>'
)

# 7. District Inspector Card below map
html = html.replace(
    'district-inspector-card p-3.5 border border-[var(--hairline)]',
    'district-inspector-card p-4 sm:p-5 border border-[var(--hairline)]'
)
html = html.replace(
    'class="font-mono text-base font-bold text-[var(--ink-text)]" id="inspect-district-name"',
    'class="font-mono text-2xl sm:text-3xl font-bold text-[var(--ink-text)]" id="inspect-district-name"'
)
html = html.replace(
    '<strong class="text-[var(--ink-text)] text-sm" id="inspect-zp-identified">',
    '<strong class="text-[var(--ink-text)] text-base sm:text-lg" id="inspect-zp-identified">'
)
html = html.replace(
    '<strong class="text-[var(--ink-text)] text-sm" id="inspect-zp-seats">',
    '<strong class="text-[var(--ink-text)] text-base sm:text-lg" id="inspect-zp-seats">'
)
html = html.replace(
    '<strong class="text-[var(--color-alert)] text-sm" id="inspect-zp-gap1">',
    '<strong class="text-[var(--color-alert)] text-base sm:text-lg" id="inspect-zp-gap1">'
)
html = html.replace(
    '<strong class="text-[var(--ink-text)] text-sm" id="inspect-bp-identified">',
    '<strong class="text-[var(--ink-text)] text-base sm:text-lg" id="inspect-bp-identified">'
)
html = html.replace(
    '<strong class="text-[var(--ink-text)] text-sm" id="inspect-bp-blocks">',
    '<strong class="text-[var(--ink-text)] text-base sm:text-lg" id="inspect-bp-blocks">'
)

# 8. Operational Action Items
html = html.replace(
    '<h4 class="text-sm font-bold text-[var(--ink-text)]">',
    '<h4 class="text-base sm:text-lg font-bold text-[var(--ink-text)]">'
)
html = html.replace(
    'class="w-full text-xs py-2 pl-8 pr-8 rounded-[4px]',
    'class="w-full text-sm py-2.5 pl-9 pr-9 rounded-[4px]'
)

# 9. Candidate Depth & Zone velocity cards
html = html.replace(
    '<span class="submetric-val block" id="donut-zp-pct">56%</span>',
    '<span class="font-mono text-2xl sm:text-3xl font-bold text-[var(--color-zp)] block" id="donut-zp-pct">56%</span>'
)
html = html.replace(
    '<span class="submetric-val block" id="donut-bp-pct">33%</span>',
    '<span class="font-mono text-2xl sm:text-3xl font-bold text-[var(--color-bp)] block" id="donut-bp-pct">33%</span>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html typography and card sizing scaled up successfully!")
