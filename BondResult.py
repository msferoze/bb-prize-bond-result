# -*- coding: utf-8 -*-
import urllib
import ssl
import re
import pandas as pd
from datetime import datetime

ssl._create_default_https_context = ssl._create_unverified_context
df = pd.read_csv(r"prize_bond.csv", dtype=object)


def MatchBond(bond_number):
    url = r"https://www.bb.org.bd/investfacility/prizebond/searchPbond.php?txtNumbers="+bond_number
    response = str(urllib.request.urlopen(url).read())
    did_win = 0
    draw_no = -1
    prize_won = r"None"
    amount_won = 0
    if re.search(r'Congratulation!', response):
        did_win = 1
        draw_no = re.search(r'(?<='+bond_number+r'<\/td><td>)\d+(?=\<\/td)', response)[0]
        prize_won = re.search(r'(?<='+bond_number+r'<\/td><td>'+draw_no+r'<\/td><td>)\w+\s\w+', response)[0]
        amount_won = re.search(r'(?<='+prize_won+r'<\/td><td>)\d+', response)[0]
    return did_win, draw_no, prize_won, amount_won

df['Won?'], df['DrawNo'], df['Place'], df['Amount'] = zip(*df['BondNo'].map(MatchBond))
df['RowInsertDateTime'] = datetime.now()
df = df.sort_values(['Won?'], ascending=[False])
df.to_csv('results.csv', index=False)
    




