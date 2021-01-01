"""
Created by @TheLastGimbus

This script reports to Home Assistant when you use/don't use your PC - in a high-level meaning
So not bear nmap or ping - *actually* estimating whether you are *actively* using this PC or not

For now, it detects whether you touch your keyboard or mouse, but in future, it could also detect
if you are watching movie or something
"""

import argparse
from time import sleep
from time import time

import pynput
import requests as re

parser = argparse.ArgumentParser(
    description='Script to monitor if you touch your PC and report it to HASS'
)
parser.add_argument(
    '-u', '--url', required=True,
    help='URL to HASS HTTP binary sensor. '
         'Example: http://IP_ADDRESS:8123/api/states/binary_sensor.DEVICE_NAME'
)
parser.add_argument('--keyboard', action='store_true', help='Whether to monitor keyboard')
parser.add_argument('--mouse', action='store_true', help='Whether to monitor mouse')
parser.add_argument(
    '-t', '--time', type=int, default=180,
    help='How many seconds must pass to report PC as not used - defaults to 3 minutes'
)
parser.add_argument('--token', type=str, required=True, help="HASS long-lived access token")
args = parser.parse_args()

last_interaction = 0


def on_interaction(*shit):
    global last_interaction
    last_interaction = time()


if args.mouse:
    mouse_listener = pynput.mouse.Listener(
        on_move=on_interaction,
        on_click=on_interaction,
        on_scroll=on_interaction,
    )
    mouse_listener.start()

if args.keyboard:
    keyboard_listener = pynput.keyboard.Listener(
        on_press=on_interaction,
        on_release=on_interaction,
    )
    keyboard_listener.start()

session = re.session()
session.headers["Authorization"] = f"Bearer {args.token}"
session.headers["Content-Type"] = "application/json"

active = True
last_report = 0
while True:
    last_state = active
    active = time() - last_interaction < args.time
    # If it's different than last state OR last report was 5 minutes ago
    # print(active)
    if last_state != active or time() - last_report > 300:
        if active:
            state = 'on'
        else:
            state = 'off'
        print(f"Reporting {state}")
        try:
            res = session.post(args.url, json={"state": state, "attributes": {}}, timeout=10)
            if not res.ok:
                raise IOError(f"Response is not ok! Code: {res.status_code} Content: {res.content.decode('utf-8')}")
            print(f"Report ok :) Response: {res.content.decode('utf-8')}")
            last_report = time()
        except Exception as e:
            print(f"Can't connect: {e}")
            sleep(5)

    # If not this, the script will use 100% cpu xD
    sleep(0.1)
