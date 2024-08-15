import csv
with open('tr_test_cases.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    sections = []
    for row in reader:
        sections.append(row['Section'])
    
    for section in set(sections):
        print(f'{section}:\n')
        for row in reader:
            print(row['Title'] if row['Section'] == section else '')