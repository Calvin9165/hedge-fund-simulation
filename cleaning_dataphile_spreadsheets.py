import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from cleaning_data_functions import *


# loading in data from dataphile csvs
dyn_alpha = clean_om_funds_from_dataphile(df=pd.read_csv('Dynamic Alpha Historical Returns.csv')).pct_change()
ehp_adv = clean_om_funds_from_dataphile(df=pd.read_csv('EHP Advantage Historical Returns.csv')).pct_change()
hgc = clean_om_funds_from_dataphile(df=pd.read_csv('HGC Historical Returns.csv')).pct_change()
timelo = clean_om_funds_from_dataphile(df=pd.read_csv('Timelo Historical Returns.csv')).pct_change()

# loading in hfri data from csv (not from dataphile)
hfri_ls_index = pd.read_csv('HFRI Long-Short Index Returns.csv')
hfri_ls_index['Date'] = pd.to_datetime(hfri_ls_index['Date'], dayfirst=True)
hfri_ls_index.set_index(keys='Date', inplace=True)
hfri_ls_index.rename({' Monthly Index Value': 'HFRI LS Index'}, axis=1, inplace=True)
hfri_ls_index = hfri_ls_index.pct_change()


fund_list = [dyn_alpha, ehp_adv, hgc, timelo, hfri_ls_index]

for fund in fund_list:

    print(fund.index[0])


start_date = start_date_finder(dates=[fund.index[0] for fund in fund_list], how='newest')
end_date = end_date_finder(dates=[fund.index[-1] for fund in fund_list], how='oldest')

date_range = pd.date_range(start_date, end_date, freq='D')

combined_hf = pd.DataFrame(index=date_range)


for fund in fund_list:

    combined_hf[fund.columns[0]] = fund

combined_hf = combined_hf.apply(pd.to_numeric)

combined_hf.fillna(0, inplace=True)
combined_hf['composite'] = combined_hf.mean(axis=1)


fig = plt.figure(figsize=(9, 6))
ax1 = fig.add_subplot(1, 1, 1)

x = 0

for fund in combined_hf.columns:

    ax1.plot(np.cumprod(1 + combined_hf[fund]), label=combined_hf.columns[x])

    x += 1

ax1.legend()
plt.show()











