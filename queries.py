import re

def create_query(query):
    query_list = query.split()
    current_query = ''
    q = ''
    for x in query_list:
        if x.startswith("format") or x.startswith("f"):
            q = _format_format(x)
        if x.startswith("usd"):
            q = _format_priceUsd(x)
        if x.startswith("eur"):
            q = _format_priceEur(x)
        if x.startswith("tix"):
            q = _format_priceTix(x)
        current_query += q + " AND "
    if current_query == '':
        return None
    return current_query[:-5]

def _format_format(query):
    
    x = list(filter(None, re.split(r"(plus|[=<>])", query)))
    x[0] = "format"
    return ''.join(x)

def _format_priceUsd(query):
    return query.replace("usd", "priceUsd", 1) + " AND priceUsd>0"

def _format_priceEur(query):
    return query.replace("eur", "priceEur", 1) + " AND priceEur>0"

def _format_priceTix(query):
    return query.replace("tix", "priceTix", 1) + " AND priceTix>0"
