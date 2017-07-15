import serial
from time import sleep, asctime
import time
from datetime import datetime
import math
import urllib2
import logging
import requests

import LogToPRTG
import WirelessSensorConfig

port = '/dev/ttyAMA0'
baud = 9600

logging.basicConfig(filename='/var/log/sensors.log',level=logging.DEBUG)


def CalculateTemp(adc_value):
    BVAL = 3977
    RTEMP = 25.0 + 273.15
    RNOM = 10000.0
    SRES = 10000.0
    if adc_value == 0:
        adc_value = 0.001
    Rtherm = (1023.0/float(adc_value) -1)*10000
    kelvin = RTEMP*BVAL/(BVAL+RTEMP*(math.log(Rtherm/RNOM)))
    temperature = kelvin - 273.15
    temp = round(temperature*100)
    temp = temp/100
    return temp


def CheckForData():
    global port
    global baud
    global prtg_host
    global temp_port
    global temp_api_key
    global light_api_key
    global light_port
    global use_ssl
    logging.debug("Opening Serial port %s with baud rate %s", port, baud)
    ser = serial.Serial(port=port, baudrate=baud)
    sleep(0.2)
    ser.flushInput()

    logging.info("Requesting values for input A00")
    ser.write('aAAA00READ--')
    sleep(0.2)
    logging.info("Requesting value for input A01")
    ser.write('aAAA01READ--')
    sleep(0.2)

    logging.info("Checking for response")
    while ser.inWaiting():
        char = ser.read()
        if char == 'a':
            llapMsg = 'a'
            llapMsg += ser.read(11)
            logging.debug("received message %s", llapMsg)
            devID = llapMsg[1:3]
            data = llapMsg[3:]
            if devID == 'AA':
                if data.startswith('A00'):
                    logging.info("received message for input A00")
                    adc = int(data[4:].strip('-'))
                    temp = CalculateTemp(adc)
                    logging.debug("Temperature calculated at %s", str(temp))
                    LogValue("Temperature", str(temp), temp_api_key, temp_port, prtg_host, use_ssl)

                elif data.startswith('A01'):
                    logging.info("received message for input A01")
                    adc = int(data[4:].strip('-'))
                    lightpc = (float(adc) / 1023) * 100
                    logging.debug("light value calculated at %s", str(lightpc))
                    LogValue("Light Level", str(lightpc), light_api_key, light_port, prtg_host, use_ssl)

    ser.close()


logging.info("Starting up at %s", datetime.now())
starttime = time.time()
while True:
    logging.info("Checking for data at %s", datetime.now())
    CheckForData()
    sleep(30.0 - ((time.time() - starttime) % 30.0))


logging.info("Process complete at %s", datetime.now())
