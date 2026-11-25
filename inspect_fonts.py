import re

with open('index.html', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'class="[^"]*font-mono[^"]*text-[0-9a-z]+[^"]*"', text)
print(f'Found {len(matches)} font-mono class usages in index.html:')
for m in matches[:15]:
    print(' ', m)
