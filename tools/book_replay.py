import numpy as np
import pandas as pd
import sys

import matplotlib.pyplot as plt
# plt.ion()

sys.path.append('../tcaf/tcaf')
import loader
import utils

loader.set_path('../../captured_md')
print loader.get_path()

start_datetime = '20180105T190500'
end_datetime = '20180105T210000'
product_id = 'btcusd'
exchange = 'gdax'

qo = loader.Query(start_datetime, end_datetime, [exchange], [product_id])
book_df = qo.query('OrderBook')

BIDS_PRICE = 'bids_price'
BIDS_QTY = 'bids_qty'
ASKS_PRICE = 'asks_price'
ASKS_QTY = 'asks_qty'


def draw_orderbook(book_df, i):
    row = book_df.iloc[[i]].to_dict('list')
    headers = row.keys()
    def get_price_qty_pairs(price_prefix, qty_prefix):
        result = []
        price_keys = filter(lambda x: x.startswith(price_prefix), headers)
        for pk in price_keys:
            i = pk.split(price_prefix)[1]
            qk = qty_prefix + i
            price, qty = float(row[pk][0]), float(row[qk][0])
            result.append((price, qty))
        return result
    bid_pairs = get_price_qty_pairs(BIDS_PRICE, BIDS_QTY)
    ask_pairs = get_price_qty_pairs(ASKS_PRICE, ASKS_QTY)
    bid_pairs.sort(key=lambda p: -p[0])  # price, descending
    ask_pairs.sort(key=lambda p: -p[0])  # price, descending
    num_bids, num_asks = len(bid_pairs), len(ask_pairs)
    y_pos = np.arange((num_bids + num_asks) * 0.2, 0, -0.2)
    qtys = [t[1] for t in ask_pairs] + [t[1] for t in bid_pairs]
    prices = ['s_%.2f' % t[0] for t in ask_pairs] + ['b_%.2f' % t[0] for t in bid_pairs]
    
    fig, ax = plt.subplots()
    fig.set_figwidth(8)
    barlist = plt.barh(y_pos, qtys, align='center', alpha=0.5, height=0.1)
    
    for i in xrange(num_asks):
        barlist[i].set_color('red')
    for i in xrange(num_asks, num_asks + num_bids):
        barlist[i].set_color('green')
    plt.yticks(y_pos, prices)
    plt.xlabel('Qty')
    plt.xlim(0, 10)
    
    def autolabel(rects):
        """
        Attach a text label above each bar displaying its height
        """
        for q, y, rect in zip(qtys, y_pos, rects):
            w = rect.get_height()
            ax.text(5.0, y, q,
                    ha='center', va='bottom')
    # autolabel(barlist)
    plt.show(block=False)
    return bid_pairs, ask_pairs

i = 150
draw_orderbook(book_df, i)

while True:
  ch = raw_input('i={}, (q)uit, any key to continue: '.format(i)).lower()
  if ch == 'q':
    break
  i += 1
  plt.close()
  draw_orderbook(book_df, i)
plt.close()