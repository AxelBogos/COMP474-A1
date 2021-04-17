
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

query2='prefix a1_data: <http://a1.io/data#> prefix dbp: <http://dbpedia.org/property/> prefix a1_schema: <http://a1.io/schema#> SELECT ?topic WHERE{a1_data:%s a1_schema:HasLecture ?lecture .?lecture a1_schema:LectureNumber 2 .?lecture dbp:subject ?topic}'

def query_fuseki(query):

    responses = requests.post('http://localhost:3030/A1/sparql',data={'query': query}).json()["results"]['bindings']
   
    values=[]
    for response in responses:
        values.append(response["topic"]["value"])
    return values

class Action_Course_Info(Action):

    def name(self) -> Text:
        return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        query=query2 % tracker.slots['course']
        answer=query_fuseki(query)

        dispatcher.utter_message(text=f"{tracker.slots['course']} is about {answer[0]} ")
        return []
