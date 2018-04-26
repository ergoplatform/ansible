#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

CERTBOT_ETC_PATH = os.environ.get('CERTBOT_ETC_PATH', '/etc/letsencrypt')
THREASHOLD = 60 * 60 * 24 * 65  # number of seconds in 65 days

if __name__ == "__main__":
    t = time.time()
    for entry in os.scandir(CERTBOT_ETC_PATH + '/live'):
        if not entry.name.startswith('.') and entry.is_dir():
            mtime = entry.stat().st_mtime
            age = t - mtime
            print(entry.name, mtime, round(age), age > THREASHOLD)
