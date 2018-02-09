#!/usr/bin/env python3

import argparse
import requests
import tabulate
import time
import sys
from pylibs import config
from pylibs import influxdb
from pylibs import utils


def get_info(url):
    timestamp_start = time.time()
    response = requests.get(url)
    timestamp_end = time.time()

    monitor = {
        'fields': {
            'response_time': timestamp_end - timestamp_start,
            'status_code': response.status_code,
        },
        'more': {
            'timestamp_start': timestamp_start,
            'timestamp_end': timestamp_end,
        }
    }

    if response.status_code == 200:
        info = response.json()
        monitor['fields']['difficulty'] = int(info['difficulty'])
        monitor['fields']['peersCount'] = info['peersCount']
        monitor['fields']['unconfirmedCount'] = info['unconfirmedCount']
        monitor['fields']['fullHeight'] = info['fullHeight']
        monitor['fields']['headersHeight'] = info['headersHeight']
        monitor['more']['name'] = info['name']

    return monitor


def sync(monitor):
    name = monitor['more']['name']
    timestamp = monitor['more']['timestamp_start']
    json_body = [{
        "time": round(timestamp * 1000000000),
        "measurement": "node_info",
        "tags": {'name': name, 'net': 'testnet'},
        "fields": monitor['fields']
    }]
    client = influxdb.connect(config['influxdb'])
    client.write_points(json_body)
    utils.message('Ergo node {} info metrics was saved to InfluxDB at timestamp {}.'.format(name, timestamp))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get Ergo node info')
    parser.add_argument('action', nargs=1, metavar="show|show-influx|sync|sync-daemon",
                        help='Choose your action: show or sync Ergo node info')
    args = parser.parse_args()

    if args.action[0] == 'show':
        print(get_info(config['DEFAULT']['node_url'] + '/info'))

    elif args.action[0] == 'show-influx':
        cl = influxdb.connect(config['influxdb'])
        res = cl.query("SELECT * FROM node_info WHERE time > now() - 1d")
        print(tabulate.tabulate(res.get_points(), headers="keys"))

    elif args.action[0] == 'sync':
        monitor = get_info(config['DEFAULT']['node_url'] + '/info')
        sync(monitor)

    elif args.action[0] == 'sync-daemon':
        utils.message('Syncing Ergo node info daemon started.')
        while True:
            monitor = get_info(config['DEFAULT']['node_url'] + '/info')
            if monitor['fields']['status_code'] != 200:
                print('Error {} occurred when processing node info, apply cooldown pause for {} seconds'.format(
                    monitor['fields']['status_code'], config['DEFAULT']['cooldown_pause']))
                time.sleep(int(config['DEFAULT']['cooldown_pause']))
            else:
                sync(monitor)
                time.sleep(int(config['DEFAULT']['pause']))
            sys.stdout.flush()
