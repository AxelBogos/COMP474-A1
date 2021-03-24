import csv
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF,RDFS,XSD,FOAF,OWL

DBR = Namespace("http://dbpedia.org/resource/")
SCH = Namespace("http://a1.io/schema#")
DAT = Namespace("http://a1.io/data#")
TEACH = Namespace("http://linkedscience.org/teach/ns#")

g = Graph()
g.parse('A1.ttl', format='turtle')

#Connect the ConU dbpedia resource to our university object, auxiliary information already connected via dbr
g.add((DBR.Concordia_University, RDF.type, SCH.University))

with open('CATALOG.csv','r') as data:
    r = csv.DictReader(data)
    for row in r:
        #Create the course
        cn = URIRef("http://a1.io/data#"+row['Course code']+row['Course number'])
        cid = URIRef("http://a1.io/data#"+row['Key'])
        g.add((cid, RDF.type, SCH.Course))

        # Add to list of offered courses at Concordia
        g.add((DBR.Concordia_University, SCH.Offers, cid))

        #Add course deets
        g.add((cid, TEACH.courseTitle, Literal(row['Title'])))
        g.add((cid, SCH.HasSubject, Literal(row['Course code'])))
        g.add((cid, SCH.CourseNumber, Literal(row['Course number'])))
        g.add((cid, TEACH.courseDescription, Literal(row['Description'])))
        # TODO: Consider manually populating the description ^^ for these 2 courses. The dataset we have is gross
        g.add((cid, RDFS.seeAlso, Literal(row['Website'])))
        # TODO: add the outline to the course

        # Iteratively give each course 12 lectures
        # TODO: wtf is going on here? materials, etc
        for i in range(1,12):
            # Add lecture (http://a1.io/data#GCS_147l1)
            lid = URIRef("http://a1.io/data#" + row['Key'] + "l" + i)
            g.add((lid, RDF.type, SCH.Lecture))
            # Add lecture name
            # g.add((lid, SCH.Lecturename, .........))
            courseNumber = "someShit"
            # Add lecture slide set (slide set)
            ss = URIRef("c" + courseNumber + "content/slides/" + i + ".pdf" )
            # g.add((, RDF.type, SCH.Slides))
            # g.add((lid, TEACH.hasCourseMaterial, .........))
            
            # Add lecture readings
            # g.add((lid,TEACH.reading, .........))

            # Add other lecture materials
            # Add lecture topic (1 for now)
                # from a list[]
            # Add a lab and tutorial to each lecture
                # Add a resource for each event   


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

g.serialize(destination="out/kb_test.ttl", format="turtle")
