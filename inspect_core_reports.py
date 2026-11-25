import json
import csv

def inspect_csv(path, num_rows=10):
    print(f"\n==================== {path} ====================")
    with open(path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
    print(f"Total rows: {len(reader)}, cols: {len(reader[0]) if reader else 0}")
    for i in range(min(num_rows, len(reader))):
        print(f"Row {i:2d}: {reader[i]}")

inspect_csv('data/csv/District Wise Report ZP.csv', 8)
inspect_csv('data/csv/District Wise Report BP.csv', 8)
inspect_csv('data/csv/Progress Report ZP.csv', 12)
inspect_csv('data/csv/Progress Report BP.csv', 12)
inspect_csv('data/csv/Bifurcation Report ZP.csv', 6)
inspect_csv('data/csv/Bifurcation Report BP.csv', 6)
