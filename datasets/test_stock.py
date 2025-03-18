from get_stock_data import get_analyst_target_price

from time import sleep
import json
from sp500 import sp_500
from regex import F

#write price data into file price.jsonl
with open('price.jsonl', 'w', encoding='utf-8') as f:
    for tiker in sp_500:
        price = get_analyst_target_price(tiker)
        f.write(json.dumps(price, ensure_ascii=False)+'\n')
        sleep(5)