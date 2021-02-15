# Wireless LAN and IoT project

A project to capture wireless packets and analyze the packet types

### How to capture packets

The currently added script captures the packet based on
the defined monitor mode interface. The channel on which
capturing takes place is changed every 100ms (configurable).

The script assumes a lot of things about the current netdev state.
There must be a monitor mode interface and a managed interface
active. Any Network Manager must be turned off as that can cause
the managed interface to associate and thus prevent channel
hopping.

Running instructions (sudo):
    1. iwconfig (to check if mon intf is present)
    2. iw phy0 interface add phy0.mon type monitor (if not, add intf)
    3. python3 capture.py (run from ./scripts/ dir only)

