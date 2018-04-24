"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API.

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test

"""

"""
bit_chop function
Takes decimal number and converts it into binary. User selects which bits are
desired and returns a decimal number.

Data: Full decimal number
msb: Most significant bit of desired number
lsb: least signficant bit of desired number
Total Bits: Totals bits of signal that is being read. Related to Opal Kelly's
wireout data. Number of bits should be established in VHDL.
"""
def bit_chop(Data, msb, lsb, Total_Bits):
    Buffer_bits = str(bin(Data)[2:])
    Reverse_bits = str(Buffer_bits[::-1])
    Remaining_bits = Total_Bits - len(Reverse_bits)
    for i in range(Remaining_bits):
        Reverse_bits += '0'
    output = str(Reverse_bits[lsb:msb+1])

    return int(output[::-1],2)

"""
Pipeout assemble function
Applies Opal Kelly's PipeOut read function and assembles the data
into the appropriate array.
Data: PipeRead data from the Opal Kelly Function
Bytes: Number of Bytes in each read (4 bytes for current FPGA board)

Notes on Data:
    A bytearray wih form  "bytearray(b'\x00\x00...etc)
    The ReadFromPipeOut (Opal Kelly Funcation) reads out 4 byte chunks 
    -- or 32 bits of data. This corresponds to four entries of the bytearray. 
    If the ReadFromPipeOut reads with different amount bytes it will need
    to be adjusted.

Returns array of assembled data
"""
def pipeout_assemble(Data, Bytes):
    Buffer = bytes(Data)
    Buffer_Reverse = Buffer[::-1]
    Samples = len(Buffer)/Bytes #Should correspond to how many bytes are in each pipe out read
    Output_Reversed = [] #Bytes had to be reversed to correctly translate bytes

    for i in range(Samples):
        Output_Reversed.append(int(Buffer_Reverse[(i*4):4+(i*4)].encode('hex'),16))
    result = Output_Reversed[::-1]
    return result

    
