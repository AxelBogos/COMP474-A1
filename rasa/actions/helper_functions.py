import requests
from rdflib import Graph,URIRef, RDFS 
import spacy
import os
import time
import numpy as np
dir_path= os.path.abspath(os.path.join('..','A1','A1_Queries'))
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('dbpedia_spotlight')



def SELECT_fuseki(query):
    responses = requests.post('http://localhost:3030/A1/sparql',data={'query': query}).json()["results"]['bindings']
    values=[]
    for response in responses:
        for key in response.keys():
            values.append(response[key]["value"])
    return values

def ASK_fuseki(query):
     response = requests.post('http://localhost:3030/A1/sparql',data={'query': query}).json()
     return response['boolean']

def load_query(file_name):
    path=os.path.join(dir_path,file_name)
    with open(path) as f:
        return f.read()

            
def find_label_from_URI(uri):
    out=os.path.basename(uri)
    out=out.replace('_',' ')
    return out

def generate_dbpedia_entities(file_txt):
    doc = nlp(file_txt)
    entities = []
    out = ''

    for ent in doc.ents:
        if eval(ent._.dbpedia_raw_result['@similarityScore']) >= 0.75:
            entities.append(ent.kb_id_)

    if(len(entities)>0):
        entities.sort()
        out=os.path.basename(entities[0])

    return out

def similarity(word):
    ref= 'Lab Lecture Tutorial'
    ref_tokens = nlp(ref)
    input_token = nlp(word)
    result=[]
    for token in ref_tokens:
        result.append(token.similarity(input_token))
    result=np.array(result)
    i=np.argmax(result)
    s=ref.split()
    return s[i]
    

