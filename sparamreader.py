"""Created by Weiwei Jiang on 20171120

Read and plot S-parameters from VNA via GPIB
"""
import sys
from time import localtime, strftime
import numpy as np
from vna import VNA
import matplotlib.pyplot as plt


class ScatterParameterReader(VNA):
    """Read and plot S-parameters"""

    # setup parameters
    _traceNameReal = 'TRC_REAL_'
    _traceNameImag = 'TRC_IMAG_'
    _measurementParameters = ['S11', 'S12', 'S21', 'S22']
    _measurementFormatReal = 'REAL'  # pp.737
    _measurementFormatImag = 'IMAG'  # pp.737

    # initializing commands
    _resetDeviceCommand = "*RST"
    _delAllTracesCommand = "CALC1:PAR:DEL:ALL"

    # setup commands
    _newTraceCommand = "CALC1:PAR:SDEF \'{0}\', \'{1}\'"  # 0: trace name, 1: mea param
    _setMeasurementFormatCommand = "CALC1:FORM {0}"  # 0: trace name
    _displayTraceCommand = "DISP1:WIND:TRAC{0}:FEED \'{1}\'"  # 0: trace number 1: trace name
    _switchWindowCommand = "DISP1:WIND:STAT ON"  # turn on display window
    _setSweepType = "SENS1:SWE:TYPE {0}"  # 0: sweep type, e.g., LIN, SEGM, etc.

    # query commands
    _getStimulusCommand = "TRAC:STIM? CH1DATA"  # query stimulus data
    _getTraceCommand = "CALC1:DATA:TRAC? \'{0}\', FDAT"  # 0: trace name
    _avgEnableCommand = "SENS1:AVER {0}"  # 0: 'ON' or 'OFF'

    def __init__(self, measurementParameters=None):
        """ Initialize a class instance.

        Args:
             measurementParameters (list, optional): Parameters for measuring.
                Defaults to None, measuring S11, S12, S21, S22.
        """
        """Initialize parent class"""
        super(ScatterParameterReader, self).__init__()
        if measurementParameters:
            self._measurementParameters = measurementParameters

    @staticmethod
    def _check_status(status):
        """Static method to check VNA status

        Args:
            status (int): The status code to be checked

        Raises:
            Exception: Raise VNA error if VNA status is not OK
        """
        if status != VNA.OK:
            raise Exception("VNA error")
        else:
            pass

    def init(self, address=None):
        """Initiate VNA remote control

        Args:
            address (str, optional): The address of an resource to be opened.
                Defaults to None, open the first scanned VISA-enabled devices.
        """
        if address is None:
            if __debug__:
                print("Warning: Automatically connect to the first device in the visa-enabled device list.")
            self.open(self.scan()[0])
        else:
            self.open(address)

    def setup(self):
        """Setup the VNA.

        The VNA will be set with S11-real and S11-imag traces

        Returns:
            int: A VNA status code
        """
        try:
            # init device
            # self.write(ScatterParameterReader._resetDeviceCommand)  # reset device
            self.write(ScatterParameterReader._delAllTracesCommand)  # delete all traces
            if __debug__:
                print("Info: Device initialization done.")
                print("Info: Setting traces.")

            for idx, parameter in enumerate(self._measurementParameters):
                # set s-real trace
                self.write(ScatterParameterReader._newTraceCommand.format(
                    self._traceNameReal+parameter, parameter))  # add trace
                self.write(
                    ScatterParameterReader._setMeasurementFormatCommand.format(self._measurementFormatReal))  # set measurement format
                self.write(ScatterParameterReader._displayTraceCommand.format(11+idx*2, self._traceNameReal+parameter))  # display trace

                # set s-imag trace
                self.write(ScatterParameterReader._newTraceCommand.format(
                    self._traceNameImag+parameter, parameter))  # add trace
                self.write(
                    ScatterParameterReader._setMeasurementFormatCommand.format(
                        self._measurementFormatImag))  # set measurement format
                self.write(ScatterParameterReader._displayTraceCommand.format(12+idx*2, self._traceNameImag+parameter))  # display trace

            # set sweep segments
            if __debug__:
                print("Info: Device setup done, please calibrate the VNA and continue...")

            return VNA.OK
        except Exception as e:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def get_stimulus(self):
        """Get frequencies of stimulus signals from the VNA

        Returns:
            str, int: Frequencies separated by comma. Return an error code if fails
        """
        try:
            data = self.query(ScatterParameterReader._getStimulusCommand)
            return np.array([float(num) for num in data.split(',')])
        except Exception as e:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def get_trace(self):
        """Get trace data from VNA

        Returns:
            (tuple): A tuple containing:

                - **dataReal** (*numpy.array*): Real part of S-parameters
                - **dataImag** (*numpy.array*): Imaginary part of S-parameters
        """
        try:
            return_data = {}
            for idx, parameter in enumerate(self._measurementParameters):
                dataReal = self.query(ScatterParameterReader._getTraceCommand.format(self._traceNameReal+parameter))
                dataImag = self.query(ScatterParameterReader._getTraceCommand.format(self._traceNameImag+parameter))
                return_data.update({parameter+"_real": [float(num) for num in dataReal.split(',')]})
                return_data.update({parameter+"_imag": [float(num) for num in dataImag.split(',')]})
            return return_data
        except Exception as e:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def read_and_plot(self):
        """Read and plot S-parameters."""

        # query data
        freqList = self.get_stimulus()
        data = self.get_trace()

        # log data
        timeStr = strftime("%Y%m%d_%H%M%S", localtime())
        filename = input("Input filename for saving data (default {}): ".format(timeStr))
        if not filename:
            filename = timeStr
        with open("./data/{}.csv".format(filename), "w+") as logfile:
            # Write head.
            logfile.write("Freq")
            for parameter in self._measurementParameters:
                logfile.write(",{0}_real,{0}_imag".format(parameter))
            logfile.write("\n")
            # Write data.
            for idx in range(len(freqList)):
                logfile.write("{}".format(freqList[idx]))
                for parameter in self._measurementParameters:
                    logfile.write(",{},{}".format(data[parameter+"_real"][idx], data[parameter+"_imag"][idx]))
                logfile.write("\n")
        
        # Plot all parameters.
        plt.close("all")
        for parameter in self._measurementParameters:
            plt.figure()
            plt.plot(freqList / 1e6, data[parameter+"_real"])
            plt.plot(freqList / 1e6, data[parameter+"_imag"])
            plt.title(parameter)
            plt.legend(['Real', 'Imag'])
            plt.xlabel('Frequency (MHz)')

        print("Close all figures to continue...")
        plt.show()


if __name__ == '__main__':
    reader = ScatterParameterReader()

    reader.init()
    reader.setup()

    input()

    while(True):
        reader.read_and_plot()
        x = input("Input q to quit, any other key(s) for another measurement: ")
        if x == 'q':
            break

    reader.close()
