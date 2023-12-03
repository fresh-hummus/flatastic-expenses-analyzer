#!/usr/bin/python3

import csv
import sys
import ruamel.yaml as yaml

def empty_analysis():
  return {
    'paid_for': dict(),
    'owes_to': dict(),
    'gets_from': dict()
  }

def expense_from_row(csvrow):
  price   = csvrow[4]
  paid_by = csvrow[5]
  sharers = csvrow[7]

  return {
    'person': paid_by,
    'price_per_sharer': float(price) / len(sharers.split(', ')),
    'paid_for': set(sharers.split(', '))
  }

def add_num_to_dict(dict_obj, key, value):
  dict_obj.setdefault(key, 0)
  dict_obj[key] += value

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

def add_expense_to_results(expense, results):
  person = expense['person']
  price_per_sharer = expense['price_per_sharer']

  expense['paid_for'].discard(person)

  results.setdefault(person, empty_analysis())

  for paid_for_person in expense['paid_for']:
    results.setdefault(paid_for_person, empty_analysis())
    
    add_num_to_dict(results[person]['paid_for'],  paid_for_person,  price_per_sharer)
    add_num_to_dict(results[person]['gets_from'], paid_for_person,  price_per_sharer)
    add_num_to_dict(results[person]['owes_to'],   paid_for_person, -price_per_sharer)
    add_num_to_dict(results[paid_for_person]['gets_from'], person, -price_per_sharer)
    add_num_to_dict(results[paid_for_person]['owes_to'],   person,  price_per_sharer)

    # print(f"{paid_by} paid {price_per_sharer:0.2f} EUR for {sharer}")

csv_reader = csv.reader(sys.stdin)
next(csv_reader)

expenses = [ expense_from_row(row) for row in csv_reader ]
results = {}

for expense in expenses:
  add_expense_to_results(expense, results)

results_pretty = {
  person: process_analysis(analysis)
  for person, analysis
  in results.items()
}

output = yaml.dump(results_pretty)
print(output.replace("'", ""))
