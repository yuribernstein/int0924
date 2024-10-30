import csv

with open('majestic_million.csv', 'r') as csvfile, open('domains.txt', 'w') as outfile:
    reader = csv.reader(csvfile)
    next(reader)
    
    for row in reader:
        domain = row[2]
        outfile.write(domain + '\n')
