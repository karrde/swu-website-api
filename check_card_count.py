#!/usr/bin/env python3
import swuapi
import json

def main():
    unique = swuapi.request_unique_cards()['meta']['pagination']['total']
    variants = swuapi.request_card_page()['meta']['pagination']['total']
    print(f"Unique Cards: {unique}\nAll Variants: {variants}")
    

if __name__ == "__main__":
    main()
