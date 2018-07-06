#!/usr/bin/env python3

import re

if __name__ == "__main__":
    path = '/data/ergo'
    log_file = path + '/ergo.log'
    config_file = path + '/application.conf'

    with open(config_file, 'r') as c:
        config = c.read()
        match = re.search('nodeName = "(.+)"', config)
        if match:
            node_name = match.group(1)
            with open(log_file, 'r') as l:
                for logstring in l:
                    if 'New block found:' in logstring:
                        match = re.search('"id":"(.+?)"', logstring)
                        if match:
                            block_id = match.group(1)
                            print(node_name, '|', block_id)
                            break
