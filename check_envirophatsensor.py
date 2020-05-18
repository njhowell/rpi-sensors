#!/usr/bin/python3

from envirophat import weather, light
import envirophatconfig
from datetime import datetime
import sys
import getopt

def main(argv):
    tempwarn = ''
    tempcrit = ''
    lightwarn = ''
    lightcrit = ''
    try:
        opts, args = getopt.getopt(argv, "hw:c:W:C:", ["tempwarn=","tempcrit=","lightwarn=","lightcrit="])
    except getopt.GetoptError:
        print("check_envirophatsensor.py --tempwarn=<warn> --tempcrit=<crit> --lightwarn=<warn> --lightcrit=<crit>")
        sys.exit(3)

    for opt, arg in opts:
        if opt == '-h':
            print("check_envirophatsensor.py --tempwarn=<warn> --tempcrit=<crit> --lightwarn=<warn> --lightcrit=<crit>")
            sys.exit()
        elif opt in ("-w", "--tempwarn="):
            tempwarn = arg
        elif opt in ("-c", "--tempcrit="):
            tempcrit = arg
        elif opt in ("-W", "--lightwarn="):
            lightwarn = arg
        elif opt in ("-C", "--lightcrit="):
            lightcrit = arg


    temp = weather.temperature()-6
    lightlevel = light.light()
    temp_message = ''
    light_message = ''
    exitcode = 0

    if tempwarn != '' and float(tempwarn) < temp:
        exitcode = 1
        temp_message = 'WARNING: Temperature is above warning threshold. '

    if tempcrit != '' and float(tempcrit) < temp:
        exitcode = 2
        temp_message = 'CRITICAL: Temperature is above critical threshold. '

    if lightwarn != '' and float(lightwarn) < lightlevel:
        if exitcode < 1:
            exitcode = 1
        light_message = 'WARNING: Light level is above warning threshold. '

    if lightcrit != '' and float(lightcrit) < lightlevel:
        exitcode = 2
        light_message = 'CRITICAL: Light level is above critical threshold. '

    exit_message = light_message + temp_message
    if exit_message == '':
        exit_message = 'OK: Everything is fine. Temp is ' + str(temp) + '  and Light is ' + str(lightlevel)
        exitcode = 0

    print(exit_message + '|temperature='+str(temp)+';'+tempwarn+';'+tempcrit+';; lightlevel='+str(lightlevel)+';'+lightwarn+';'+lightcrit+';;')
    sys.exit(exitcode)


if __name__ == "__main__":
    main(sys.argv[1:])
