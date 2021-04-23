
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

# Question 7
class count_courses_by_subj(Action):
    def name(self) -> Text:
        return "count_courses_by_subj"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        uni = generate_dbpedia_entities(tracker.slots['university'])
        subj = tracker.slots['subject']

        Query = load_query("q7.txt")
        Query = Query %(uni, tracker.slots['subject'])
        answer = SELECT_fuseki(Query)

        if(answer):
            message = f"There are {answer[0]} {tracker.slots['subject']} courses taught at {tracker.slots['university']}"
        else:
            message = f"Could not find any {tracker.slots['subject']} courses at {tracker.slots['university']}"

        dispatcher.utter_message(text=message)
        return []

#Question 8
class get_website(Action):
    def name(self) -> Text:
        return "get_website"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        course = tracker.slots['course']
        Query = load_query("q8.txt") % (course)
        answer = SELECT_fuseki(Query)

        if (answer):
            message = f"The website for {tracker.slots['course']} is: {answer[0]}"
        else:
            message = f"A website for {tracker.slots['course']} could not be found"

        dispatcher.utter_message(text=message)
        return []


#Question 9
class count_readings(Action):
    def name(self) -> Text:
        return "count_readings"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        answer = SELECT_fuseki(load_query("q9.txt"))

        if (answer):
            message = f"{answer[0].replace('http://a1.io/data#',' ')} has {answer[1]} readings"
        else:
            message = f"You have asked an unanswerable question, you fool! Reassess the choices you have made to end up here."

        dispatcher.utter_message(text=message)
        return []

#Question 10
class subj_by_title(Action):
    def name(self) -> Text:
        return "subj_by_title"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        title = tracker.slots['course_title']
        subj = tracker.slots['subject']
        print(title, '\t', subj)

        # print(f"{title}: {subj}")
        get = SELECT_fuseki(load_query("q10.2.txt") % (title))

        #both are provided -> check truthfulness, return truth
        if title and subj != "initial": 
            ask = ASK_fuseki(load_query("q10.txt") % (subj, title))
            
            if ask == True: message = f"Yes, {title} is a {subj} course"
            elif ask == False and get: message = f"No, {title} is a {get[0]} course"
            else: message =  "I dont recognize that course"
            
        # only title provided -> just get the subject of that course
        elif title and subj == "initial":
            if get: message = f"{title} is a {get[0]} course"
            else: message = f"Could not determine the subject of {title}"
        else: message = "Something went wrong..."

        dispatcher.utter_message(text=message)
        return []
        