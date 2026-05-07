#!/usr/bin/env python3

import sys
import json
import math
from swuapi import request_card_page

expansion = sys.argv[1]

page_size = 250

data = request_card_page(0,1,"&filters[expansion][code]="+str(expansion))
pages = math.ceil(data['meta']['pagination']['total']/page_size)




####
# curl 'https://admin.starwarsunlimited.com/api/cards?pagination\[pageSize\]=250&pagination\[page\]=5&filters\[expansion\]\[code\]=LOF' > LOF-p5.json

for p in range(pages):
    data = request_card_page(p+1,page_size,"&filters[expansion][code]="+str(expansion))
#    print(json.dumps(data))
    for card in data['data']:
        print(card['attributes']['expansion']['data']['attributes']['code']
            +",EN,"+(card['attributes']['variantTypes']['data'][0]['attributes']['name'] if card['attributes']['variantTypes']['data'] else '')
            +","
            +(str(card['attributes']['cardNumber']) if not ('Token' in card['attributes']['type']['data']['attributes']['name']) else f"T{card['attributes']['cardNumber']:02}")
            +","+card['attributes']['rarity']['data']['attributes']['character']
            +",\""+card['attributes']['title']
            +"\",\""
            +(card['attributes']['subtitle'] or "")
            +"\","
            +card['attributes']['type']['data']['attributes']['name']
            +","
            +str(card['attributes']['cost'] or '')
            +",\""
            +", ".join([x['attributes']['name'] for x in card['attributes']['aspects']['data']+card['attributes']['aspectDuplica\
tes']['data']])
            +"\","
            +str((card['attributes']['power'] if card['attributes']['type']['data']['attributes']['name'] != 'Upgrade' else  card['attributes']['upgradePower']) or '')
            +","
            +str((card['attributes']['hp'] if card['attributes']['type']['data']['attributes']['name'] != 'Upgrade' else  card['attributes']['upgradeHp']) or '')
            +",\""
            +", ".join([x['attributes']['name'] for x in card['attributes']['traits']['data']])
            +"\",\""
            +"\\\\n".join(list(filter(None, [card['attributes']['text'],card['attributes']['deployBox'],card['attributes']['epicAct\
ion']])))
            +"\","
            +str(card['id'])
            +","
            +(str(card['attributes']['variantOf']['data']['id']) if card['attributes']['variantOf']['data'] else '')
            +","
            +(str(card['attributes']['reprintOf']['data']['id']) if card['attributes']['reprintOf']['data'] else '')
            )