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
  paid_by   = csvrow[5]
  sharers = set(csvrow[7].split(', '))
  price_per_sharer = float(csvrow[4]) / len(sharers)

  sharers.discard(paid_by)

  return {
    'paid_by': paid_by,
    'price_per_sharer': price_per_sharer,
    'paid_for': sharers
  }

def add_num_to_dict(dict_obj, key, value):
  dict_obj.setdefault(key, 0)
  dict_obj[key] += value

def add_expense_to_results(expense, results):
  paid_by = expense['paid_by']
  price = expense['price_per_sharer']

  results.setdefault(paid_by, empty_analysis())

  for paid_for in expense['paid_for']:
    results.setdefault(paid_for, empty_analysis())
    
    add_num_to_dict(results[paid_by]['paid_for'],   paid_for,  price)
    add_num_to_dict(results[paid_by]['gets_from'],  paid_for,  price)
    add_num_to_dict(results[paid_by]['owes_to'],    paid_for, -price)
    add_num_to_dict(results[paid_for]['gets_from'], paid_by,  -price)
    add_num_to_dict(results[paid_for]['owes_to'],   paid_by,   price)

def pretty_analysis(analysis):
  return {
    category: {
      person: f"{price:0.2f}"
      for person, price
      in entries.items()
      if price > 0
    }
    for category, entries
    in analysis.items()
  }

csv_reader = csv.reader(sys.stdin)
next(csv_reader)

expenses = [ expense_from_row(row) for row in csv_reader ]
results = {}

for expense in expenses:
  add_expense_to_results(expense, results)

results_pretty = {
  person: pretty_analysis(analysis)
  for person, analysis
  in results.items()
}

output = yaml.dump(results_pretty)
print(output.replace("'", ""))
