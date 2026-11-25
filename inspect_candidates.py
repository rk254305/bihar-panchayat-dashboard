import csv

def inspect_candidates(path, n=6):
    print(f"\n==================== {path} ====================")
    with open(path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    clean_rows = [r for r in reader if any(c.strip() for c in r)]
    print(f"Non-empty rows: {len(clean_rows)}")
    for i in range(min(n, len(clean_rows))):
        print(f"Row {i:2d}: {clean_rows[i][:15]}")

inspect_candidates('data/csv/Final Candidate List.csv', 4)
inspect_candidates('data/csv/Block Pramukh.csv', 4)
