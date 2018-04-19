"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API. 

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test

"""

"""
bitchop function
Takes 
"""
def bitchop(Data, msb, lsb, Total_Bits):
    Buffer_bits = str(bin(Data)[2:])
    Reverse_bits = str(Buffer_bits[::-1])
    Remaining_bits = Total_Bits - len(Reverse_bits)
    for i in range(Remaining_bits):
        Reverse_bits += '0'
    output = str(Reverse_bits[lsb:msb+1])
    
    return int(output[::-1],2)
