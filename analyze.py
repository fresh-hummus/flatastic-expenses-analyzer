#!/usr/bin/python3

import csv
import sys
import ruamel.yaml as yaml

INDEX_PRICE   = 4
INDEX_PAID_BY = 5
INDEX_SHARERS = 7

csv_reader = csv.reader(sys.stdin)
next(csv_reader)

expenses = [{
  'person': row[INDEX_PAID_BY],
  'price_per_sharer': float(row[INDEX_PRICE]) / len(row[INDEX_SHARERS].split(', ')),
  'paid_for': set(row[INDEX_SHARERS].split(', ')),
} for row in csv_reader ]

results = {}

for expense in expenses:

  person = expense['person']
  price_per_sharer = expense['price_per_sharer']

  expense['paid_for'].discard(person)

  results.setdefault(person, { 'paid_for': dict(), 'owes_to': dict(), 'gets_from': dict()})

  for paid_for_person in expense['paid_for']:
    results.setdefault(paid_for_person, { 'paid_for': dict(), 'owes_to': dict(), 'gets_from': dict()})
    
    results[person]['paid_for'].setdefault(paid_for_person, 0) 
    results[person]['paid_for'][paid_for_person] += price_per_sharer

    results[person]['gets_from'].setdefault(paid_for_person, 0)
    results[person]['gets_from'][paid_for_person] += price_per_sharer

    results[paid_for_person]['gets_from'].setdefault(person, 0)
    results[paid_for_person]['gets_from'][person] -= price_per_sharer

    results[person]['owes_to'].setdefault(paid_for_person, 0)
    results[person]['owes_to'][paid_for_person] -= price_per_sharer

    results[paid_for_person]['owes_to'].setdefault(person, 0)
    results[paid_for_person]['owes_to'][person] += price_per_sharer

    # print(f"{paid_by} paid {price_per_sharer:0.2f} EUR for {sharer}")

def process_entries(entries):
  return { person: f"{price:0.2f}"
    for person, price
    in entries.items()
    if price > 0
  }

def process_analysis(analysis):
  return {
    category: process_entries(entries)
    for category, entries
    in analysis.items()
  }

results = {
  person: process_analysis(analysis)
  for person, analysis
  in results.items()
}

output = yaml.dump(results)
print(output.replace("'", ""))