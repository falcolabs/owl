import TCP_Communicator as Communicator
import datetime
import thread
import queue
import tkinter

Time_elapsed = 0
Time_queue = queue.Queue(maxsize = 1)

CALLSIGN = b'Hi!'
POLYNOMIAL = polynomial
Port = Communicator.Port
Initializer_Values = Communicator.Initializer_Values
Socket_Descriptor = Communicator.Socket_Descriptor
HOST = Initializer_Values["Host address"]
Name = Initializer_Values["Name"]

Communicator.Generate_TCP_Socket(Host = False, 
                    Port = Port, 
                    Host_Address = HOST)
Reply = Communicator.Receive(Socket_Descriptor["SOCKET"], Buffer_Size = 3)
if Reply == b'Hi!':
    pass
else:
    raise ValueError("Unexpected callsign from host.")
Communicator.Send(Socket_Descriptor["SOCKET"], Data = CALLSIGN, Destination = HOST, Port = Port)

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

def Check_Time():
    global Time_queue, Time_elapsed
    try:
        Time_elapsed = Time_queue.get(blocking = False, timeout = None)
        Time_queue.put(Time_elapsed, blocking = False, timeout = None)
        return Time_elapsed
    except:
        pass

def End_Session():
    global Socket_Descriptor
    Communicator.Close_Socket(Socket_Descriptor["SOCKET"])
    return True

#RECEIVE THE QUESTION

def Receive_Question():
    global Socket_Descriptor
    Data = Communicator.Receive(Socket_Descriptor["SOCKET"], Buffer_Size = 50000)
    return Data

#SEND THE ANSWER

Time = 0

def Send_Answer(Answer:bytes):
    global Socket_Descriptor, HOST, Port, POLYNOMIAL, Name, Time, Time_elapsed, Time_queue
    if Answer != b'':
        Time = Check_Time()
        Communicator.Send(Socket_Descriptor["SOCKET"], Data = (b'!     !' + str(Time) + Name + Answer), Destination = HOST, Port = Port)
        return True
    else:
        pass

Timer_thread = threading.Thread(target = Timer, args = (), daemon = True)

PART = 0

Client_Interface = tkinter.Tk()
Client_Frame = tkinter.Frame(Client_Interface)
Client_Frame.pack(fill = 'both')
Client_Frame.grid()

#DISPLAYING THE QUESTION ON THE FRAME

LINE_LIMIT = 150

FIN = False

QUESTION = b''

Question_Label = tkinter.Label(Client_Frame, text = QUESTION).grid(column = 10, row = 5)
Send_Answer = tkinter.Button(Client_Frame, text = "Send answer", command = lambda: Send_Answer(Answer = ANSWER)).grid(column = 75, row = LINE_COUNT + 5)

while FIN == False:
    LINE_COUNT = 1

    QUESTION = Communicator.Receive(Socket_Descriptor["SOCKET"], Buffer_Size = 2048)

    if QUESTION == b'FIN':
        Question_Label.destroy()
        Send_Answer.destroy()
        Completion_Notification = tkinter.Label(Client_Frame, text = "PROGRAM IS FINISHED.").grid(column = 10, row = 10)
        End_Session()
        FIN = True
    else:
        QUESTION = QUESTION.decode('utf-8', 'strict')
        for Character_Index in range(0,len(QUESTION) - 1,1):
            if Character_Index % LINE_LIMIT == 0 and QUESTION[Character_Index] == " ":
                QUESTION = QUESTION[:Character_Index] + r"\n" + QUESTION[Character_Index:]
                LINE_COUNT += 1
            elif Character_Index % LINE_LIMIT == 0 and QUESTION[Character_Index] != " ":
                QUESTION = QUESTION[:Character_Index] + "-" + r"\n" + QUESTION[Character_Index:]
                LINE_COUNT += 1
            else:
                pass
    
    Question_Label.config(QUESTION)
    Reset_Timer()

tkinter.mainloop()

#FIN
