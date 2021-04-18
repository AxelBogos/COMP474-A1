
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from helper_functions import SELECT_fuseki, ASK_fuseki,load_query, find_label

# Question 1
class Action_topic_of_lecture(Action):

    def name(self) -> Text:
        return "action_topic_of_lecture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        Query=load_query("q1.txt")
        Query=Query % (tracker.slots['course'],tracker.slots['lecture_number'])
        Answer=SELECT_fuseki(Query)
        

        if(Answer):
            process_query=find_label(Answer[0])
            message=f"Lecture {tracker.slots['lecture_number']} of {tracker.slots['course']} is about {process_query}"
        else:
            message=f"I don't find any information about the lecture {tracker.slots['lecture_number']} of {tracker.slots['course']}."

        dispatcher.utter_message(text=message)
        return []


# Question 2
class Action_Course_Info(Action):

    def name(self) -> Text:
        return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        Query=load_query("q2.txt")
        Query=Query % tracker.slots['course']
        Answer=SELECT_fuseki(Query)

        if(Answer):
            message=f"{tracker.slots['course']} is about {Answer[0]}"
        else:
            message=f"I don't find any information about {tracker.slots['course']}."

        dispatcher.utter_message(text=message)
        return []
# Question 5
class Action_Course_Link(Action):

    def name(self) -> Text:
        return "action_university_offers_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        Query=load_query("q5.txt")
        Query=Query % (tracker.slots['university'],tracker.slots['course'])
        Answer=ASK_fuseki(Query)
        print(Answer)
        if(Answer):
            message=f"Yes, it does!"
        else:
            message=f"No, it doesn't."

        dispatcher.utter_message(text=message)
        return []
