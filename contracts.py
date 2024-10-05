import requests
import re
import heapq
from collections import defaultdict
from dataclasses import dataclass
import starlette
import starlette.status
import csv
from generate_url import generate_url
from dotenv import load_dotenv
import os

load_dotenv()

{
    "collection" : 
    {
        "ext" : 
        {
            "sign" : ["min", "max", "name"]
        }
    }
}

params = {
        'query': '',
        'appid': '730',  
        'norender': 1,
        'count': 100,
        'start': 0
}
MIN_PRICE_IN_CENTS = int(os.getenv('MIN_PRICE_IN_CENTS', 100))
MIN_NUMBER_OF_ITEMS = int(os.getenv('NUMBER_OF_ITEMS', 10))
url = "https://steamcommunity.com/market/search/render"
exterior_pattern = r"Exterior:\s*(.+)"
def default_price():
    return [float("inf"), float("-inf"), ""]
prices = defaultdict(lambda: defaultdict(lambda: defaultdict(default_price)))
significances = {
    "Consumer Grade": 0,
    "Industrial Grade": 1,
    "Mil-Spec Grade": 2,
    "Restricted": 3,
    "Classified": 4,
    "Covert": 5
}

for i in range(13):
    params["start"] = i * 100
    result = requests.post(url=url, params=params)
    if result.status_code != starlette.status.HTTP_200_OK:
        print("invalid response")
        continue
    s = result.json()
    for item in s["results"]:            
        if "asset_description" not in item:
            continue
        item_name = item["name"]
        if "Souvenir" in item_name or "StatTrak" in item_name:
            continue
        item_price = item["sell_price"]
        exterior = None
        significance = None
        collection = None
    
        descs = item["asset_description"]["descriptions"]
        for desc in descs:
            val = desc["value"]
            if "Exterior" in val:
                ext = re.search(exterior_pattern, val)
                exterior = ext.group(1)
            if "Collection" in val:
                collection = val
        item_type = item["asset_description"]["type"]
        for sign, sign_val in significances.items():
            if sign in item_type:
                significance = sign_val
                break
        
        if exterior and significance and collection:
            cur_min, cur_max, _ = prices[collection][exterior][significance]
            prices[collection][exterior][significance] = [min(cur_min, item_price), max(cur_max, item_price), item_name]

# поиск джекпот элемента
k = 1

@dataclass
class Item:
    collection : str = None
    sign : str = None
    ext : str = None
    target_name : str = None
    price : int = 0

result = [] 
heapq.heapify(result)
c = e = s = None
for collection in prices:
    for ext in prices[collection]:
        for sign in prices[collection][ext]:
            cur_item = prices[collection][ext][sign]
            if sign < 5 and sign + 1 in prices[collection][ext]:
                best_received_item = prices[collection][ext][sign + 1]
                best_received_item_price = best_received_item[1]
                best_received_item_name = best_received_item[2]
                cur_item_price = cur_item[0]
                if best_received_item_price < MIN_PRICE_IN_CENTS:
                    continue
                cur_k = best_received_item_price / cur_item_price
                
                ent = (cur_k, Item(collection, sign, ext, best_received_item_name, best_received_item_price))
                if len(result) < 10:
                    heapq.heappush(result, ent)
                else:
                    heapq.heappushpop(result, ent)
                if k < cur_k:
                    c, e, s = collection, ext, sign
                    k = cur_k

with open('dataset.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=' ')
    csvwriter.writerow(['name', 'url', 'ratio', 'price'])
    while result:
        ratio, item = heapq.heappop(result)
        row = [item.target_name, generate_url(item.target_name), ratio, item.price]
        csvwriter.writerow(row)
                
                
    