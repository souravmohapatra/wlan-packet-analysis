# Transform the pcap file into txt files with the desired fields for easier analysis 

import argparse
from pathlib import Path
from scapy.all import sniff, RadioTap

# Fiddle with this method to change what goes into the file
def convert_to_txt(pkt):
    return F"{pkt[RadioTap].Channel}, {pkt.time}, {pkt.type}, {pkt.subtype}\n"

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('files', nargs='*')
    args = p.parse_args()

    for arg in args.files:
        path = Path(arg)

        if path.suffix != ".pcap" or not path.exists():
            print(F"Skipping {arg}")
            continue

        new_path = path.with_suffix('.txt')
        
        with new_path.open('w+') as w:
            sniff(offline=str(path), prn=lambda pkt: w.write(convert_to_txt(pkt)) and None, store=0)

        print(str(new_path) + " has been written")


            


