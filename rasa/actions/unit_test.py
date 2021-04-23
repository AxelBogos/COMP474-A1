from helper_functions import *

def test_q1(course,number):
    Query=load_query("q1.txt")
    Query=Query % (course,number)
    Answers=SELECT_fuseki(Query)

    if(Answers):
        
        message=f"Lecture {number} of {course} covers:\n"
        for answer in Answers:
            label=find_label_from_URI(answer)
            message +=f"{label}\t{answer}\n"
        print(message)


similatiry("lab")
#test_q1("COMP474",2)