import heapq
from contracts.parse_data import parse_data
from schemas import Item
from utils.adjusted_params import MIN_PRICE_IN_CENTS, MIN_NUMBER_OF_ITEMS


async def find_best_contracts(prices: dict) -> list[Item]:
    result = [] 
    heapq.heapify(result)
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
                    
                    ent = (cur_k, 
                           Item(
                                collection=collection, 
                                sign=sign, 
                                ext=ext, 
                                target_name=best_received_item_name, 
                                price=best_received_item_price,
                                ratio=cur_k
                        )
                    )
                    if len(result) < MIN_NUMBER_OF_ITEMS:
                        heapq.heappush(result, ent)
                    else:
                        heapq.heappushpop(result, ent)
    array_items = []
    while result:
        _, item = heapq.heappop(result)
        array_items.append(item)
    return array_items