import subprocess
import json
import time
import pygetwindow as gw
from yaspin import yaspin


def get_status_fun():
    cmd = 'aws lightsail get-instance-state --instance-name papa_machine --output json'
    push = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    response = json.loads(push.communicate()[0])
    return response['state']['name']


def is_stopped():
    return get_status_fun() == "stopped"


def is_stopping():
    return get_status_fun() == "stopping"


def is_running():
    return get_status_fun() == "running"


with yaspin(text="Time Elapsed: ", color="cyan", timer=True) as sp:
    if is_running() and not is_stopped():
        sp.write('> Checking if instance is stopping...')
        time.sleep(10)

    if(is_stopping()):
        sp.write("> Waiting for instance to stop gracefully.")
        while not is_stopped():
            time.sleep(5)
        sp.write("> Instance stopped successfully.")

    if(is_stopped()):
        cmd = 'aws lightsail start-instance --instance-name papa_machine'
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
        sp.write("> Start instance process initiated, please wait for it to run...")

    while not is_running():
        time.sleep(5)
    sp.write("> Instance is running successfully.")
    sp.write("> Initiating rdp session...")

    cmd = 'mstsc.exe vm_connection.rdp'
    subprocess.Popen(cmd)

    while len(gw.getWindowsWithTitle('Remote Desktop Connection')) == 0:
        time.sleep(1)
    win = gw.getWindowsWithTitle('Remote Desktop Connection')[0]
    win.activate()
    sp.write("> Remote Desktop initiated.")
