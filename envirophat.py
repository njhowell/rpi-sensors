from envirophat import weather, light
import LogToPRTG
import envirophatconfig
import time
import logging

interval = 60

logging.basicConfig(filename='/var/log/sensors.log',level=logging.DEBUG)

logging.info("Starting up")

while True:
    temp = weather.temperature()-10 
    logging.info("Got temperature of %s", str(temp))
    
    light = light.light()
    logging.info("Got light level of %s", str(light))
    
    LogToPRTG.LogValue("Temperature", str(temp), envirophatconfig.temp_api_key, envirophatconfig.temp_port, envirophatconfig.prtg_host, envirophatconfig.use_ssl)
    logging.info("Logged temperature with PRTG at %s using apikey %s", envirophatconfig.prtg_host, envirophatconfig.temp_api_key)

    LogToPRTG.LogValue("Light Level", str(light), envirophatconfig.light_api_key, envirophatconfig.light_port, envirophatconfig.prtg_host, envirophatconfig.use_ssl)
    logging.info("Logged light level with PRTG at %s using apikey %s", envirophatconfig.prtg_host, envirophatconfig.light_api_key)

    logging.info("Going to sleep for %s seconds", interval)
    time.sleep(interval)
