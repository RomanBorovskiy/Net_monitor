import logging
import time
from flask import Flask, make_response, jsonify, render_template
import json
import datetime
from constants import *
import app_logger
from net_discovery import do_discovery
import threading
#-------------------------------------------------
# its array of devices if devices.json not found - useful for testing.
# "monitoring" - is not using now, except old tempate index.html with route '../old'

devices = [
    {"name" : "router", "ip": "192.168.2.1", "monitoring": 'enable'},
    {"name": "nas", "ip": "192.168.2.202", "monitoring": 'enable'},
    {"name": "raspi", "ip": "192.168.2.200", "monitoring": 'enable'}
]

app = Flask(__name__, static_url_path='/static', static_folder=os.path.join(WEB_DIR, "static"),
            template_folder=WEB_DIR)
logger = app_logger.get_logger(__name__)
logger.info(f'Logger level key DEBUG={DEBUG}')

if DEBUG:
    logger.setLevel(logging.DEBUG)

logger.debug(f' DEBUG key is {DEBUG}')




#-------------------------------------------------
def run_discovery_loop(devices):
    ''' run thread with discovery every DISCOVERY_PERIOD_SEC '''
    def loop():
        while True:
            try:
                do_discovery(devices)
            except Exception as e:

                logger.error("ERROR DISCOVERY LOOP: %s"% e)
            time.sleep(DISCOVERY_PERIOD_SEC)

    logger.info(f'Run discovery thread with DISCOVERY_PERIOD_SEC={DISCOVERY_PERIOD_SEC}')
    threading.Thread(target=loop, args=(), daemon=True).start()
#-------------------------------------------------

def pretty_datetime(data):
    """ convert data from timestamp to string Day.Month.Year Hours:Minutes:Seconds"""
    if 0 == data:
        return "-"
    try:
        return datetime.datetime.fromtimestamp(int(data)).strftime("%d.%m.%Y %H:%M:%S")
    except Exception as e:
        logger.error("Cannot format for datetime: %s data = %s" % (str(e), data))
    return "-"
#-------------------------------------------------
#load list of devices from json file
def load_devices():
    logger.info('Load devices from json file')
    try:
        with open(os.path.join(CONFIG_DIR, DEVICES_FILE),'r') as jsn:
            dev_lst = json.load(jsn)
    except Exception as e:
        logger.error("Error open file json with devices: %s" % str(e))
        return None

    return dev_lst
#-------------------------------------------------
# create devices with IP addr 192.168.2.1 -192.168.2.254 - for testing only
def add_devices():
    for i in range(1,254):
        ip = '192.168.2.' + str(i)
        name = 'device_' + str(i)
        devices.append({"type":"dummy", "name":name, "ip":ip, "monitoring":"enable"})

# -------------------------------------------------
# create json file with devices - not used in app. I used it for testing and create file from array
def save_devices():
    with open(os.path.join(RESOURCES_DIR, DEVICES_FILE), 'w') as jsn:
        json.dump(devices, jsn, indent = 4)

#-------------------------------------------------
@app.route('/old')
def html_js():
    data = dict(devices=devices[:])
    for dev in data["devices"]:
        dev["str_last_discovery"] = pretty_datetime(dev.get("last_discovery",0)/1000)
        dev["str_last_online"] = pretty_datetime(dev.get("last_online",0)/1000)
    return render_template("index.html", **data)
#-------------------------------------------------
@app.route('/')
def root():
    return render_template("dev_mon.html")
#-------------------------------------------------
@app.route('/api/devices')
def list_devices():
    # TODO it's safe with threading?
    return jsonify(devices)
#-------------------------------------------------
def init_devices_list():
# bad style - global var 'devices' used))
    jsn_devices = load_devices()
    if jsn_devices:
        devices.clear()
        devices.extend(jsn_devices)
    else:
        add_devices()
#-----------START----------------------------------

init_devices_list()
run_discovery_loop(devices)

#-------------------------------------------------

if __name__ == "__main__":

    logger.info('Runing web server')
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)
