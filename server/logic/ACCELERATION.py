
import engine as BASE
import penguin as CONF
import json
import datetime as TIME

#ACCELERATION PART

RPC_object = penguin.rpc.RPCManager("Accelerate")
Timer_object = engine.Timer()
Timer_object.pause()

def Question_number():
    get_question_number, set_question_number = penguin.rpc.use_state("qid",-1)
    #   ^^^^                ^^^^
    #GET QID             BROADCAST QID

def Question_content():
    get_question_content, set_question_content = penguin.rpc.use_state("current_question_content","")
    #   ^^^^                ^^^^
    # GET QUESTION         BROADCAST QUESTION

RPC.object.add_procedure(
    [
        ("Stop_timer", Timer_object.pause, []),
        ("Start_timer", Timer_object.resume, []),
        ("Proceed", lambda *_ : set_question_number(get_question_number()+1),[])
    ]
)

def View_question():
    if get_question_number == -1:
        set_question_content("Please wait until the session starts.")
    else:
        set_question_content(penguin.SHOW.qbank.get_question(get_question_number()).prompt)
        Timer_object.resume() 

def Wait():
    ...
    #HOW IS AN ANSWER GOT FROM THE USER? AND HOW CAN IT BE SENT?

async def Main_program_per_question():
    while True:
        Question_number()
        Question_content()
        View_question()
        await Wait()
        break
