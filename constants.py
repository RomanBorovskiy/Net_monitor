import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
WEB_DIR = os.path.join(RESOURCES_DIR, "web")
CONFIG_DIR = os.path.join(BASE_DIR, "config")

OFFLINE_STATE = "offline"
ONLINE_STATE = "online"

DEVICES_FILE = 'devices.json'
LOG_FILE = "discovery.log"

DISCOVERY_PERIOD_SEC = int(os.getenv("DISCOVERY_PERIOD_SEC", default=30))
DISCOVERY_WORKER_POOL = int(os.getenv("DISCOVERY_WORKER_POOL", default=10))
DEBUG = int(os.getenv("DEBUG", default=1))

