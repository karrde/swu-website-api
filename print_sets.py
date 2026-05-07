#!/usr/bin/env python3

import sys
import json
import math
from swuapi import request_card_page
import logging, sys

logger = logging.getLogger(__name__)    
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

page_size = 250

data = request_card_page(0,1)
pages = math.ceil(data['meta']['pagination']['total']/page_size)


cardsets = {}

####
# curl 'https://admin.starwarsunlimited.com/api/cards?pagination\[pageSize\]=250&pagination\[page\]=5&filters\[expansion\]\[code\]=LOF' > LOF-p5.json

for p in range(pages):
    data = request_card_page(p+1,page_size)
#    print(json.dumps(data))
    for card in data['data']:
        cardsets[card['attributes']['expansion']['data']['attributes']['code']] = card['attributes']['expansion']['data']['attributes']['name']
        
for expansion in cardsets:
    print(f"{expansion},{cardsets[expansion]}")