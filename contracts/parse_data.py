from collections import defaultdict
from utils.enums import significances_grade
import re
import starlette
import starlette.status
{
    "collection" : 
    {
        "ext" : 
        {
            "sign" : ["min", "max", "name"]
        }
    }
}

def default_price():
    return [float("inf"), float("-inf"), ""]

async def parse_data(data: list) -> tuple[bool, list]:
    prices = defaultdict(lambda: defaultdict(lambda: defaultdict(default_price)))
    exterior_pattern = r"Exterior:\s*(.+)"

    for result in data:
        if result.status != starlette.status.HTTP_200_OK:
            print(f"invalid response\nstatus code: {result.status}")
            continue
        s = result.json
        
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
            for sign, sign_val in significances_grade.items():
                if sign in item_type:
                    significance = sign_val
                    break
            
            if exterior and significance and collection:
                cur_min, cur_max, cur_max_name = prices[collection][exterior][significance]
                if item_price > cur_max:
                    cur_max_name = item_name
                prices[collection][exterior][significance] = [min(cur_min, item_price), max(cur_max, item_price), cur_max_name]
    
    return prices





