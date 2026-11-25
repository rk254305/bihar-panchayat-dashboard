with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update body class to use var(--bg-page) and var(--ink-text)
html = html.replace(
    '<body class="bg-[#f1f4f9] text-slate-800 antialiased selection:bg-blue-100 selection:text-blue-900">',
    '<body class="bg-[var(--bg-page)] text-[var(--ink-text)] antialiased selection:bg-[#26407A] selection:text-white">'
)

# 2. Refine sidebar container
old_sidebar_header = '''    <aside id="app-drawer"
      class="fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-[#e8ecf2] p-5 shadow-2xl transition-transform duration-300 transform -translate-x-full lg:translate-x-0 lg:static lg:z-auto lg:shadow-[0_18px_40px_-4px_rgba(15,23,42,0.08),0_8px_16px_-2px_rgba(15,23,42,0.04)] lg:rounded-2xl lg:border lg:border-black/[0.04] flex flex-col justify-between shrink-0 lg:sticky lg:top-5 lg:h-[calc(100vh-2.5rem)]">'''

new_sidebar_header = '''    <aside id="app-drawer"
      class="fixed inset-y-0 left-0 z-50 w-64 bg-[var(--surface-card)] border-r border-[var(--hairline)] p-3.5 transition-transform duration-200 transform -translate-x-full lg:translate-x-0 lg:static lg:z-auto lg:rounded-[6px] lg:border lg:border-[var(--hairline)] flex flex-col justify-between shrink-0 lg:sticky lg:top-4 lg:h-[calc(100vh-2rem)]">'''

html = html.replace(old_sidebar_header, new_sidebar_header)

# 3. Clean up the sidebar header and borders
html = html.replace('border-b border-slate-100 shrink-0', 'hairline-b pb-2.5 shrink-0')
html = html.replace('pt-3 border-t border-slate-100', 'pt-2.5 hairline-t')
html = html.replace('bg-blue-600 flex items-center justify-center text-white shadow-sm', 'bg-[var(--color-zp)] flex items-center justify-center text-white')
html = html.replace('text-blue-600', 'text-[var(--color-zp)]')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Refined sidebar and document body in index.html!")
