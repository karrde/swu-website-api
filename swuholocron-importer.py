#!/usr/bin/env python3
import swuapi
import json
import html
import pathlib, os
from datetime import datetime


def card_xmlpage(card):
#    for repltext in ['deployBoxStyled', 'textStyled']:
#        card[repltext].replace('[<img src=\\"https://cdn.starwarsunlimited.com/icon_exhaust_0c450d09d4.png\\" alt=\\"icon_exhaust.png\\">]','{{DisplayExhaust}}')
    xmlstring = f'<page>\n<title>{card["title"]}'
    if card["subtitle"]:
        xmlstring += f', {card["subtitle"]}'
    xmlstring += '</title><ns>0</ns><revision><model>wikitext</model><format>text/x-wiki</format><text xml:space="preserve">{{Card\n|CardUnique='
    if card["unique"]:
        xmlstring += 'Yes'
    else:
        xmlstring += 'No'
    aspects = []
    for aspect in card['aspects']['data']:
        aspects.append(aspect['attributes']['name'])
    for aspect in card['aspectDuplicates']['data']:
        aspects.append(aspect['attributes']['name'])
    xmlstring += f'\n|Aspects={",".join(aspects)}'
    xmlstring += f'\n|Type={card["type"]["data"]["attributes"]["name"]}|Arena='
    arenas = []
    for arena in card['arenas']['data']:
        arenas.append(arena['attributes']['name'])
    if len(arenas):
        xmlstring += ",".join(arenas)
    else:
        xmlstring += 'None'
    xmlstring += '\n|Cost='
    if card['cost']:
        xmlstring += str(card['cost'])
    else:
        xmlstring += 'None'
    xmlstring += '\n|Power='
    if card['power']:
        xmlstring += str(card['power'])
    else:
        xmlstring += 'None'
    xmlstring += '\n|HP='
    if card['hp']:
        xmlstring += str(card['hp'])
    elif card["type"]["data"]["attributes"]["name"] == "Upgrade":
        xmlstring += str(0)
    else:
        xmlstring += 'None'
    traits = []
    xmlstring += '\n|Traits='
    for trait in card['traits']['data']:
        traits.append(trait['attributes']['name'])
    if len(traits):
        xmlstring += ", ".join(traits)
    else:
        xmlstring += 'None'
    xmlstring += '\n|LeaderAction='
    if ("deployBoxStyled" in card) & (card['deployBoxStyled'] != ""):
        xmlstring += html.escape(f"{card['textStyled']}{card['epicActionStyled']}")
    else:
        xmlstring += 'None'
    xmlstring += '\n|Action='
    if ("deployBoxStyled" in card) & (card['deployBoxStyled'] != ""):
        xmlstring += html.escape(f"{card['deployBoxStyled']}")
    else:
        xmlstring += html.escape(f"{card['textStyled']}")
    
    xmlstring += '}}</text></revision></page>'
    return xmlstring

def variant_xmlpage(card):
    xmlstring = f'<page>\n<title>{card["expansion"]["data"]["attributes"]["code"]}-{card["cardNumber"]:03d}</title>'
    xmlstring += '<ns>0</ns><revision><model>wikitext</model><format>text/x-wiki</format><text xml:space="preserve">{{Variant\n|Card='
    xmlstring += f'{card["title"]}'
    if card["subtitle"]:
        xmlstring += f', {card["subtitle"]}'
    xmlstring += f'\n|Artist={card["artist"]}'
    xmlstring += f'\n|Subset=Base'
    xmlstring += f'\n|CardSet={card["expansion"]["data"]["attributes"]["code"]}'
    xmlstring += f'\n|Rarity={card["rarity"]["data"]["attributes"]["name"]}'
    xmlstring += f'\n|SetNum={card["cardNumber"]:03d}'
    xmlstring += '\n|Treatment=Standard'
    xmlstring += f'\n|Images={card["expansion"]["data"]["attributes"]["code"]}-{card["cardNumber"]:03d}.png'
    xmlstring += f'\n|BackImage='
    if card["type"]["data"]["attributes"]["name"] == "Leader":
        xmlstring += f'{card["expansion"]["data"]["attributes"]["code"]}-{card["cardNumber"]:03d}b.png'
    else:
        xmlstring += 'None'
    xmlstring += '\n|SourceName=Fantasy Flight Games'
    xmlstring += f'\n|Source=https://starwarsunlimited.com/cards?cid={card["cardUid"]}'
    xmlstring += f'\n|RevealDate={card["publishedAt"].split("T")[0]}'
    xmlstring +='\n|Lore=Unknown'
    
    xmlstring += '}}</text></revision></page>'
    return xmlstring

def main():
    card_table = swuapi.CardTable()
    card_table.load()
    swuh_epoch = '2024-04-18T08:44:20.196Z'
    output = '''<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.11/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.11/ http://www.mediawiki.org/xml/export-0.11.xsd" version="0.11" xml:lang="en">
  <siteinfo> 
    <sitename>SWU Holocron</sitename>
    <dbname>swuholocron</dbname>
    <base>https://swuholocron.mywikis.wiki/wiki/Main_Page</base>
    <generator>MediaWiki 1.35.13</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter" />
      <namespace key="3006" case="first-letter">Leaks</namespace>
    </namespaces>
  </siteinfo>'''
    for cid,card in card_table.table.items():
        if card['variantOf']['data']:
            continue
        if swuapi.fixdate(card['updatedAt']) > swuapi.fixdate(swuh_epoch):
            output += card_xmlpage(card_table.table[cid])
            output += variant_xmlpage(card_table.table[cid])
    output += '</mediawiki>'
    print(output)

if __name__ == "__main__":
    main()
