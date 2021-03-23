import csv
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF,RDFS,XSD,FOAF,OWL

DBR = Namespace("http://dbpedia.org/resource/")
SCH = Namespace("http://a1.io/schema#")
DAT = Namespace("http://a1.io/data#")

g = Graph()
g.parse('A1.ttl', format='turtle')

#Independent triples
g.add((DAT.Concordia, RDF.type, SCH.University))

with open('/Users/welton/remoteproj/copy.csv','r') as data:
    r = csv.DictReader(data)
    for row in r:
        if row['Course code'] == 'COMP' and row['Course number'] in ['474','353']:
            #Create the course
            cn = URIRef("http://a1.io/data#"+row['Course code']+row['Course number'])
            g.add((cn, RDF.type, SCH.Course))
            g.add((DAT.Concordia, SCH.Offers, cn))

            #Add course deets
            # g.add((cn, SCH.CourseName, Literal(row['Title'])))
            g.add((cn, SCH.CourseSubject, Literal(row['Course code'])))
            g.add((cn, SCH.CourseNumber, Literal(row['Course number'])))
            # g.add((cn, SCH.CourseDescription, Literal(row['Description'])))
            # g.add((cn, SCH.CourseWebsite, Literal(row['Website'])))

            # g.add((cn, SCH.Outline, someURIToContent)))
            

        


print(g.serialize(format="turtle").decode("utf-8"))