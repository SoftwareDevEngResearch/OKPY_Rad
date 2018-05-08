"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API.

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test. This also requires the "ok" package to be imported from Opal Kelly.
An error will occur if the appropriate package is not imported.

"""
#import ok
from tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from Ok_Analysis import *
import csv
import os

class RadDevice():
    """
    Class to designate FPGA systems at Oregon State University to connect them
    via the USB.
    """

    def __init__(self):
        pass
        #self.xem = ok.okCFrontPanel()
        #self.xem.OpenBySerial("")


    def program_device(self):
        """
        program_device:
        Simple function to create an object of the connected FPGA device. Opens
        Tkinter window for user to select Bit_File to program the FPGA. The window
        then closes and programs the FPGA. Also checks for errors.
        """
        root = Tk()
        root.update()
        Bit_File = askopenfilename()
        root.update()
        root.destroy()
        self.xem.ConfigureFPGA(str(Bit_File))
        return None

    def auto_update_settings(self):
        """Grabs file to update a series of WireIns from Opal Kelly   """
        file_dir = os.path.join(os.getcwd(), 'settings.csv')
        wire_in = []
        trigger_in = []
        with open(file_dir, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ',')
            for row in spamreader:
                if row[-1] == 0:
                    wire_in.append(map(int,row))
                elif row[-1] == 1:
                    trigger_in.append(map(int,row))
        print wire_in
        print trigger_in
