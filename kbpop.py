import csv
import os
from os import path

import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS

DBR = Namespace("http://dbpedia.org/resource/")
DBP = Namespace("http://dbpedia.org/property/")
SCH = Namespace("http://a1.io/schema#")
DAT = Namespace("http://a1.io/data#")
TEACH = Namespace("http://linkedscience.org/teach/ns#")
ORG = Namespace("http://rdf.muninn-project.org/ontologies/organization#")

REGEN_CLEAN_CATALOG = False

special_courses = [URIRef("http://a1.io/data#COMP353"), URIRef("http://a1.io/data#COMP474")]

# All topics are dbpedia resources
topics_353 = ['Database', 'Entity–relationship_model', 'Relational_database',
              'Armstrong%27s_axioms', 'Armstrong%27s_axioms', 'Database_normalization',
              'Relational_algebra', 'SQL', 'SQL', 'SQL', 'Datalog', 'Object_Definition_Language']

topics_474 = ['Intelligent_system', 'Knowledge_graph', 'Ontology_(information_science)',
              'SPARQL', 'Knowledge_base', 'Recommender_system', 'Machine_learning',
              'Intelligent_agent', 'Text_mining']


def populate_knowledge_base():
    g = Graph()
    g.parse('A1.ttl', format='turtle')

    # Add our university to the KB using the pre-defined schema
    g.add((DAT.Concordia_University, RDF.type, SCH.University))
    g.add((DAT.Concordia_University, ORG.name, Literal("Concordia University")))
    g.add((DAT.Concordia_University, RDFS.seeAlso, DBR.Concordia_University))
    with open('CLEAN_CATALOG.csv', 'r') as data:
        r = csv.DictReader(data)
        for row in r:
            # Create the course
            cn = URIRef("http://a1.io/data#" + row['Course code'] + row['Course number'])
            g.add((cn, RDF.type, SCH.Course))

            # Add to list of offered courses at Concordia
            g.add((DBR.Concordia_University, SCH.Offers, cn))

            # Add course details
            g.add((cn, TEACH.courseTitle, Literal(row['Title'])))
            g.add((cn, SCH.HasSubject, Literal(row['Course code'])))
            g.add((cn, SCH.CourseNumber, Literal(row['Course number'])))
            g.add((cn, TEACH.courseDescription, Literal(row['Description'])))
            g.add((cn, RDFS.seeAlso, Literal(row['Website'])))

            if cn in special_courses:
                if row['Course number'] == '353':
                    lecture_number = 13
                else:
                    lecture_number = 10

                for i in range(1, lecture_number):
                    # Add Lectures
                    lec_id = DAT["{}{}Lec{}".format(row['Course code'], row['Course number'], i)]
                    g.add((cn, SCH.HasLecture, lec_id))
                    g.add((lec_id, RDF.type, SCH.Lecture))
                    g.add((lec_id, SCH.LectureNumber, Literal(i)))

                    # Add topics & Lecture Name
                    if row['Course number'] == '353':
                        g.add((lec_id, DBP.subject, DBR[topics_353[i - 1]]))
                        g.add((lec_id, TEACH.hasTitle, Literal(topics_353[i - 1])))
                    else:
                        g.add((lec_id, DBP.subject, DBR[topics_474[i-1]]))
                        g.add((lec_id, TEACH.hasTitle, Literal(topics_474[i - 1])))

                    # Add Labs
                    lab_id = DAT["{}{}Lab{}".format(row['Course code'], row['Course number'], i)]
                    g.add((lab_id, RDF.type, SCH.Lab))
                    g.add((lab_id, SCH.RelatedToLecture, lec_id))

                    # Add Tutorials
                    tut_id = DAT["{}{}Tut{}".format(row['Course code'], row['Course number'], i)]
                    g.add((tut_id, RDF.type, SCH.Tutorial))
                    g.add((tut_id, SCH.RelatedToLecture, lec_id))

                # Add Outline
                dir_name = "c{}content".format(row['Course number'])
                outline_path = os.path.join(dir_name, 'Outline.pdf')
                if(os.path.isfile(outline_path)):
                    g.add((cn, SCH.Outline, DAT[outline_path]))

                # Add content
                for sub_dir in ['Readings', 'Slides', 'Worksheet', 'Other']:
                    dir_path = os.path.join(dir_name, sub_dir)
                    if os.path.isdir(dir_path):
                        for idf, f in enumerate(sorted(os.listdir(dir_path))):
                            f_uri = DAT[path.join(dir_path, f)]
                            lec_id = DAT["{}{}Lec{}".format(row['Course code'], row['Course number'], idf + 1)]
                            g.add((f_uri, RDF.type, SCH[sub_dir]))
                            g.add((lec_id, SCH.HasMaterial, f_uri))
    g.serialize(destination="out/kb_test.ttl", format="turtle")


def regenerate_catalog():
    """
    Function to wrangle and clean data used in the KB construction. A bit bare bone for now.
    Creates a new .csv file CLEAN_CATALOG.csv  in the current dir.
    :return: void
    """
    catalog = pd.read_csv('CATALOG.csv')

    catalog = catalog.dropna(subset=['Course code', 'Course number'])  # remove empty course codes and course names
    catalog.to_csv('CLEAN_CATALOG.csv', index=False)


if __name__ == '__main__':
    if REGEN_CLEAN_CATALOG:
        regenerate_catalog()
    populate_knowledge_base()
