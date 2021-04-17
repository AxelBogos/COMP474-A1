import requests

def query_fuseki(query):

    responses = requests.post('http://localhost:3030/A1/sparql',data={'query': query}).json()["results"]['bindings']
   
    values=[]
    for response in responses:
        values.append(response["topic"]["value"])
    return values


