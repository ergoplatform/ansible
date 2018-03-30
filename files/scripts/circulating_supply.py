#!/usr/bin/env python3

import json
import urllib.request

URL = "https://marketdata.wavesplatform.com/api/ticker/725Yv9oceWsB4GsYwyy4A52kEwyVrL5avubkeChSnL46/BTC"
FILE = 'circulating_supply.html'

req = urllib.request.Request(URL, data=None, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
})

with urllib.request.urlopen(req) as url:
    data = json.loads(url.read().decode())

    if 'amountAssetCirculatingSupply' in data:
        with open(FILE, 'w') as f:
            f.write(data['amountAssetCirculatingSupply'])
