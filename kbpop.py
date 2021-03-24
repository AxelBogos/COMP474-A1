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
g.add((DAT.Concordia, RDFS.seeAlso, URIRef("http://dbpedia.org/resource/Concordia_University")))

with open('CATALOG.csv','r') as data:
    r = csv.DictReader(data)
    for row in r:
        #Create the course
        cn = URIRef("http://a1.io/data#"+row['Course code']+row['Course number'])
        g.add((URIRef("http://a1.io/data#"+row['Key']), RDF.type, SCH.Course))
        g.add((DAT.Concordia, SCH.Offers, cn))

        #Add course deets
        # g.add((cn, SCH.CourseName, Literal(row['Title'])))
        g.add((cn, SCH.CourseSubject, Literal(row['Course code'])))
        g.add((cn, SCH.CourseNumber, Literal(row['Course number'])))
        # g.add((cn, SCH.CourseDescription, Literal(row['Description'])))
        g.add((cn, SCH.CourseWebsite, Literal(row['Website'])))
        # g.add((cn, SCH.Outline, someURIToContent)))
        # for i in range(1,12):
            # TODO add a whole bunch of lectures for each class since there are 12 weeks of class (could also potentially add nested labs and tutorials to each lecture if need be)
            # g.add(())
                

# TODO: Manually add topics and materials to satisfy the competency questions
# TODO/ASK: What does "give each item an automatically generated URI" mean? 
# TODO: Add all the materials. literally alllll of it
    # c474 course topics
        # Introduction to Intel Systems  (slides01)
        # Knowledge Graphs               (slides02,worksheet01)
        # Vocabularies & Ontologies      (slides03,worksheet02)
    # c353 course topics
        # Introduction to Databases      (DB1)
        # Basic SQL                      (DB1)
        # ER Diagrams and Models         (DB2)
        # Relation Data Model            (DB3)

g.serialize(destination="out/kb_test2.ttl",format="turtle")


