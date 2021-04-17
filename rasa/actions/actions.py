
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from helper_functions import query_fuseki, load_query


query2='prefix a1_data: <http://a1.io/data#> prefix dbp: <http://dbpedia.org/property/> prefix a1_schema: <http://a1.io/schema#> SELECT ?topic WHERE{a1_data:%s a1_schema:HasLecture ?lecture .?lecture a1_schema:LectureNumber 2 .?lecture dbp:subject ?topic}'



class Action_Course_Info(Action):

    def name(self) -> Text:
        return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        Query=load_query("q2.txt")
        Query=Query % tracker.slots['course']
        Answer=query_fuseki(Query)

        if(Answer):
            message=f"{tracker.slots['course']} is about {Answer[0]}"
        else:
            message=f"I don't find any information about {tracker.slots['course']}."

        dispatcher.utter_message(text=message)
        return []
