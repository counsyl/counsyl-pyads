counsyl-pyads
=============

This Python package contains a Python-only implementation of the AMS/ADS (Automation Device Specification) protocol for communicating directly with Beckhoff PLCs.
No router is included or required.
It is a fork of the [pyads library by Christoph Wiedemann](https://github.com/chwiede/pyads), with support for more data types (including arrays).


### Installation

```
git clone git@counsyl.com:counsyl/counsyl_pyads.git
cd counsyl_pyads
# consider making yourself a virtualenv
pip install -r requirements.txt
python setup.py install
```

### PLC setup

Beckhoff PLCs won't accept connections from just anyone. The Twincat System Manager on the PLC contains a list of "routes" that define allowed clients. Perform the following steps to add the host where you plan to use `counsyl_pyads` to the list of routes:

 1. Find your local IP address (`ifconfig | grep inet` should help), e.g. `192.168.4.13`
 * Dream up an Ams ID for your local machine. The Ams ID is a program identifier used by the ADS protocol. It's often `IP address + .1.1` but any six byte sequence works, for example`192.168.192.168.1.1`. See the [Beckoff Documentation](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/html/tcadscommon_remoteconnection.htm&id=) for more information.
 * Connect to the PLC computer and log in
 * Open the System Manager (right click Twincat tray icon, then select System Manager)
 * Navigate to `SYSTEM - Configuration`, `Route Settings`, then open the `Static Routes` tab
 * Click `Add`. In the `Add Route Dialog` window, you need to fill out the bottom half of the form
     * `Route Name (Target)`: Something descriptive to describe this route, consider including your name
     * `AmsNetId`: The Ams ID you dreamed up above
     * `Transport Type`: `TCP/IP`
     * `Address Info`: Your IP address
     * Select `IP Address`
     * `Connection Timeout`: 5
     * `Target Route`: Static
     * `Remote Route`: None


### Usage

The script `bin/twincat_plc_info.py` should get you started with the basics. You can use it to query system information and a list of all varibles on a PLC.

```bash
twincat_plc_info.py 5.21.172.208.1.1:801 10.1.0.99 801 192.168.192.168.1.1:5555
```

This assumes that you have a PLC with Ams ID `5.21.172.208.1.1` available at IP `10.1.0.99` that is set up to accept connections from you (see PLC setup section above). Port `801` is default. `192.168.192.168.1.1:5555` is your arbitrary local Ams ID including a port that isn't used for anything.


### Related Links

 * [AMS/ADS Protocol Overview](http://infosys.beckhoff.com/content/1033/bk9000/html/bt_ethernet%20ads%20potocols.htm?id=2222)
 * [ADS Command Documentation](http://infosys.beckhoff.com/english.php?content=../content/1033/TcAdsAmsSpec/HTML/TcAdsAmsSpec_Intro.htm)
 * [pyads library by Christoph Wiedemann](https://github.com/chwiede/pyads)
