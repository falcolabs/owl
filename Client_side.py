import TCP_Communicator as Communicator
import datetime
import thread
import queue
import tkinter

Time_elapsed = 0
Time_queue = queue.Queue(maxsize = 1)

CALLSIGN = b'Hi!'
POLYNOMIAL = Communicator.CRC_polynomial
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
Communicator.Send(Socket_Descriptor["SOCKET"], Data = Communicator.CRC(CALLSIGN,POLYNOMIAL), Destination = HOST, Port = Port)

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

def End_Session():
    global Socket_Descriptor, Port, POLYNOMIAL, Client_List
    for Client in Client_List:
        Communicator.Send(Socket_Descriptor["SOCKET"], Data = Communicator.CRC(b'FIN',POLYNOMIAL), Destination = Client, Port = Port)
    Communicator.Close_Socket()
    return True

#RECEIVE THE QUESTION

def Receive_Question():
    global Socket_Descriptor
    Data = Communicator.Receive(Socket_Descriptor["SOCKET"], Buffer_Size = 50000)
    return Data

#SEND THE ANSWER

def Send_Answer(Answer:bytes):
    global Socket_Descriptor, HOST, Port, POLYNOMIAL, Name
    Communicator.Send(Socket_Descriptor["SOCKET"], Data = Communicator.CRC((b'!     !' + Name + Answer),POLYNOMIAL), Destination = HOST, Port = Port)
    return True

Timer_thread = threading.Thread(target = Timer, args = (), daemon = True)

'''
TO BE DEVELOPED
'''
