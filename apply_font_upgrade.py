with open('index.html', encoding='utf-8') as f:
    html = f.read()

replacements = [
    (
        'class="font-mono text-5xl sm:text-6xl font-bold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified"',
        'class="font-display text-5xl sm:text-6xl font-extrabold tracking-tight text-[var(--color-zp)]" id="hero-zp-identified"'
    ),
    (
        'class="font-mono text-5xl sm:text-6xl font-bold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified"',
        'class="font-display text-5xl sm:text-6xl font-extrabold tracking-tight text-[var(--color-bp)]" id="hero-bp-identified"'
    ),
    (
        'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-zp)]" id="hero-mahila-total"',
        'class="font-display text-4xl sm:text-5xl font-extrabold text-[var(--color-zp)]" id="hero-mahila-total"'
    ),
    (
        'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-bp)]" id="hero-bp-female"',
        'class="font-display text-4xl sm:text-5xl font-extrabold text-[var(--color-bp)]" id="hero-bp-female"'
    ),
    (
        'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-zp)]" id="hero-zp-minority"',
        'class="font-display text-4xl sm:text-5xl font-extrabold text-[var(--color-zp)]" id="hero-zp-minority"'
    ),
    (
        'class="font-mono text-4xl sm:text-5xl font-bold text-[var(--color-bp)]" id="hero-bp-minority"',
        'class="font-display text-4xl sm:text-5xl font-extrabold text-[var(--color-bp)]" id="hero-bp-minority"'
    ),
    (
        'class="font-mono text-2xl sm:text-3xl font-bold text-[var(--ink-text)]" id="inspect-district-name"',
        'class="font-display text-2xl sm:text-3xl font-extrabold text-[var(--ink-text)]" id="inspect-district-name"'
    ),
    (
        'id="page-main-title" class="text-2xl sm:text-3xl font-bold font-sans text-[var(--ink-text)] tracking-tight"',
        'id="page-main-title" class="text-2xl sm:text-3xl font-extrabold font-display text-[var(--ink-text)] tracking-tight"'
    )
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        print(f"Replaced: {old[:50]}...")
    else:
        print(f"NOT FOUND: {old[:50]}...")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html upgraded with Outfit font-display for numbers & titles!")
