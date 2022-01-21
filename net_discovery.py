import logging
import time
from multiprocessing.dummy import Pool as threadpool
import app_logger

from pythonping import ping  # https://github.com/alessandromaggio/pythonping
# from getmac import get_mac_address  #https://github.com/GhostofGoes/getmac
# i used arpreq instead of getmac because socket.gethostbyname() after getmac is wrong!

import arpreq
from constants import *


# -------------------------------------------------
logger = app_logger.get_logger(__name__)
if DEBUG:
    logger.setLevel(logging.DEBUG)
# -------------------------------------------------
def discover(device):
    ip = device["ip"]
    try:
        logger.debug(f'ping ip: {ip}')
        response = ping(ip)
        logger.debug(f'result ping ip: {ip} = {response.success()}')
    except Exception as e:
        logger.error('ping error: %s' % e)
        return False
    try:
        logger.debug(f'get mac ip: {ip}')
        device["mac"] = arpreq.arpreq(ip)
        logger.debug(f'result get mac ip: {ip} {device["mac"]}')
    except Exception as e:
        logger.error('get mac error: %s' % e)

    device["last_discovery"] = int(time.time() * 1000)
    if response.success():
        logger.debug(f'device ip:{ip} is Online')
        device["last_online"] = int(time.time() * 1000)
        device["status"] = ONLINE_STATE
    else:
        logger.debug(f'device ip:{ip} is Offline')
        device["status"] = OFFLINE_STATE

    return response.success()
# -------------------------------------------------
def do_discovery(devices):
    logger.debug(f'Run discovery with pool size:{DISCOVERY_WORKER_POOL}')
    with threadpool(DISCOVERY_WORKER_POOL) as pool:
        pool.map(discover, devices)
    logger.debug(f'End discovery with pool size:{DISCOVERY_WORKER_POOL}')
# -------------------------------------------------

