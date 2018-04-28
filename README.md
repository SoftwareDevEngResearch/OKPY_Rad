# OKPY_Rad
Using Opal Kelly Python API to interface with FPGAs with a focus on Radiation Detection.


The RadDevice class is used to connect a FPGA Opal Kelly board with the intent to
utilize it for radiation detection. The class accepts "settings_file" for updating
parameters within the FPGA. These can include filter parameters, run mode, and other
necessary settings that to properly run the VHDL design. This is specifically
for Opal Kellys SetWireInValue method. The settings file should be formatted as follows:

[WireAddress(int), Value(int), WireType(int)]

WireType Description:
---------------------
0: WireIn
1: TrigIn

Additional WireType will be included in future versions of the code.
