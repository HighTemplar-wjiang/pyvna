"""Created by Weiwei Jiang on 20170804.

This module includes a base class for manipulating VNA.

Todo:
    * Implement close() method.
"""

import sys
import visa


class VNA(object):
    """Base class for manipulating VNA with GPIB commands."""

    OK = 0
    """int: A status code indicating no error."""
    ERROR = -1
    """int: A status code indicating errors."""

    _resourceManager = 0
    _address = 0
    _vnaInst = 0

    def __init__(self):
        """Initialize resource manager from pyvisa."""
        self._resourceManager = visa.ResourceManager()

    def scan(self):
        """Scan and return all available VISA-enabled devices (a.k.a, resources)."""
        try:
            return self._resourceManager.list_resources()
        except Exception as exc:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def open(self, address):
        """Open a VISA-enabled device (a.k.a, resource) by its address.

        Args:
            address (str): The address of an resource to be opened.
        """
        try:
            self._vnaInst = self._resourceManager.open_resource(address)
            self._address = address
            return VNA.OK
        except Exception as exc:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def close(self):
        """Close all opened resources."""
        # TODO: implementation
        pass

    def write(self, strCommand):
        """Write a GPIB command string to the opened resource.

        Args:
            strCommand (str): A command string to be sent to the opened resource.
        """
        try:
            return self._vnaInst.write(strCommand)
        except Exception as exc:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def read(self, strCommand):
        """Read and return characters from the opened resource.

        Args:
            strCommand (str): A command string for reading characters.
        """
        try:
            return self._vnaInst.read(strCommand)
        except Exception as exc:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR

    def query(self, strCommand):
        """Write a GPIB command string to the opened resource, then read and return the characters from the resource.

        Args:
            strCommand (str): A command string for query.
        """
        try:
            return self._vnaInst.query(strCommand)
        except Exception as exc:
            print('Unexpected error:', sys.exc_info()[0])
            return VNA.ERROR


if __name__ == '__main__':

    import time

    objVNA = VNA()
    objVNA.open(objVNA.scan()[0])
    for idx in range(1,10):
        print("Measure at " + str(time.time()))
        data = objVNA.query("CALC:DATA:TRAC? 'Trc1', FDAT")
        print("Respond at " + str(time.time()) + ": " + str(data))
        #time.sleep(1e-2)

