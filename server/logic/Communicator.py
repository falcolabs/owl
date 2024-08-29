import socket

def CRC(Input:bytes,Exponents:list) -> "This function generates CRC remainder.":
    Digit_List = []
    Output_String = ""
    Output_Bytes = b''

    Shift_Space = max(Exponents)

    Shifted_Binary_Input_String = str(bin(int(Input.hex(),16)<<Shift_Space)).replace('0b','')

    for String_digit in Shifted_Binary_Input_String:
        Digit_List.append(int(String_digit,2))
    
    Digit_index = 0
    while Digit_index < len(Digit_List) - Shift_Space:
        if Digit_List[Digit_index] == 1:
            for Flipped_bit in Exponents:
                Digit_List[Digit_index + Shift_Space - Flipped_bit] = int(not Digit_List[Digit_index + Shift_Space - Flipped_bit])
        Digit_index += 1

    for Digit in Digit_List:
        Output_String += str(Digit)
    
    return Input + Output_Bytes.fromhex(hex(int(Output_String,2)).replace('0x',''))

def Communicate(message:bytes,port:int,buffersize:int, source:str,destination:str,rw:bool) -> "This function communicates using UDP.":
    '''
    When rw is set to True, this function sends data, and no source address is needed.
    When rw is set to False, this function receives data, and no destination address is needed.
    '''
    Communicating_object = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    if rw == True:
        Communicating_object.sendto(message,(destination,port))
    elif rw == False:
        Communicating_object.bind((source,port))
        Data, Peer_address = Communicating_object.recvfrom(buffersize)
    else:
        Communicating_object.shutdown(SHUT_RDWR)
        Communicating_object.close()
    if rw == True:
        return True
    elif rw == False:
        return Data
    else:
        return None
