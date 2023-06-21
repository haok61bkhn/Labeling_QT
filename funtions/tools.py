import yaml
import os
from .camera import Camera

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "config.yaml")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def login(username, password):
    if username == "admin" and password == "admin":
        return True, True
    if username == "user" and password == "user":
        return True, False
    return False, False


def get_all_keys(dictionary):
    keys = []

    for key, value in dictionary.items():
        keys.append(key)
        if isinstance(value, dict):
            keys.extend(get_all_keys(value))

    return keys


def get_old_data():
    if os.path.exists(DATA_FILE):
        configs = yaml.load(open(DATA_FILE, "r"), Loader=yaml.FullLoader)
        is_full = len(get_all_keys(configs)) == 34
        return configs, is_full
    else:
        return {}, False


def save_config(config):
    print(config)
    with open(DATA_FILE, "w") as f:
        yaml.dump(config, f)


def check_connect_camera():
    try:
        camera = Camera()
        return camera.check_connect()
    except:
        return False
    


def check_connect_plc(port, baudrate, timeout):
    try:
        print(str(port.lower()), int(baudrate), float(timeout))
        return PLC(str(port.lower()), int(baudrate), float(timeout))
    except:
        return None
