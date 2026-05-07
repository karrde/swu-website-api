#!/usr/bin/env python3
import swuapi
import json
import pathlib, os
from datetime import datetime
import urllib.request
import urllib.parse
from pytz import timezone

def check_and_download(filename, art):
    if not os.path.exists(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    if os.path.exists(filename):
        cur_time = datetime.fromtimestamp(int(os.path.getmtime(filename)), tz=timezone('UTC'))
        Download = swuapi.fixdate(art['data']['attributes']['updatedAt']) > cur_time
    else:
        Download = True
    if Download:
        request_uri = art['data']['attributes']['formats']['card']['url']
        f = urllib.request.urlopen(request_uri)
        with open(filename, "wb") as image_file:
            image_file.write(f.read())

def get_location(base, card, back = False):
    file_loc = base
    if card['expansion']['data']:
        file_prefix = card['expansion']['data']['attributes']['code'] + "-"
        if len(card['variantTypes']['data']) == 0:
            file_loc = file_loc / card['expansion']['data']['attributes']['code']
        else:
            file_loc = file_loc / (card['expansion']['data']['attributes']['code'] + " - " + card['variantTypes']['data'][0]['attributes']['name'])
    else:
        file_prefix = "SWU-"
    if back:
        file_loc = file_loc / (file_prefix + "{:03d}".format(int(card['cardNumber'])) +"b.png")
    else:
        file_loc = file_loc / (file_prefix + "{:03d}".format(int(card['cardNumber'])) +".png")
    return file_loc

def main():
    card_table = swuapi.CardTable()
    card_table.load()
    base_location = pathlib.Path('images/')
    if not os.path.exists(base_location):
        of.mkdir(base_location)
    for id_num,card in card_table.table.items():
        download = False
        print(f"Checking card ID {id_num}")
           
        check_and_download(get_location(base_location, card), card['artFront'])
        if card['artBack']['data']:
            check_and_download(get_location(base_location, card, True), card['artBack'])
            
if __name__ == "__main__":
    main()
