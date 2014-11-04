import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep
import datetime as dt
import numpy as np
import pandas as pd
from itertools import *
import matplotlib.pyplot as plt

def main():
    s_date = dt.datetime(2008, 1, 1)
    e_date = dt.datetime(2008, 12, 31)
    lookback = 20
    print "Reading data..."
    data, symbols, timestamps = setup(s_date, e_date, lookback)
    indicator_bol = bol_band(data, symbols, timestamps, lookback, s_date)
    event_matrix = create_matrix(indicator_bol)

def create_matrix(indicator_data):
    return

def bol_band(data, syms, timestamps, lookback, s_date):
    indicator_bol_vals = pd.DataFrame(index=timestamps, columns=syms).truncate(before=s_date)
    for sym in syms:
        prices = data['close'][sym]
        rm = pd.rolling_mean(prices, lookback).truncate(before=s_date)
        rstd = pd.rolling_std(prices, lookback).truncate(before=s_date)
        for timestamp in rm.index:
            indicator_bol_vals[sym][timestamp] = (prices[timestamp] - rm[timestamp]) / rstd[timestamp]

    return indicator_bol_vals

def setup(s_date, e_date, lookback):
    time_of_day = dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(s_date - dt.timedelta(days=lookback+10), e_date, time_of_day)
    data, symbols = read_data(timestamps)
    return data, symbols, timestamps

def read_data(timestamps):
    data_obj = da.DataAccess('Yahoo')
    symbols = ['GOOG']
    keys = ['close']
    all_data = data_obj.get_data(timestamps, symbols, keys)

    # remove NaN from price data
    all_data = dict(zip(keys, all_data))
    return all_data, symbols


if __name__ == "__main__":
    main()

