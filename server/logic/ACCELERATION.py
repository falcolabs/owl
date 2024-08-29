
import engine as BASE
import penguin as CONF
import json
import datetime as TIME

#ACCELERATION PART

Questions = {1:"Speed",2:"Organization",3:"Logic",4:"Identification"}

RPC_object = penguin.rpc.RPCManager()
Timing_object = TIME.today()

def Timer_start():
    Start_time = Timing_object.second()

def Timer_stop():
    Stop_time = Timing_object.second()
    Time_elapsed = Stop_time - Start_time

Question_number = 0

RPC.object.add_procedure(
    [
        ("Answer", Timer_stop, []),
        ("Start_timer", Timer_start, []),
        ("Proceed", engine.QuestionBank.get_question, [Question_number])
    ]
)

def Get_question(number: int):
    return penguin.SHOW.qbank.get_question(number).prompt

if Question_number == 0:
    False
else:
    Get_question(Question_number)

'''
TO BE DEVELOPED
'''
