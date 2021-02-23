#
# Questions to ask?
#  - Can we manually simulate events?
#  - Any idea how to capture 11ax related packets?
#  - Suggested channel dwell time?
#  - Have (and how) to decrypt?
#  - Data frames are not captured?
#

#
# @brief: Script to capture packets
# @dependencies: Script needs to run with sudo
#                Assumes the monitor mode interface is up
#                Assumes NetworkManager won't interfere with interfaces
# @output: PCAP file with packet captures
#
# @desciption: This script runs the tshark on one thread while it does
#              channel hopping on another thread. The channel hopping can
#              independently and the generated pcap file consists of packets
#              from all the channels
#

from subprocess import Popen, PIPE
from threading import Thread
from time import time, sleep
from random import seed, random
import datetime

# True if ran on Tolga's laptop
TOLGA = False

# Interfaces
MON_INTF = "phy0.mon"
if TOLGA:
    MANAGED_INTF = "wlp2s0" 
else: 
    MANAGED_INTF = "wlp62s0"

# Output file
FILE_NAME = "packets_"
FILE_NAME_TEXT = "packets_cumulative"
FILE_SIZE = 512 # in mb

# Functionality specific definitions
DWELL_TIME = 10 # Max dwell time in seconds. Hopping will happen in max(rand(), DWELL_TIME)
stop_capture = False

# list of 802.11 channels to hop. Has all valid 2.4Ghz, 5Ghz, 6Ghz channels. 
# 2.4Ghz: 1 - 13
# 5Ghz: 36 - 64
#       100 - 144
#
# Todo: Figure out how to sniff on 11ax 6Ghz channels?
channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

if not TOLGA:
    channels += [36, 40, 44, 48, 52, 56, 60, 64,
                100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165]

# Simple function to execute a shell command
def run_cmd(cmd, disp=False):
    ''' Returns output and error code '''
    process = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    
    stdout, stderr = process.communicate()
    rc = process.returncode
    
    if (rc != 0):
        print("Error: " + stderr.decode("utf-8"))
        raise Exception("Failed at command: " + cmd)
    
    if (disp):
        print(stdout.decode("utf-8"))
    return stdout.decode("utf-8"), stderr.decode("utf-8"), rc

# Setup the monitor interface. Change the global names
def setup_interface():
    ''' Setups the interface '''
    run_cmd("echo Setting up interface", disp=True)

    # Unblock wifi if already blocked. NetworkManager needs to be turned off
    # as it forces the wifi to be connected which prevents channel hopping
    run_cmd("sudo rfkill unblock wifi")
    run_cmd("sudo ifconfig " + MON_INTF + " up")
    run_cmd("sudo ifconfig " + MANAGED_INTF + " down")

# Thread to run tshark on the monitor interface
def run_tshark():
    f_pcap = "../captures/" + FILE_NAME + datetime.datetime.now().strftime("%H-%M_%m-%d-%Y") + ".pcap"
    f_txt = "../captures/" + FILE_NAME_TEXT + ".txt"
    run_cmd("touch " + f_pcap)
    run_cmd("touch " + f_txt)
    
    # Give read/write permissions to "others" as tshark executes from that group
    run_cmd("sudo chmod o=rw " + f_pcap)
    run_cmd("sudo chmod o=rw " + f_txt)
    run_cmd("sudo tshark -i " + MON_INTF + " -a filesize:" + str(FILE_SIZE * 1024) + " -T fields -e frame.time -e wlan_radio.channel -e wlan.fc.type -e wlan.fc.type_subtype -w " + f_pcap + " >> " + f_txt)

# Thread to do channel hopping
def hop_channel():
    seed(3.14)
    while (True):
        for ch in channels:
            run_cmd("sudo iwconfig " + MON_INTF + " channel " + str(ch))
            dw_time = max(int(random() * 100) / 10 + 1, DWELL_TIME)
            sleep(dw_time)

if __name__ == '__main__':
    setup_interface()

    t1 = Thread(target = run_tshark)
    t2 = Thread(target = hop_channel)

    t1.start()
    t2.start()

    print("Capturing packets, Press CTRL+C to stop capture")
    start_time = time()

    t1.join()

    print("Capture complete. Time taken: " + str(time() - start_time).split(".")[0] + "s.")
    exit(0)
