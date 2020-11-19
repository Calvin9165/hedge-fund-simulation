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


fund_list = [dyn_alpha, ehp_adv, timelo, hfri_ls_index]


start_date = start_date_finder(dates=[fund.index[0] for fund in fund_list], how='newest')
end_date = end_date_finder(dates=[fund.index[-1] for fund in fund_list], how='oldest')

date_range = pd.date_range(start_date, end_date, freq='D')

combined_hf = pd.DataFrame(index=date_range)


for fund in fund_list:

    combined_hf[fund.columns[0]] = fund

combined_hf = combined_hf.apply(pd.to_numeric)

# combined_hf.fillna(0, inplace=True)
# combined_hf['composite'] = combined_hf.mean(axis=1)

combined_hf.fillna(0, axis=0, inplace=True)

# add back in hgc here, so that we can get the average performance of the funds before 2016, then once HGC is live
# we combine their returns into the average
combined_hf['hgc'] = hgc
combined_hf['hgc'].loc[hgc.index[0]:hgc.index[-1]].fillna(0, inplace=True)

# calculate the cumulative product for each investment
combined_hf = np.cumprod(1 + combined_hf, axis=0)

# calculate the composite index as the average of the other investments' returns.
combined_hf['composite'] = combined_hf.mean(axis=1)

combined_hf.plot()
plt.show()


# composite_hedge_funds = combined_hf['composite'].pct_change()
# composite_hedge_funds.to_csv('composite hedge fund returns.csv')








