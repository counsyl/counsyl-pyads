#!/usr/bin/env python

import argparse
import logging
import pprint

from counsyl_pyads.adsconnection import AdsConnection
from counsyl_pyads.adsclient import AdsClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target_ams', help='The Ams ID of the PLC.')
    parser.add_argument(
        'target_host', help='The IP address or hostname of the PLC.')
    parser.add_argument(
        'target_port', type=int, default=801,
        help='The port of the Twincat system on the PLC.')
    parser.add_argument(
        'source_ams',
        help='The (arbitrary) Ams ID of the relay server.')
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(process)d:%(threadName)s]"
        "[%(filename)s/%(funcName)s][%(levelname)s] %(message)s")

    ads_conn = AdsConnection(
        target_ams=args.target_ams,
        target_ip=args.target_host,
        target_port=args.target_port,
        source_ams=args.source_ams,
    )

    print("Target AMS: %s" % args.target_ams)
    print("Target host: %s:%s" % (args.target_host, args.target_port))

    with AdsClient(ads_conn) as device:
        print ""
        print "DEVICE INFO"
        print ""
        pprint.pprint(device.read_device_info().__dict__)
        print ""
        print "SYMBOLS"
        print ""
        for sym in device.get_symbols():
            pprint.pprint(sym.__dict__)


if __name__ == '__main__':
    main()
