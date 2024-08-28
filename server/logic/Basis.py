import threading
import queue
import json
import Communicator as COMMS
import datetime

#THREADS
Threads = {1:"Inactive",2:"Inactive",3:"Inactive",4:"Inactive"}

#PORTS
Ports = {1:b'',2:b'',3:b'',4:b''}
Port_Status = [None,"Open","Open","Open","Open"]

#QUEUES
Main_Queue = queue.Queue(maxsize = 1)
TX_Queue = queue.Queue(maxsize = 0)
RX_Queue = queue.Queue(maxsize = 0)
Sync_Queue = queue.Queue(maxsize = 1)
Time_Queue = queue.Queue(maxsize = 1)

#CHECKPOINTS
Supposed_external_checkpoint = 0
Supposed_internal_checkpoint = 0

class Participant:
    
    def __init__(self,name:str) -> "Create a player instance.":
        self.name = name
    
    def getscore(self,score:int) -> "Award scores to player.":
        self.score += score
    
    def getpermission(self,allowed:bool) -> "Allow the player to do something.":
        self.allowed = allowed
    
    def Ignore(self,ignore:bool) -> "Ignore the player.":
        self.ignore = ignore
    
    def Answer(self,answer:bytes) -> "Answer a question.":
        self.answer = answer
    
    def sendstatistics(self,destination_port:int) -> "Send information to a port.":
        '''
        This function generates a byte string consisting of the following:
            The header, in this case: 'TFR PYR,' TFR indicating that this is to be sent, while 'PYR' means that this is from a player.
            The name of the player.
            The score of the player.
        Data is put into one of the four ports given.
        '''
        Ports[destination_port] = b'TFR PYR'
        + b'IDENT' + self.name.encode('utf-8','strict')
        + b'SCORE' + str(self.score).encode('utf-8','strict')
        + b'ANSWER' + self.answer
    
class Question:

    def __init__(self,content:str,worth:int):
        self.content = content
        self.worth = worth
    
    def State(self,selected:bool) -> "Select a question.":
        self.selected = selected
    
    def Close(self,closed:bool) -> "Close a question - making it unavailable.":
        self.closed = closed
    
    def ReplaceContent(self,new_content:str) -> "Changes the question's content":
        self.content = new_content

def Synchronize() -> "This function sends a synchronization request to other devices.":
    SYNC_MESSAGE = b'TFR SNC'
    try:
        TX_Queue.put(SYNC_MESSAGE,blocking = False,timeout = None)
    except queue.Full:
        pass

def Port_To_Queue(port_number:int) -> "Send information from a port to the main queue":
    try:
        if Port_Status[port_number] == "Open":
            Main_Queue.put(Ports[port_number],block = False,timeout = None)
        else:
            return ValueError("Port closed")
    except queue.Full:
        pass

def Clear_Ports() -> "Regulating ports.":
    Cleared_port = 0
    if Main_Queue.full() is True:
        Port_Status[1:] = "Closed"
        Cleared_port = 0
    else:
        Cleared_port += 1
        Port_Status[Cleared_port] = "Open"
    if Cleared_port == 4:
        Cleared_port = 0
    else:
        pass

@staticmethod
def Extract_Question_Data(data:str) -> "This function parses question data.":
    Buffer = ""
    Output = {"Content":"","Score":0,"Key":"","Other":None}
    for parser_pointer in range(0,len(data)-1,1):
        Buffer += data[parser_pointer]
        if Buffer[:2] == "CT" and len(Buffer) == 5:
            Output[Content] = data[parser_pointer+1:parser_pointer+int(Buffer[2:6],10)]
        elif Buffer[:2] == "SC" and len(Buffer) == 5:
            Output[Score] = int(data[parser_pointer+1:parser_pointer+int(Buffer[2:6],10)],10)
        elif Buffer[:2] == "AK" and len(Buffer) == 5:
            Output[Key] = data[parser_pointer+1:parser_pointer+int(Buffer[2:6],10)]
        elif Buffer[:2] == "TP" and len(Buffer) == 5:
            Output[Explanation] = data[parser_pointer+1:parser_pointer+int(Buffer[2:6],10)]
        else:
            raise TypeError("Invalid input.")
    return Output

def Internal_Receive() -> "This function reads from RX_Queue.":
    Received_data = RX_Queue.get(blocking = False,timeout = None)
    RX_Queue.task_done()
    Received_data = Received_data.decode('utf-8','strict')
    if Received_data[0:8] == "TFR QST":
        Extract_Question_Data(Received_data[9:])
    elif Received_data[0:8] == "TFR RSC":
        Supposed_external_checkpoint = Received_data[9:]
    else:
        pass

def Internal_Send() -> "This function writes to TX_Queue.":
    TX_mode = False
    try:
        TX_data = Main_Queue.get(block = False,timer = None)
    except queue.Empty:
        pass
    #CHECK THE HEADER
    if TX_data[0:3] == b'TFR':
        TX_mode = True
        Main_Queue.task_done()
    else:
        TX_data = b''
        TX_mode = False
    #CALCULATE AND THEN CONCATENATE THE CRC REMAINDER
    TX_data = COMMS.CRC(TX_data,[16,12,5,0])
    try:
        TX_Queue.put(TX_data,blocking = False,timeout = None)
    except queue.Full:
        pass

def Timer(checking_interval:int) -> "This function sends internal synchronyzation request and updates the Time_Queue.":
    Timer_object = datetime.today()
    Previous_second_check = Timer_object.second()
    while True:
        if Timer_object.second() > Previous_second_check + checking_interval and timeoutmode == False:
            try:
                Time_Queue.get(blocking = False, timeout = None)
            except queue.Full:
                pass
            try:
                Sync_Queue.put("SYNCHRONIZE",blocking = False,timeout = None)
                Time_Queue.put(Timer_object.second(),blocking = False, timeout = None)
            except queue.Full:
                pass
        else:
            pass

Regulating_Thread = threading.Thread(target = Clear_Ports, args = (), daemon = True)
Timing_Thread = threading.Thread(target = Timer,args = (5),daemon = True)

'''MAIN PROGRAM STARTS HERE.'''

#A LIST OF ALL DEVICES INVOLVED
Device_Address_List = ["","","",""]
Regulator_Address = ""
Corresponding_Data = {"1":b'',"2":b'',"3":b'',"4":b''}
UDP_Port = 6942

#INITIALIZING GAME

Timing_Thread.start()
Regulating_Thread.start()

Initialize_Check = ""

Initializer = open('Initializing_file.json')
Initial_dictionary = json.loads(Initializer)

Participant_object = Participant(Initializer["Name"])

INITIAL_MESSAGE = COMMS.CRC(Input = b'CONNECT', Exponents = [16,12,5,0])
ACCEPTANCE_MESSAGE = b''
HOLD_MESSAGE = COMMS.CRC(Input = b'HOLD', Exponents = [16,12,5,0])
CALLSIGN = Initializer["Callsign"]

Confirmation = b''

if Initializer["Regulator"] == 1:
    for PARTICIPANT in Device_Address_List:
        COMMS.Communicate(message = CALLSIGN, port = UDP_Port, buffersize = 0, source = '', destination = PARTICIPANT, rw = True)
        Confirmation = COMMS.Communicate(message = b'', port = UDP_Port, buffersize = 3, source = PARTICIPANT, destination = '', rw = False)
elif Initializer["Regulator"] == 0:
    Received_Request = COMMS.Communicate(message = b'', port = UDP_Port, buffersize = 6, source = Regulator_Address, destination = '', rw = False)
    COMMS.Communicate(message = CALLSIGN, port = UDP_Port, buffersize = 0, source = '', destination = Regulator_Address, rw = True)
