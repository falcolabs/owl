
import engine
import penguin
import json
import datetime as TIME

#ACCELERATION PART

Questions = {
    1:"Speed",
    2:"Organization",
    3:"Logic",
    4:"Identification"}

RPC_object = penguin.rpc.RPCManager()

#THE QUESTION DICTIONARY
Question_storage_location = ""
Question_repository = engine.QuestionBank.load(filepath = Question_storage_location)

#THE TIME REFERENCE
Time_reference = TIME.today()

def Timer_start():
    Start_time = Time_reference.second()

def Timer_stop():
    Stop_time = Time_reference.second()
    Time_elapsed = Stop_time - Start_time
    return Time_elapsed

Question_number = 0
Question_description = ""

RPC.object.add_procedure(
    [
        ("Answer", Timer_stop, []),
        ("Start_timer", Timer_start, []),
        ("Proceed", engine.QuestionBank.get_question, [Question_number])
    ]
)

if Question_number == 0:
    print(False)
else:
    Question_description = Questions[Question_number]
'''
TO BE DEVELOPED
'''
