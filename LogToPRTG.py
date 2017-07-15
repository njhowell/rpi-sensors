import logging
import requests
logging.getLogger(__name__)

def LogValue(sensorname, value, api_key, port, prtg_host, ssl):
    if ssl:
        url_scheme = 'https'
    else:
        url_scheme = 'http'

    json_response = {
        "prtg": {
            "result": [
                {
                     "channel": sensorname,
                     "float": 1,
                     "value": value
                }
            ]
        }
    }

    json_string = str(json_response)
    json_string = str.replace(json_string, '\'','\"')
    prtg_request_URL = url_scheme + '://' + prtg_host + ':' + port + '/' + api_key +'?content=' + json_string
    complete_url = prtg_request_URL
    logging.info("Logging value %s for sensor %s using URL %s", value, sensorname, complete_url)
    request = requests.get(prtg_request_URL)
    logging.debug("Request response: %s", request)
