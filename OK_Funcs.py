"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API.

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test. This also requires the "ok" package to be imported from Opal Kelly.
An error will occur if the appropriate package is not imported.

"""
import ok
import tkinter


class OSU_Rad_Device(device):
    """
    Class to designate FPGA systems at Oregon State University to connect them
    via the USB.
    """

    def __init__(self):
        self.device = device

    """
    connect_device:
    Simple function to create an object of the connected FPGA device. Will use This

    """
    def connect_device(self):
        xem = ok.okCFrontPanel()
        xem.OpenBySerial("")
        return xem
