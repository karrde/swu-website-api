#!/usr/bin/env python3

import json
import urllib.request
import urllib.parse
from datetime import datetime
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
import csv
        
swu_epoch = '2023-05-07T01:01:01.000Z'

def fixdate(datestring):
    return datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S.%f%z")

def request_card_page(pageno = 0, pagesize = 25, additional_queries = ''):
    ## Filter variants filters[variantOf][id][$null]=true
    ## page size pagination[pageSize]=250
    ## page number pagination[page]=2
    primary_uri = 'https://admin.starwarsunlimited.com/api/cards'
    
    request_uri = primary_uri + '?pagination[pageSize]='+str(pagesize)
    
    req_page = pageno or 1
    request_uri = request_uri+'&pagination[page]='+str(req_page)+additional_queries
    logging.debug(f"Requesting: {request_uri}")
    f = urllib.request.urlopen(request_uri)
    return json.loads(f.read())
    
def request_unique_cards():
    return request_card_page(additional_queries = '&filters[variantOf][id][$null]=true')

def filter_table_by(table, attribute, value):
    return {k: v for k,v in table.items() if v[attribute]==value}

def sort_table_by(table, attribute):
    return sorted(table.items(), key=lambda x: x[1][attribute])

 
class CardTable:
    def __init__(self, filename = 'card_table.json'):
        self.table = {}
        self.filename = filename
        
    def load(self):
        try: 
            file = open(self.filename,'r')
        except FileNotFoundError:
            self.table = {}
        else:
            self.table = json.loads(file.read())
            file.close()
        
    def save(self):
        try:
            file = open(self.filename,'w')
        except:
            raise
        else:
            file.write(json.dumps(self.table))
            file.close()
        
    def update(self):
        page = 1
        update_from = self.latest_update()
    
        while True:
            ct = request_card_page(page, additional_queries = '&filters[updatedAt][$gt]='+update_from)
            for card in ct['data']:
                logging.debug(f"Card ID {card['id']}")
                if card['id'] in self.table.keys():
                    logging.debug(f"Exists")
                    if fixdate(card['attributes']['updatedAt']) <= fixdate(self.table[card['id']]['updatedAt']):
                        logging.debug(f"Not updated")
                        continue
                self.table[str(card['id'])] = card['attributes']
                logging.debug(f"Updated")
            if ct['meta']['pagination']['page'] > ct['meta']['pagination']['pageCount']:
                break
            page = page + 1
            logging.debug(f"Moving to page {page}")

    def latest_update(self):
        last_update = swu_epoch
        
        for id in self.table:
            last_update = max(last_update,self.table[id]['updatedAt'])
        return(last_update)
        
    def sets(self):
        sets = {}
        for id in list(self.table):
            logging.debug(f"checking id {id}")
            expansion = self.table[id]['expansion']['data']
            if expansion:
                sets[expansion['id']] = expansion['attributes']
        return sets

    def traits(self):
        traits = {}
        for id in list(self.table):
            logging.debug(f"checking id {id}")
            for trait in self.table[id]['traits']['data']:
                traits[trait['id']] = trait['attributes']
        return traits
        
    def filter_by(self, attribute, value):
        return {k: v for k,v in self.table.items() if v[attribute]==value}
        
    def spreadsheet(self):
        ssrows = []
        fields = ['SetNo','Rarity','Name','Title','Type','Arena','Aspect A','Aspect B','Cost','Power','Defense','Traits','Keyword A','Keyword B','Text','Leader Ability']
        for k,v in sort_table_by(filter_table_by(self.filter_by('expansion', {'data': {'id': 2, 'attributes': self.sets()[2]}}), 'variantOf', {'data': None}),'cardNumber'):
            ssrows.append(
                {
                    'SetNo': v['cardNumber'],
                    'Rarity': v['rarity']['data']['attributes']['character'],
                    'Name': v['title'],
                    'Title': v['subtitle'] or '',
                    'Type': v['type']['data']['attributes']['name'],
                    'Arena': v['arenas']['data'][0]['attributes']['name'] if len(v['arenas']['data']) else '',
                    'Aspect A': v['aspects']['data'][0]['attributes']['name'] if len(v['aspects']['data']) else '-',
                    'Aspect B': v['aspectDuplicates']['data'][0]['attributes']['name'] if len(v['aspectDuplicates']['data']) 
                        else (v['aspects']['data'][0]['attributes']['name'] if len(v['aspects']['data'])>1 else '-' ),
                    'Cost': v['cost'] or "-",
                    'Power': v['power'] or "-",
                    'Defense': v['hp'] or "-",
                    'Traits': ', '.join([trait['attributes']['name'] for trait in v['traits']['data']]),
                    'Keyword A': v['keywords']['data'][0]['attributes']['name'] if len(v['keywords']['data']) else '',
                    'Keyword B': v['keywords']['data'][1]['attributes']['name'] if len(v['keywords']['data']) > 1 else '',
                    'Text': v['text'].replace("\n", "\\n") if v['text'] else '',
                    'Leader Ability': v['deployBox'].replace("\n", "\\n") if v['deployBox'] else ''
                }
            )
        
        # creating a csv dict writer object
        writer = csv.DictWriter(sys.stdout, fieldnames=fields)

        # writing headers (field names)
        writer.writeheader()

        # writing data rows
        writer.writerows(ssrows)
        
def main():
    pass

if __name__ == "__main__":
    main()