import numpy as np
import math
from Ok_Analysis import *
from Ok_Funcs import *
import random
"""
TESTING BIT_CHOP FUNCTION
Using Decimal number 34050342 and convert it to binary
Dec: 34050342
Bin: 10000001111001000100100110
Will use this value to test bit_chop function
Total Bits: 26

Bit counting starts at '0' from the far right
"""


def test_bit_chop_00(): #Testing bit zero
    kwn = 0
    assert bit_chop(34050342,0,0,26) == kwn

#Testing the last bit
def test_bit_chop_last():
    kwn = 1
    assert bit_chop(34050342, 25,25,26) == kwn

#Testings bits 14 to 20
def test_bit_chop_14_20():
    kwn = int('0011110', 2)
    assert bit_chop(34050342, 20,14,26) == kwn

"""
Testing PipeOut_Assemble with a bytearray:
    Definite a function to create a bytearray with hex values. These values will
    be limited to 32 bit numbers to emulate the ReadFromPipeOut function from
    Opal Kelly.
"""

def create_byte_array_hex(array_length):
    Data = bytearray() #Create Empty bytearray
    Value_Array = []
    Value_Array_Str = []
    for i in range(array_length):
        Value_Array.append(bin(random.randint(0,10000))[2:])
        Value_Array_Str.append('')
    #Split into 32 bit Chunks
    for i in range(len(Value_Array)):
        #Pad with 0's to ensure 32-bits

        Value_Array_Str[i] = 32%len(Value_Array[i]) *'0' + str(Value_Array[i])
        while len(Value_Array_Str[i]) < 32:
            Value_Array_Str[i] = '0' + str(Value_Array_Str[i])
        for q in range(4):
            Data.append(int(Value_Array_Str[i][(q*8):8+(q*8)],2))
    print Data
    return Value_Array_Str, Data[::-1]

def test_pipe_assemble():
    #data = bytearray()
    obs,data = create_byte_array_hex(4) #Change this value to make longer arrays
    est = Pipeout_Assemble(data, 4)
#    print "Actual"
#    print obs
#    print "Actual Byte Array"
#    print data
#    print "PipeOut Assemble Results"
#    print est
    est = est[::-1]
    for i in range(len(obs)):
        print "Testing Value Number %f" %i
        assert est[i] == int(obs[i],2)

"""
TESTING DETECT PEAK FUNCTION

First create a function to generate an array for gaussian
"""

def gaussian(x, mu, sig):
    return (float(1)/math.sqrt(2*math.pi*sig**2))*np.exp(-((x-mu)**2)/(2*sig**2))



def test_detect_peaks():
    #First create gaussian data
    x_1 = np.linspace(0,100,1000)
    mu_1 = 20
    sig_1 = .5
    y_1 = [gaussian(i,mu_1,sig_1) for i in x_1]
    x_2 = np.linspace(100,200,1000)
    mu_2 = 140
    sig_2 = 0.5
    y_2 = [gaussian(i,mu_2,sig_2) for i in x_2]
    y = y_1 + y_2
    x = x_1 + x_2
    mu = [mu_1, mu_2]

    print detect_peaks(y)
    print detect_peaks(y)[0]/float(10)
    print len(y)
    #Compare each mu with indx from test_detect_peaks
    #Must divide index by 10 to account for aditional numbers
    #Created by linspace
    for i in range(len(mu)):
       assert np.allclose(detect_peaks(y)[i]/float(10), mu[i])
test_detect_peaks()
