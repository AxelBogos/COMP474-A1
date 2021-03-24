import csv
from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF,RDFS,XSD,FOAF,OWL
import os
from os import path
import pandas as pd

DBR = Namespace("http://dbpedia.org/resource/")
SCH = Namespace("http://a1.io/schema#")
DAT = Namespace("http://a1.io/data#")
TEACH = Namespace("http://linkedscience.org/teach/ns#")

REGEN_CLEAN_CATALOG = False

special_courses = [URIRef("http://a1.io/data#COMP353"),URIRef("http://a1.io/data#COMP474")]

def populate_knowledge_base():

    g = Graph()
    g.parse('A1.ttl', format='turtle')

    # Add our university to the KB using the pre-defined schema
    # TODO it says we should have a link to the university's DBPEDIA entry,
    #  so maybe we are not supposed to use the dbp entry as our key?
    g.add((DBR.Concordia_University, RDF.type, SCH.University))

    with open('CLEAN_CATALOG.csv','r') as data:
        r = csv.DictReader(data)
        for row in r:
            #Create the course
            cn = URIRef("http://a1.io/data#"+row['Course code']+row['Course number'])
            # TODO the CID in catalog doesnt seem to mean much intuitively. I think it should be cn everywhere
            cid = URIRef("http://a1.io/data#"+row['Key'])
            g.add((cn, RDF.type, SCH.Course))

            # Add to list of offered courses at Concordia
            g.add((DBR.Concordia_University, SCH.Offers, cn))

            #Add course deets
            g.add((cn, TEACH.courseTitle, Literal(row['Title'])))
            g.add((cn, SCH.HasSubject, Literal(row['Course code'])))
            g.add((cn, SCH.CourseNumber, Literal(row['Course number'])))
            g.add((cn, TEACH.courseDescription, Literal(row['Description'])))
            # TODO: Consider manually populating the description ^^ for these 2 courses. The dataset we have is gross
            g.add((cn, RDFS.seeAlso, Literal(row['Website'])))

            if cn in special_courses:
                for i in range(1,12):

                    # Add Lectures
                    lec_id = URIRef("http://a1.io/data#" + "{}{}Lec{}".format(row['Course code'],row['Course number'],i))
                    g.add((cn, SCH.HasLecture, lec_id))
                    g.add((lec_id,RDF.type,SCH.Lecture))
                    g.add((lec_id, SCH.LectureNumber, Literal(i)))

                    # Add Labs
                    lab_id = URIRef("http://a1.io/data#" + "{}{}Lab{}".format(row['Course code'], row['Course number'], i))
                    g.add((lab_id, RDF.type, SCH.Lab))
                    g.add((lab_id,SCH.RelatedToLecture,lec_id))

                    # Add Tutorials
                    tut_id = URIRef("http://a1.io/data#" + "{}{}Tut{}".format(row['Course code'], row['Course number'], i))
                    g.add((tut_id, RDF.type, SCH.Tutorial))
                    g.add((tut_id,SCH.RelatedToLecture,lec_id))

                    # Add Topics TODO: will be manual i think?

                # Add content
                dir_name = "c{}content".format(row['Course number'])
                for sub_dir in ['Readings', 'Slides', 'Worksheet', 'Other']:
                    dir_path = os.path.join(dir_name, sub_dir)
                    if os.path.isdir(dir_path):
                        for idf, f in enumerate(sorted(os.listdir(dir_path))):
                            f_uri = URIRef("http://a1.io/data#" + path.join(dir_path,f))
                            lec_id = URIRef("http://a1.io/data#" + "{}{}Lec{}".format(row['Course code'], row['Course number'], idf+1))
                            g.add((f_uri, RDF.type, SCH+sub_dir))
                            g.add((lec_id, SCH.HasMaterial,f_uri))

                # Add outline TODO



# TODO: Manually add topics and materials to satisfy the competency questions
# TODO/ASK: What does "give each item an automatically generated URI" mean?
# TODO: Add all the materials. literally all of it
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


def regenerate_catalog():
    """
    Function to wrangle and clean data used in the KB construction. A bit bare bone for now.
    Creates a new .csv file CLEAN_CATALOG.csv  in the current dir.
    :return: void
    """
    catalog = pd.read_csv('CATALOG.csv')

    catalog = catalog.dropna(subset=['Course code', 'Course number']) #remove empty course codes and course names
    catalog.to_csv('CLEAN_CATALOG.csv', index=False)

if __name__ == '__main__':
    if REGEN_CLEAN_CATALOG:
        regenerate_catalog()
    populate_knowledge_base()
