import TCP_Communicator as Communicator
import datetime
import thread
import queue
import tkinter

QUESTION_BANK = json.parse(open('Questions.json'))
QUESTION_NUMBER = 0
Time_elapsed = 0
Time_queue = queue.Queue(maxsize = 1)

CALLSIGN = b'Hi!'
POLYNOMIAL = polynomial
Port = Communicator.Port
Initializer_Values = Communicator.Initializer_Values
Socket_Descriptor = Communicator.Socket_Descriptor
Client_List = Communicator.Client_List
Callsign_List = Initializer_Values["Callsign list"]

Communicator.Generate_TCP_Socket(Host = True, 
                    Port = Port, 
                    Clients = Client_List, 
                    Host_Address = Initializer_Values["Address"], 
                    Address = Initializer_Values["Address"])
for Client in Client_List:
    Communicator.Send(Socket_Descriptor["SOCKET"], Data = CALLSIGN, Destination = Client, Port = Port)
    Reply = Communicator.Receive(Buffer_Size = 3)
    if Reply == b'Hi!':
        pass
    else:
        raise TypeError("Wrong callsign from "+Client)

#GET THE QUESTIONS

Options = []
Option_count = 0

Answer_List = []
Scores = {Callsign_List[0]:0,Callsign_List[1]:0,Callsign_List[2]:0,Callsign_List[3]:0}
Responsiveness = {Callsign_List[0]:0,Callsign_List[1]:0,Callsign_List[2]:0,Callsign_List[3]:0}

def Next_question(Client:str):
    global Socket_Descriptor, Port, QUESTION_BANK, QUESTION_NUMBER, POLYNOMIAL
    Communicator.Send(Socket_Descriptor["SOCKET"], Data = QUESTION_BANK[QUESTION_NUMBER], Destination = Client, Port = Port)
    QUESTION_NUMBER = QUESTION_NUMBER + 1

#BROADCAST THE QUESTION

def Broadcast_question():
    global Socket_Descriptor, Port, QUESTION_BANK, QUESTION_NUMBER, POLYNOMIAL, Client_List
    for Client in Client_List:
        Communicator.Send(Socket_Descriptor["SOCKET"], Data = QUESTION_BANK[QUESTION_NUMBER], Destination = Client, Port = Port)
    for Client in Client_List:
        Answers = Communicator.Receive(Socket_Descriptor["SOCKET"], Buffer_Size = 50000)
    return Answers
    QUESTION_NUMBER = QUESTION_NUMBER + 1

def Evaluate_Answers(Answers:bytes, Key:bytes):
    global Answer_List, Scores
    #SEPARATING THE ANSWERS
    Check = False
    Chunk = False
    Chunk_length = 0
    Check_Buffer = b''
    for Check_Chunk in range(0,len(Answers) - 1,1):
        if Answers[Check_Chunk:Check_Chunk + 7] == b'!     !':
            Chunk_length = Answers[Check_Chunk + 7: Check_Chunk + 10]
            Chunk = Answers[Check_Chunk + 11: Check_Chunk + Chunk_length]
            Check_Chunk = Check_Chunk + Chunk_length + 10
            Answer_List.append(Chunk)
        else:
            pass
    for Answer_Considered in Answer_List:
        Scores[Answer_Considered[:5]] += 10 * int(Answer_Considered[10:] == Key)
        Responsiveness[Answer_Considered[:5]] = Answer_Considered[5:10]
    return True

    '''
    ANSWER FORMAT:
        From byte 1 to byte 7: Answer header
        From byte 8 to byte 11: Answer length
        From byte 11 to byte 15: Origin of answer
        From byte 16 to byte 21: Response time
        From byte 22 and onwards: Answer content
    '''

def Broadcast():
    global Socket_Descriptor, Port, QUESTION_BANK, QUESTION_NUMBER, POLYNOMIAL, Client_List, Answer_List, Scores, Callsign_List
    ANSWER_LIST = Broadcast_question()
    Evaluate_Answers(ANSWER_LIST, QUESTION_BANK[QUESTION_NUMBER][2])
    for Client_Index in range(0,len(Client_List) - 1,1):
        Score = b''.fromhex(str(hex(Scores[Callsign_List[Client_Index]])).replace('0x',''))
        Communicator.Send(Socket_Descriptor["SOCKET"], Data = Score, Destination = Client_List[Client_Index], Port = Port) 
    return True

#SELECT QUESTIONS

def Select_Question(Selections:list):
    global Socket_Descriptor, Port, QUESTION_BANK, QUESTION_NUMBER, POLYNOMIAL, Client_List, Options
    Options = [QUESTION_BANK[QUESTION_NUMBER][Selections[0]],QUESTION_BANK[QUESTION_NUMBER][Selections[1]],QUESTION_BANK[QUESTION_NUMBER][Selections[2]]]

def Proceed(Client:str):
    global Socket_Descriptor, Port, QUESTION_BANK, QUESTION_NUMBER, POLYNOMIAL, Client_List, Options
    Communicator.Send(Socket_Descriptor["SOCKET"], Data = Options,[Option_count], Destination = Client, Port = Port)
    Requests = Communicator.Receive(Socket_Descriptor["SOCKET"], Buffer_Size = 32)
    Option_count += 1
    return Requests

#TIMING

def Timer():
    global Time_queue, Time_elapsed
    Time_Object = datetime.today()
    Start_time = Time_Object.second()
    while True:
        Current_time = Time_Object.second()
        if Start_time != Current_time:
            try:
                Time_elapsed = Time_queue.get(blocking = False, timeout = None)
            except:
                pass
            Time_elapsed += 1
            if Time_elapsed == 200000:
                Time_elapsed = 0
            else:
                pass
            try:
                Time_queue.put(Time_elapsed, blocking = False, timeout = None)
            except:
                pass
        else:
            pass

def Reset_Timer():
    global Time_queue, Time_elapsed
    try:
        Time_elapsed = Time_queue.get(blocking = False, timeout = None)
        Time_elapsed = 0
        Time_queue.put(Time_elapsed, blocking = False, timeout = None)
    except:
        pass

def Check_Time(Time:int):
    global Time_queue, Time_elapsed
    try:
        Time_elapsed = Time_queue.get(blocking = False, timeout = None)
        Time_queue.put(Time_elapsed, blocking = False, timeout = None)
        if Time_elapsed > Time:
            return True
        else:
            return False
    except:
        pass

def Timeout(Time:int):
    global Time_queue, Time_elapsed
    Reset_Timer()
    Check_Time(Time)

def End_Session():
    global Socket_Descriptor, Port, POLYNOMIAL, Client_List
    for Client in Client_List:
        Communicator.Send(Socket_Descriptor["SOCKET"], Data = b'FIN', Destination = Client, Port = Port)
    Communicator.Close_Socket()
    return True

#CONFIGURATION OF INTERFACE

Timer_thread = threading.Thread(target = Timer, args = (), daemon = True)

PART_NUMBER = 0
PLAYER_LIST = [""]
CURRENT_PLAYER = 0

Interface_Object = tkinter.Tk()
Control_Frame = tkinter.Frame(Interface_Object)
Control_Frame.Pack(fill = 'both')
Control_Frame.grid()
Level_Label = tkinter.Label(Control_Frame, text = "PART: "+str(PART_NUMBER)).grid(column = 25, row = 10)
Client_Label = tkinter.Label(Control_Frame, text = "PLAYER: "+PLAYER_LIST[CURRENT_PLAYER]).grid(column = 25, row = 25)
Question_Label = tkinter.Label(Control_Frame, text = "QUESTION:"+QUESTION_NUMBER)

Started = False
FIN = False

def START():
    global PART_NUMBER, Level_Label, Reset_Timer, Started
    if Started == False:
        Reset_Timer()
        PART_NUMBER += 1
        Level_Label.config(PART_NUMBER)
        Started = True
    else:
        pass

def NEXT_PLAYER():
    global Started, PLAYER_LIST, CURRENT_PLAYER, Client_Label
    if Started == True:
        CURRENT_PLAYER += 1
        Client_Label.config(PLAYER_LIST[CURRENT_PLAYER])
    else:
        pass

def NEXT_PART():
    global Started, Level_Label, Client_Label, PLAYER_LIST, CURRENT_PLAYER, Reset_Timer, PART_NUMBER
    if Started == True:
        PART_NUMBER += 1
        Level_Label.config(PART_NUMBER)
        CURRENT_PLAYER = 0
        Client_Label.config(PLAYER_LIST[CURRENT_PLAYER])
    else:
        pass
    
Start_Button = tkinter.Button(Control_Frame, text = "START SESSION", command = START).grid(column = 10, row = 10)
Selected_List = []
while FIN == False:
    if Started == True and PART_NUMBER == 1:
        Next_Player = tkinter.Button(Control_Frame, text = "NEXT PLAYER", command = NEXT_PLAYER).grid(column = 10, row = 25)
        Next_Question = tkinter.Button(Control_Frame, text = "NEXT QUESTION", command = lambda: Next_Question(Client_List[CURRENT_PLAYER])).grid(column = 10, row = 35)
        Next_Part = tkinter.Button(Control_Frame, text = "NEXT PART", command = NEXT_PART).grid(column = 20, row = 75)
        Current_Question = tkinter.Label(Control_Frame, text = "QUESTION NUMBER: "+str(QUESTION_NUMBER)).grid(column = 40, row = 15)
    elif Started == True and PART_NUMBER >= 2 and PART_NUMBER < 4:
        Next_Player.destroy()
        Next_Question.destroy()
        Next_Question = tkinter.Button(Control_Frame, text = "NEXT QUESTION", command = Broadcast()).grid(column = 10, row = 35)
    elif Started == True and PART_NUMBER == 4:
        Question_Type = tkinter.Label(Control_Frame, text = "QUESTION TYPES").grid(column = 10, row = 50)
        Q_Selected = tkinter.Label(Control_Frame, text = str(Selected_List)).grid(column = 10, row = 90)
        def SELECT_VALUE(Value:int):
            global Q_Selected, Selected_List
            Selected_List.append(Value)
            Q_Selected.config(Selected_List)
        Q10_Select = tkinter.Button(Control_Frame, text = "10", command = lambda: Selected_List.append(10)).grid(column = 10, row = 60)
        Q20_Select = tkinter.Button(Control_Frame, text = "20", command = lambda: Selected_List.append(20)).grid(column = 10, row = 70)
        Q30_Select = tkinter.Button(Control_Frame, text = "30", command = lambda: Selected_List.append(30)).grid(column = 10, row = 80)
    elif Started == True and PART_NUMBER > 3:
        Next_Question.destroy()
        Next_Part.destroy()
        Current_Question.destroy()
        Question_Type.destroy()
        Q10_Select.destroy()
        Q20_Select.destroy()
        Q30_Select.destroy()
        Q_Selected.destroy()
        Completion = tkinter.Label(Control_Frame, text = "PROGRAM COMPLETE.").grid(column = 25, row = 25)
        Reset_Timer()
        End_Session()
        CHECK = False
        while CHECK == False:
            CHECK = Check_Time(Time = 30)
        Interface_Object.destroy()
        FIN = True
        break
    else:
        raise IndexError("Invalid part number, or faulty code.")

tkinter.mainloop()

#FIN