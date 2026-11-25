import csv

def print_cols(path):
    print(f"\nCols for {path}:")
    with open(path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    clean = [r for r in reader if any(c.strip() for c in r)]
    headers = clean[1]
    for i, h in enumerate(headers):
        print(f"  Col {i}: {h}")

print_cols('data/csv/Final Candidate List.csv')
print_cols('data/csv/Block Pramukh.csv')
