import csv
import os
from os import path

import pandas as pd
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, RDFS
from tika import parser

DBR = Namespace("http://dbpedia.org/resource/")
DBP = Namespace("http://dbpedia.org/property/")
SCH = Namespace("http://a1.io/schema#")
DAT = Namespace("http://a1.io/data#")
TEACH = Namespace("http://linkedscience.org/teach/ns#")
ORG = Namespace("http://rdf.muninn-project.org/ontologies/organization#")

BASE_DATA_DIR = 'data'
REGENERATE_CATALOG = False
POPULATE_KNOWLEDGE_BASE = False
REGENERATE_TXT_FROM_PDF = False

special_course_codes = ['353', '474']
special_courses = [URIRef("http://a1.io/data#COMP353"), URIRef("http://a1.io/data#COMP474")]

# All topics are dbpedia resources
topics_353 = ['Database', 'Entity–relationship_model', 'Relational_database',
              'Armstrong%27s_axioms', 'Armstrong%27s_axioms', 'Database_normalization',
              'Relational_algebra', 'SQL', 'SQL', 'SQL', 'Datalog', 'Object_Definition_Language']

topics_474 = ['Intelligent_system', 'Knowledge_graph', 'Ontology_(information_science)',
              'SPARQL', 'Knowledge_base', 'Recommender_system', 'Machine_learning',
              'Intelligent_agent', 'Text_mining']

comp353_description = "Introduction to database management systems. Conceptual database design: the entity‑relationship model. The relational data model and relational algebra: functional dependencies and normalization. The SQL language and its application in defining, querying, and updating databases; integrity constraints; triggers. Developing database applications. "
comp474_description = "Rule‑based expert systems, blackboard architecture, and agent‑based. Knowledge acquisition and representation. Uncertainty and conflict resolution. Reasoning and explanation. Design of intelligent systems."


def populate_knowledge_base():
    g = Graph()
    g.parse('A1.ttl', format='turtle')

    # Add our university to the KB using the pre-defined schema
    g.add((DAT.Concordia_University, RDF.type, SCH.University))
    g.add((DAT.Concordia_University, ORG.name, Literal("Concordia University")))
    g.add((DAT.Concordia_University, RDFS.seeAlso, DBR.Concordia_University))
    with open(os.path.join(BASE_DATA_DIR, 'CLEAN_CATALOG.csv'), 'r') as data:
        r = csv.DictReader(data)
        for row in r:
            # Create the course
            cn = URIRef("http://a1.io/data#" + row['Course code'] + row['Course number'])
            g.add((cn, RDF.type, SCH.Course))

            # Add to list of offered courses at Concordia
            g.add((DAT.Concordia_University, SCH.Offers, cn))

            # Add course details
            g.add((cn, TEACH.courseTitle, Literal(row['Title'])))
            g.add((cn, SCH.HasSubject, Literal(row['Course code'])))
            g.add((cn, SCH.CourseNumber, Literal(row['Course number'])))
            if cn not in special_courses:
                g.add((cn, TEACH.courseDescription, Literal(row['Description'])))
            if row['Website'] != "":
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

                    # Add topics, Lecture Name, description
                    if row['Course number'] == '353':
                        g.add((lec_id, DBP.subject, DBR[topics_353[i - 1]]))
                        g.add((lec_id, TEACH.hasTitle, Literal(topics_353[i - 1])))
                        g.add((cn, TEACH.courseDescription, Literal(comp353_description)))
                    else:
                        g.add((lec_id, DBP.subject, DBR[topics_474[i - 1]]))
                        g.add((lec_id, TEACH.hasTitle, Literal(topics_474[i - 1])))
                        g.add((cn, TEACH.courseDescription, Literal(comp474_description)))

                    # Add Labs
                    lab_id = DAT["{}{}Lab{}".format(row['Course code'], row['Course number'], i)]
                    g.add((lab_id, RDF.type, SCH.Lab))
                    g.add((lab_id, SCH.RelatedToLecture, lec_id))

                    # Add Tutorials
                    tut_id = DAT["{}{}Tut{}".format(row['Course code'], row['Course number'], i)]
                    g.add((tut_id, RDF.type, SCH.Tutorial))
                    g.add((tut_id, SCH.RelatedToLecture, lec_id))

                # Add Outline
                dir_name = os.path.join(BASE_DATA_DIR, "c{}content").format(row['Course number'])
                outline_path = os.path.join(dir_name, 'Outline.pdf')
                if os.path.isfile(outline_path):
                    g.add((cn, SCH.Outline, DAT[outline_path]))

                # Add website (Neither special courses have one in CATALOG.csv)
                g.add((cn, RDFS.seeAlso, URIRef("http://example.com/" + row['Course code'] + row['Course number'])))

                # Add content
                for sub_dir in ['Reading', 'Slide', 'Worksheet', 'Other']:
                    dir_path = os.path.join(dir_name, sub_dir)
                    if os.path.isdir(dir_path):
                        for idf, f in enumerate(sorted(os.listdir(dir_path))):
                            f_uri = DAT[path.join(dir_path, f)]
                            lec_id = DAT["{}{}Lec{}".format(row['Course code'], row['Course number'], idf + 1)]
                            g.add((f_uri, RDF.type, SCH[sub_dir]))
                            g.add((lec_id, SCH.HasMaterial, f_uri))
    g.serialize(destination="out/kb.ttl", format="turtle")
    g.serialize(destination="out/kb_ntriples.rdf", format="ntriples")


def regenerate_catalog():
    """
    Function to wrangle and clean data used in the KB construction. A bit bare bone for now.
    Creates a new .csv file CLEAN_CATALOG.csv  in the current dir.
    :return: void
    """
    catalog = pd.read_csv(os.path.join(BASE_DATA_DIR, 'CATALOG.csv'))
    catalog = catalog.replace(r'\n', ' ', regex=True)  # remove newline characters
    catalog = catalog.dropna(subset=['Course code', 'Course number'])  # remove empty course codes and course names
    catalog.to_csv(os.path.join(BASE_DATA_DIR, 'CLEAN_CATALOG.csv'), index=False)


def regenerate_txt_from_pdf():
    generate_directories()
    for course in special_course_codes:
        base_dir = os.path.join(BASE_DATA_DIR, f"c{course}content")
        txt_dir = os.path.join(BASE_DATA_DIR, f"c{course}content" + "_txt")

        base_outline = os.path.join(base_dir, 'Outline.pdf')
        txt_outline = os.path.join(txt_dir, 'Outline.txt')

        if os.path.isfile(base_outline):
            file_data = parser.from_file(base_outline)

            # get the content of the pdf file
            output = file_data['content']

            # convert it to utf-8
            output = output.encode('utf-8', errors='ignore')
            # save it
            with open(txt_outline, 'w') as f:
                f.write(str(output))

        # Add content
        for sub_dir in ['Reading', 'Slide', 'Worksheet', 'Other']:
            base_subdir = os.path.join(base_dir, sub_dir)
            if not os.path.exists(base_subdir):
                continue
            txt_subdir = os.path.join(txt_dir, sub_dir)
            for idf, f in enumerate(sorted(os.listdir(base_subdir))):
                file_data = parser.from_file(os.path.join(base_subdir, f))

                # get the content of the pdf file
                output = file_data['content']

                # convert it to utf-8
                output = output.encode('utf-8', errors='ignore')
                # save it
                with open(os.path.join(txt_subdir, f.split(".")[0] + ".txt"), 'w') as f:
                    f.write(str(output))


def generate_directories():
    for course in special_course_codes:
        dir_name = os.path.join(BASE_DATA_DIR, f"c{course}content")
        if os.path.exists(dir_name) and not os.path.exists(dir_name + "_txt"):
            txt_dir = dir_name + "_txt"
            os.mkdir(txt_dir)
        else:
            continue

        for sub_dir in ['Reading', 'Slide', 'Worksheet', 'Other']:
            dir_path = os.path.join(dir_name, sub_dir)
            if os.path.exists(dir_path) and not os.path.exists(os.path.join(txt_dir, sub_dir)):
                txt_subdir = os.path.join(txt_dir, sub_dir)
                os.mkdir(txt_subdir)
            else:
                continue


if __name__ == '__main__':
    if REGENERATE_CATALOG:
        print('Generating catalog...')
        regenerate_catalog()
    if POPULATE_KNOWLEDGE_BASE:
        print('Populating Knolwedge Base...')
        populate_knowledge_base()
    if REGENERATE_TXT_FROM_PDF:
        print('Rendering PDF as txt...')
        regenerate_txt_from_pdf()
