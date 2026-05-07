#!/usr/bin/env python3

import sys
import json
import math
from swuapi import request_card_page

expansion = sys.argv[1]

expression = "&filters[$and][0][$or][0][type][name]=Leader&filters[$and][0][$or][0][type][name]=Base&filters[$and][0][variantTypes][name]=Standard&filters[$and][0][expansion][code]="+str(expansion)

page_size = 250

data = request_card_page(0,1,expression)
pages = math.ceil(data['meta']['pagination']['total']/page_size)




####
# curl 'https://admin.starwarsunlimited.com/api/cards?pagination\[pageSize\]=250&pagination\[page\]=5&filters\[expansion\]\[code\]=LOF' > LOF-p5.json

for p in range(pages):
    data = request_card_page(p+1,page_size,expression)
#    print(json.dumps(data))
    for card in data['data']:
        print(card['attributes']['expansion']['data']['attributes']['code']
            +",EN,Base,"+card['attributes']['variantTypes']['data'][0]['attributes']['name']
            +","
            +str(card['attributes']['cardNumber'])
            +","+card['attributes']['rarity']['data']['attributes']['character']
            +",\""+card['attributes']['title']
            +"\",\""
            +(card['attributes']['subtitle'] or "")
            +"\","
            +card['attributes']['type']['data']['attributes']['name']
            #### str(data['data'][1]['attributes']['reprintOf']['data']['attributes']['cardNumber']) if data['data'][1]['attributes']['reprintOf']['data'] else ''
            )