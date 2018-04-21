import Ok_Analysis
from Ok_Funcs import *

"""
Using Decimal number 34050342 and convert it to binary
Dec: 34050342
Bin: 10000001111001000100100110
Will use this value to test bit_chop function
Total Bits: 26
"""


def test_bit_chop_00(): #Testing bit zero
    kwn = 0
    assert bit_chop(34050342,0,0,26) == kwn
    
def test_bit_chop_last():
    kwn = 1
    assert bit_chop(34050342, 25,25,26) == kwn
    
def test_bit_chop_14_20():
    kwn = int('0011110', 2)
    assert bit_chop(34050342, 20,14,26) == kwn
    
"""
Testing PipeOut_Assemble with a bytearray
"""