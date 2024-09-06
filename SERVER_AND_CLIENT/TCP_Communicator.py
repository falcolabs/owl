import socket
import json



Initializer = open('Descriptor.json')
Initializer_Values = json.parse(Initializer)



Port = Initializer_Values["Port"]
Client_List = []
Accepted_Clients = []
Socket_in_existence = False
CRC_polynomial = Initializer["CRC polynomial exponents"]


Socket_Descriptor = {"SOCKET":None, "PORT":Port, "HOST":None, "HOST ADDRESS":""}
def Generate_TCP_Socket(Host:bool, Port:int, Clients:list, Host_Address:str, Address:str):

    global Socket_Descriptor, Socket_in_existence, Client_List, Port, Accepted_Clients
    if Socket_in_existence == False:
        TCP_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if Host == True:
            TCP_Socket.bind((Address, Port))
            TCP_Socket.listen(len(Clients))
            for Client in Clients:
                Client_Socket, Client_Address = TCP_Socket.accept()
                if Client_Address in Clients:
                    Accepted_Clients.append(Client_Address)
                else:
                    pass
        elif Host == False:
            TCP_Socket.connect((Host_Address, Port))
        else:
            pass
        Socket_Descriptor["SOCKET"] = TCP_Socket
        Socket_Descriptor["HOST"] = Host
        Socket_Descriptor["HOST ADDRESS"] = Host_Address
        return Socket_Descriptor
    else:
        raise ValueError("Socket already in use.")


def Send(Socket_Object, Data:bytes, Destination:str, Port:int):
    global Socket_in_existence
    if Socket_in_existence == True:
        Socket_Object.send(Data, (Destination, Port))
    else:
        return None


def Receive(Socket_Object, Buffer_Size:int):
    global Socket_in_existence
    if Socket_in_existence == True:
        Data = Socket_Object.recv(Buffer_Size)
        return Data
    else:
        return None


def Close(Socket_Object):
    global Socket_in_existence, Socket_Descriptor
    if Socket_in_existence == True:
        Socket_Object.shutdown(SHUT_RDWR)
        Socket_Object.close()
        Socket_Descriptor = Socket_Descriptor = {"SOCKET":None, "PORT":Port, "HOST":None, "HOST ADDRESS":""}
        Socket_in_existence = False
    else:
        return None



def CRC(Data:bytes, Exponents:list):
    Parsed_Data = []
    Output_Data = ""
    Shift_Space = max(Exponents)
    Binary_Data = str(bin(int(Data.hex(),16)<<Shift_Space)).replace('0b','')
    for Datum in Binary_Data:
        Parsed_Data.append(int(Datum,2))
    for Bit_Number in range(0,len(Parsed_Data) - Shift_Space,1):
        if Parsed_Data[Bit_Number] == 1:
            for Flipped_Bit in Exponents:
                Parsed_Data[Bit_Number + Shift_Space - Flipped_Bit] = int( not Parsed_Data[Bit_Number + Shift_Space - Flipped_Bit])
        else:
            pass
    for Bit_Counter in Parsed_Data[len(Parsed_Data) - Shift_Space:]:
        Output_Data += str(Bit_Counter)
    return b''.fromhex(str(hex(int(Output_Data,2))).replace('0x',''))
