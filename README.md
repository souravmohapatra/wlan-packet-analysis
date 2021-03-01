# Wireless LAN and IoT project

A project to capture wireless packets and analyze the packet types

### How to capture packets

The currently added script captures the packet based on
the defined monitor mode interface. The channel on which
capturing takes place is changed randomly with a max time of
10 seconds (configurable).

The script assumes a lot of things about the current netdev state.
There must be a monitor mode interface and a managed interface
active. Any Network Manager must be turned off as that can cause
the managed interface to associate and thus prevent channel
hopping.

Running instructions (sudo):
- iwconfig (to check if mon intf is present)
- iw phy0 interface add phy0.mon type monitor (if not, add intf)
- python3 capture.py (run from ./scripts/ dir only)

### How to transform the pcap to txt

Use the script ./scripts/transform.py to extract usefull data from
the pcap files to a text file. The data to be extracted can be
configured in the script

### How to plot the graphs

All the graphs have been plotted using Wireshark's built in IO graphing
tool.
