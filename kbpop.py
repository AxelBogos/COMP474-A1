import csv
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF,RDFS,XSD,FOAF,OWL

DBR = Namespace("http://dbpedia.org/resource/")



g = Graph()
g.parse('COMP474-A1/A1.ttl', format='turtle')

for s,p,o in g:
    print(s,p,o)



with open('/Users/welton/remoteproj/copy.csv','r') as data:
    r = csv.DictReader(data)
    for row in r:
        if row['Course code'] == 'COMP' and row['Course number'] in ['474','353']:
            print(row)



