"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API.

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test. This also requires the "ok" package to be imported from Opal Kelly.
An error will occur if the appropriate package is not imported.

"""
import ok
from tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename

class OSU_Rad_Device():
    """
    Class to designate FPGA systems at Oregon State University to connect them
    via the USB.
    """

    def __init__(self):
        #self.device = self.connect_device()
        pass

    """
    connect_device:
    Simple function to create an object of the connected FPGA device. Opens
    Tkinter window for user to select Bit_File to program the FPGA. The window
    then closes and programs the FPGA. Also checks for errors.

    """
    def connect_device(self):
        self.xem = ok.okCFrontPanel()
        self.xem.OpenBySerial("")
        root = Tk()
        root.update()
        Bit_File = askopenfilename()
        root.update()
        root.destroy()
        self.xem.ConfigureFPGA(str(Bit_File))
        return None
