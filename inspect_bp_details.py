import csv

def inspect(name):
    print(f"\n--- {name} ---")
    with open(f'data/csv/{name}', 'r', encoding='utf-8') as f:
        rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    for idx, r in enumerate(rows):
        non_empty = [f"{i}:{c}" for i, c in enumerate(r) if c.strip()]
        if len(non_empty) > 0 and idx < 25:
            print(f"Row {idx:2d}: {' | '.join(non_empty)}")

inspect('District Wise Report BP.csv')
inspect('Progress Report BP.csv')
inspect('Progress Report ZP.csv')
