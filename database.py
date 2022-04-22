import requests
import json
import random
import sqlite3

def _connect():
    conn = sqlite3.connect('cards.db')
    return conn

def get_bulk_data():
    url = "https://api.scryfall.com/bulk-data"
    r = requests.get(url)
    data = json.loads(r.text)

    for x in data["data"]:
        if x["name"] == "Oracle Cards":
            r = requests.get(x["download_uri"])
            ret = json.loads(r.text)
            return ret

def update_db():
    conn = _connect()

    fails = 0
    for x in get_bulk_data():
        excluded_cards = ["island", "plains", "forest", "swamp", "mountain"]
        if (x["legalities"]["vintage"] == "legal" or x["border_color"] == "silver") and (not "token" in x["layout"] and (not (x["name"].lower() in excluded_cards))):
            try:
                sql = ("INSERT OR REPLACE INTO Cards ("
                    "name,"
                    "isLegalStandard,"
                    "isLegalModern,"
                    "isLegalPenny,"
                    "isLegalLegacy,"
                    "expansion,"
                    "rarity,"
                    "priceUsd,"
                    "priceEur,"
                    "priceTix"
                    ")"
                    " VALUES ("
                    '\"{name}\",'
                    '{isLegalStandard},'
                    '{isLegalModern},'
                    '{isLegalPenny},'
                    '{isLegalLegacy},'
                    '\"{expansion}\",'
                    '\"{rarity}\",'
                    '{priceUsd},'
                    '{priceEur},'
                    '{priceTix})'
                ).format(
                    name = x["name"].replace("\"", "\"\""),
                    isLegalStandard = x["legalities"]["standard"] == "legal",
                    isLegalModern = x["legalities"]["modern"] == "legal",
                    isLegalPenny = x["legalities"]["penny"] == "legal",
                    isLegalLegacy = x["legalities"]["legacy"] == "legal",
                    expansion = x["set"],
                    rarity = x["rarity"],
                    priceUsd = x["prices"]["usd"] or -1,
                    priceEur = x["prices"]["eur"] or -1,
                    priceTix = x["prices"]["tix"] or -1,
                )
                conn.execute(sql)
            except:
                print(x["name"] + " failed")
                fails+=1
    conn.commit()
    print(fails)

def get_list(query = None):
    conn = _connect()
    ret = ""
    if query is None:
        sql = "SELECT name FROM Cards ORDER BY RANDOM() LIMIT 1"
    else:
        sql = "SELECT name FROM Cards WHERE (" + query + ") ORDER BY RANDOM() LIMIT 1"
    for i in range (100):
        cursor = conn.execute(sql)
        for row in cursor:
            ret += str(row[0]) + "\n"
    return ret

