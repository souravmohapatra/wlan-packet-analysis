# Count and output the number of each packet in all given pcap files

import argparse
from pathlib import Path
from scapy.all import sniff, RadioTap

types = {0: ['Association Requests', 0],
         1: ['Association Responses', 0],
         2: ['Reassociation Requests', 0],
         3: ['Resssociation Responses', 0],
         4: ['Probe Requests', 0],
         5: ['Probe Responses', 0],
         6: ['Fragmented frame', 0],
         7: ['Unrecognized', 0],
         8: ['Beacons', 0],
         9: ['ATIMs', 0],
         10: ['Disassociations', 0],
         11: ['Authentications', 0],
         12: ['Deauthentications', 0],
         13: ['Actions', 0],
         14: ['Beamforming Action', 0],
         15: ['Aruba Management Packet', 0],
         16: ['Unrecognized', 0],
         17: ['Unrecognized', 0],
         19: ['Unrecognized', 0],
         18: ['Trigger BQRP', 0],
         20: ['Unrecognized', 0],
         21: ['NDP Announcement', 0],
         24: ['Block ACK Requests', 0],
         25: ['Block ACKs', 0],
         26: ['PS-Polls', 0],
         27: ['Ready To Sends', 0],
         28: ['Clear To Sends', 0],
         29: ['ACKs', 0],
         30: ['CF-Ends', 0],
         31: ['CF-Ends/CF-Acks', 0],
         32: ['Data', 0],
         33: ['Data+CF-Ack', 0],
         34: ['Data+CF-Poll', 0],
         35: ['Data+CF-Ack+CF-Poll', 0],
         36: ['Null', 0],
         37: ['CF-Ack', 0],
         38: ['CF-Poll', 0],
         39: ['CF-Ack+CF-Poll', 0],
         40: ['QoS Data', 0],
         41: ['QoS Data+CF-Ack', 0],
         42: ['QoS Data+CF-Poll', 0],
         43: ['QoS Data+CF-Ack+CF-Poll', 0],
         44: ['QoS Null', 0],
         45: ['Unrecognized', 0],
         46: ['QoS CF-Poll', 0],
         47: ['QoS CF-Ack+CF-Poll', 0]}


def count_packets(pkt):
    # print(pkt.type, pkt.subtype)
    types[int(format(pkt.type, '02b') + format(pkt.subtype, '04b'), 2)][1]+= 1


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='*')
    args = p.parse_args()

    for i, arg in enumerate(args.files):
        path = Path(arg)

        if path.suffix != ".pcap" or not path.exists():
            print(F"Skipping {arg}")
            continue

        sniff(offline=str(path), prn=count_packets, store=0)

        print(i, len(args.files))

    print(types)