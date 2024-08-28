
import engine as BASE
import penguin as CONF
import json
import datetime as TIME

#ACCELERATION PART

Questions = {1:"Speed",2:"Organization",3:"Logic",4:"Identification"}

RPC_object = penguin.rpc.RPCManager()
Timing_object = engine.Timer()
Timing_object.pause()

#THE QUESTION DICTIONARY
Question_storage_location = ""
Question_repository = engine.QuestionBank.load(filepath = Question_storage_location)

Question_number = 0

RPC.object.add_procedure(
    [
        ("Answer", Timing_object.pause, []),
        ("Start_timer", Timing_object.resume, []),
        ("Proceed", engine.QuestionBank.get_question, [Question_number])
    ]
)


'''
TO BE DEVELOPED
'''
