#!/usr/bin/env python
# Author: Jon Trulson <jtrulson@ics.com>
# Copyright (c) 2016 Intel Corporation.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function
import time, sys, signal, atexit
from upm import pyupm_t8100 as sensorObj

def main():
    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting...")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    # You will need to edit this example to conform to your site and your
    # devices, specifically the Device Object Instance ID passed to the
    # constructor, and the arguments to initMaster() that are
    # appropriate for your BACnet network.

    defaultDev = "/dev/ttyUSB0"

    # if an argument was specified, use it as the device instead
    if (len(sys.argv) > 1):
        defaultDev = sys.argv[1]

    print("Using device", defaultDev)
    print("Initializing...")

    # Instantiate an T8100 object for an T8100 device that has 568000
    # as it's unique Device Object Instance ID.  NOTE: You will
    # certainly want to change this to the correct value for your
    # device(s).
    sensor = sensorObj.T8100(568000)

    # Initialize our BACnet master, if it has not already been
    # initialized, with the device and baudrate, choosing 1000001 as
    # our unique Device Object Instance ID, 2 as our MAC address and
    # using default values for maxMaster and maxInfoFrames
    sensor.initMaster(defaultDev, 38400, 1000001, 2)

    # Uncomment to enable debugging output
    # sensor.setDebug(True);

    # output the serial number and firmware revision
    print()
    print("Device Description:", sensor.getDeviceDescription())
    print("Device Location:", sensor.getDeviceLocation())
    print()

    # update and print available values every 5 seconds
    while (1):
        # update our values
        sensor.update();

        print("CO2 Concentration:", end=' ')
        print(sensor.getCO2(), end=' ')
        print("ppm")

        # we show both C and F for temperature
        print("Temperature:", sensor.getTemperature(), end=' ')
        print("C /", sensor.getTemperature(True), "F")

        print("Humidity:", end=' ')
        print(sensor.getHumidity(), end=' ')
        print("%RH")

        print("Relay State:", end=' ')
        print(sensor.getRelayState())

        print()
        time.sleep(5)

if __name__ == '__main__':
    main()
