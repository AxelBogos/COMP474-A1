import csv
from rdflib import URIRef, BNode, Literal

with open('/Users/welton/remoteproj/copy.csv','r') as data:
    r = csv.DictReader(data)
    for row in r:
        if row['Course code'] == 'COMP' and row['Course number'] in ['474','353']:
            print(row)
