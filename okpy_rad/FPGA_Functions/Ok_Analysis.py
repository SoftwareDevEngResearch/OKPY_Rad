"""
Analysis functions

Provides analysis functions for radiation detector data that has been read
from the FPGA. This module will not have functions that require the system to be
connected to a PC.
"""

#from __future__ import division, print_function
import numpy as np


#Here is  Change



def bit_chop(Data, msb, lsb, Total_Bits):
    """
    bit_chop function
    Takes decimal number and converts it into binary. User selects which bits are
    desired and returns a decimal number.

    Data(int): Full decimal number
    msb(int): Most significant bit of desired number
    lsb(int): least signficant bit of desired number
    Total Bits(int): Totals bits of signal that is being read. Related to Opal Kelly's
                     wireout data. Number of bits should be established in VHDL.
    """
    if msb < lsb:

        print "msb variable must be larger than lsb"
        return None
    Buffer_bits = str(bin(Data)[2:])
    Reverse_bits = str(Buffer_bits[::-1])
    Remaining_bits = Total_Bits - len(Reverse_bits)
    for i in range(Remaining_bits):
        Reverse_bits += '0'
    output = str(Reverse_bits[lsb:msb+1])

    return int(output[::-1],2)


def pipeout_assemble(Data, Bytes):
    """
    Pipeout assemble function
    Applies Opal Kelly's PipeOut read function and assembles the data
    into the appropriate array.

    Data(bytearray): PipeRead data from the Opal Kelly Function
    Bytes(int): Number of Bytes in each read (4 bytes for current FPGA board)

    Notes on Data:
        A bytearray wih form  "bytearray(b'\x00\x00...etc)
        The ReadFromPipeOut (Opal Kelly Funcation) reads out 4 byte chunks
        -- or 32 bits of data. This corresponds to four entries of the bytearray.
        If the ReadFromPipeOut reads with different amount bytes it will need
        to be adjusted.

    Returns array of assembled data
    """
    Buffer = bytes(Data)
    Buffer_Reverse = Buffer[::-1]
    Samples = len(Buffer)/Bytes #Should correspond to how many bytes are in each pipe out read
    Output_Reversed = [] #Output must be reversed to account for the way OK reads in data

    for i in range(Samples):
        #Convert the specified "byte chunks" into an interger and add to array
        Output_Reversed.append(int(Buffer_Reverse[(i*4):4+(i*4)].encode('hex'),16))
    result = Output_Reversed[::-1]
    return result

"""
Detection of peaks for gamma spectrum. Author of code is cited.
"""


__author__ = "Marcos Duarte, https://github.com/demotu/BMC"
__version__ = "1.0.4"
__license__ = "MIT"


def detect_peaks(x, mph=None, mpd=1, threshold=0, edge='rising',
                 kpsh=False, valley=False, show=False, ax=None):

    """Detect peaks in data based on their amplitude and other features.

    Parameters
    ----------
    x : 1D array_like
        data.
    mph : {None, number}, optional (default = None)
        detect peaks that are greater than minimum peak height.
    mpd : positive integer, optional (default = 1)
        detect peaks that are at least separated by minimum peak distance (in
        number of data).
    threshold : positive number, optional (default = 0)
        detect peaks (valleys) that are greater (smaller) than `threshold`
        in relation to their immediate neighbors.
    edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
        for a flat peak, keep only the rising edge ('rising'), only the
        falling edge ('falling'), both edges ('both'), or don't detect a
        flat peak (None).
    kpsh : bool, optional (default = False)
        keep peaks with same height even if they are closer than `mpd`.
    valley : bool, optional (default = False)
        if True (1), detect valleys (local minima) instead of peaks.
    show : bool, optional (default = False)
        if True (1), plot data in matplotlib figure.
    ax : a matplotlib.axes.Axes instance, optional (default = None).

    Returns
    -------
    ind : 1D array_like
        indeces of the peaks in `x`.

    Notes
    -----
    The detection of valleys instead of peaks is performed internally by simply
    negating the data: `ind_valleys = detect_peaks(-x)`

    The function can handle NaN's

    See this IPython Notebook [1]_.

    References
    ----------
    .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

    Examples
    --------
    >>> from detect_peaks import detect_peaks
    >>> x = np.random.randn(100)
    >>> x[60:81] = np.nan
    >>> # detect all peaks and plot data
    >>> ind = detect_peaks(x, show=True)
    >>> print(ind)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # set minimum peak height = 0 and minimum peak distance = 20
    >>> detect_peaks(x, mph=0, mpd=20, show=True)

    >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
    >>> # set minimum peak distance = 2
    >>> detect_peaks(x, mpd=2, show=True)

    >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
    >>> # detection of valleys instead of peaks
    >>> detect_peaks(x, mph=0, mpd=20, valley=True, show=True)

    >>> x = [0, 1, 1, 0, 1, 1, 0]
    >>> # detect both edges
    >>> detect_peaks(x, edge='both', show=True)

    >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
    >>> # set threshold = 2
    >>> detect_peaks(x, threshold = 2, show=True)
    """

    x = np.atleast_1d(x).astype('float64')
    if x.size < 3:
        return np.array([], dtype=int)
    if valley:
        x = -x
    # find indices of all peaks
    dx = x[1:] - x[:-1]
    # handle NaN's
    indnan = np.where(np.isnan(x))[0]
    if indnan.size:
        x[indnan] = np.inf
        dx[np.where(np.isnan(dx))[0]] = np.inf
    ine, ire, ife = np.array([[], [], []], dtype=int)
    if not edge:
        ine = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
    else:
        if edge.lower() in ['rising', 'both']:
            ire = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
        if edge.lower() in ['falling', 'both']:
            ife = np.where((np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
    ind = np.unique(np.hstack((ine, ire, ife)))
    # handle NaN's
    if ind.size and indnan.size:
        # NaN's and values close to NaN's cannot be peaks
        ind = ind[np.in1d(ind, np.unique(np.hstack((indnan, indnan-1, indnan+1))), invert=True)]
    # first and last values of x cannot be peaks
    if ind.size and ind[0] == 0:
        ind = ind[1:]
    if ind.size and ind[-1] == x.size-1:
        ind = ind[:-1]
    # remove peaks < minimum peak height
    if ind.size and mph is not None:
        ind = ind[x[ind] >= mph]
    # remove peaks - neighbors < threshold
    if ind.size and threshold > 0:
        dx = np.min(np.vstack([x[ind]-x[ind-1], x[ind]-x[ind+1]]), axis=0)
        ind = np.delete(ind, np.where(dx < threshold)[0])
    # detect small peaks closer than minimum peak distance
    if ind.size and mpd > 1:
        ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
        idel = np.zeros(ind.size, dtype=bool)
        for i in range(ind.size):
            if not idel[i]:
                # keep peaks with the same height if kpsh is True
                idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                    & (x[ind[i]] > x[ind] if kpsh else True)
                idel[i] = 0  # Keep current peak
        # remove the small peaks and sort back the indices by their occurrence
        ind = np.sort(ind[~idel])

    if show:
        if indnan.size:
            x[indnan] = np.nan
        if valley:
            x = -x
        _plot(x, mph, mpd, threshold, edge, valley, ax, ind)

    return ind

    def determine_polarity(data):
        """Determines if pulses have positive or negative polarity

        data(list, numbers) : array of numbers representing the pulse


        """
        pass
