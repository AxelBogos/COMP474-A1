
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.helper_functions import *


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
            message=f"{tracker.slots['course']} is about {Answer[0]}."
        else:
            message=f"I don't find any information about {tracker.slots['course']}."

        dispatcher.utter_message(text=message)
        return []

# Question 3
class Action_Which_course_teaches_about(Action):

    def name(self) -> Text:
        return "action_which_course_in_university_teaches_about_subject"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        topic=generate_dbpedia_entities(tracker.slots['topic'])
        university=generate_dbpedia_entities(tracker.slots['university'])
        
        message=f"I don't find any course at {tracker.slots['university']} about {tracker.slots['topic']}."
        

        if(university and topic): 
            Query=load_query("q3.txt") 
            Query=Query %(university, topic)
            Answer=SELECT_fuseki(Query)
            if(Answer):
                a=Answer[0].replace("data#",'')
                message=f"{a} teaches {tracker.slots['topic']}."
       
        dispatcher.utter_message(text=message)
        return []

# Question 4
class materials_for_lec(Action):
    def name(self) -> Text: return "materials_for_lecture"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        Query = load_query("q4.txt")
        Query = Query %(tracker.slots['course'], tracker.slots['lecture_number'])
        Answer = SELECT_fuseki(Query)

        if(Answer):
            message = f"Lecture {tracker.slots['lecture_number']} of {tracker.slots['course']} covered the following material(s):\n"
            for a in Answer:
                message = message + f"\t- {a}\n"
        else: 
            message = f"No course materials found for {tracker.slots['lecture_number']} of {tracker.slots['course']}"

        dispatcher.utter_message(text=message)
        return []

# Question 5
class Action_Course_Link(Action):

    def name(self) -> Text:
        return "action_university_offers_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message=f"No, it doesn't."
        
        university=generate_dbpedia_entities(tracker.slots['university'])
       
        if(university):
            Query=load_query("q5.txt")
            Query=Query % (university,tracker.slots['course'])
            Answer=ASK_fuseki(Query)
            if(Answer):
                message=f"Yes, it does!"
        
        dispatcher.utter_message(text=message)
        return []

# Question 6
class get_unis_teach_topic(Action):
    def name(self) -> Text: return "get_unis_teach_topic"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
         
        topic = generate_dbpedia_entities(tracker.slots['topic'])

        if(topic):
            print(topic)
            Query = load_query("q6.txt")
            Query = Query % (topic)
            answer = SELECT_fuseki(Query)
            if(answer):
                message = f"The topic '{tracker.slots['topic']}' is taught in some courses at:\n"
                for a in answer:
                    message = message + f"\t- {find_label(a)}\n"
            else: message = f"Could not find any universities that teach courses about {tracker.slots['topic']}"

        else: message = f"Did not recognize topic '{tracker.slots['topic']}'"

        dispatcher.utter_message(text=message)
        return []