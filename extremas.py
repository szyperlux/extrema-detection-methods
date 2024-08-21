import pandas as pd
from scipy import signal
import yfinance as yf
import os.path
import numpy as np
from scipy.signal import find_peaks, find_peaks_cwt
from scipy.ndimage import gaussian_filter1d
from pathlib import Path


data_folder = Path('data')  

def load_data (ticker, period):
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    file_name = data_folder / (ticker+'_'+period+'.csv')
    if os.path.isfile(file_name): # check if data file already exists locally
        df = pd.read_csv(file_name)
    else:  # if not, load and store data  
        df = yf.download(ticker, period=period)  # possible periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        df.to_csv(file_name)
        df.reset_index(inplace=True)
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df


def get_find_peaks_cwt_extremas (df, widths) :
    x = df['Date'].values
    y = df['Close'].values
    # find indices of extremas
    idxh = find_peaks_cwt (y, widths = widths ) # todo np.array([40,80,100,150,200])/60
    idxl = find_peaks_cwt (-y, widths = widths  ) # todo
    # create dataframes with extremas and merge them
    dfm = merge_extremas(x, y, idxh, idxl)
    # remove 'duplicates'
    return clean_extremas(dfm)


def get_find_peaks_extremas (df, prominence=5) :
    x = df['Date'].values
    y = df['Close'].values
    # find indices of extremas
    idxh, _ = find_peaks (y, prominence=prominence, width=1)
    idxl, _ = find_peaks (-y, prominence=prominence, width=1)
    # create dataframes with extremas and merge them
    dfm = merge_extremas(x, y, idxh, idxl)
    # remove 'duplicates'
    return clean_extremas(dfm)


def get_argrelmax_extremas(df, order=7) :
    x = df['Date'].values
    y = df['Close'].values
    # find indices of extremas
    idxh = signal.argrelmax(y, order=order)
    idxl = signal.argrelmin(y, order=order) 
    # create dataframes with extremas and merge them
    dfm = merge_extremas(x, y, idxh, idxl)
    # remove 'duplicates'
    return clean_extremas(dfm)


def get_argrelmax_gaussian_extremas(df, order=7, sigma=7) :
    x = df['Date'].values
    y = df['Close'].values
    # smooth data
    dataFiltered = gaussian_filter1d(y, sigma=sigma)
    # find indices of extremas on smoothed data
    idxh = signal.argrelmax(dataFiltered, order=order)
    idxl = signal.argrelmin(dataFiltered, order=order)
    # create dataframes with extremas and merge them
    dfm =  merge_extremas(x, y, idxh, idxl)
    # remove 'duplicates'
    return clean_extremas(dfm)


def merge_extremas(x, y, idxh, idxl):
    # takes two lists of extrema indices and creates a dataset with columns: Date, Extrema and Type {H|L}
    idxx = x[idxh].tolist() + x[idxl].tolist()
    idxy = y[idxh].tolist() + y[idxl].tolist()
    dfh = pd.DataFrame({'Date': x[idxh].tolist(), 'Extrema': y[idxh].tolist(), 'Type': 'H'})
    dfl = pd.DataFrame({'Date': x[idxl].tolist(), 'Extrema': y[idxl].tolist(), 'Type': 'L'})
    df = pd.concat([dfh, dfl])
    df = df.sort_values(by="Date")
    df = df.reset_index(drop=True)
    return df    


def clean_extremas(df):
    d, e = [], []
    d.append(df.Date[0])
    e.append(df.Extrema[0])      
    for i in df.index:
        if i > 0 and i+1 < len(df):
            next_ok = False
            prev_ok = False           

            if df.Type[i-1] == df.Type[i]:
                if (df.Type[i] == 'H' and df.Extrema[i-1] > df.Extrema[i]) or ( df.Type[i] == 'L' and df.Extrema[i-1] < df.Extrema[i]):
                    prev_ok = False
                else:    
                    prev_ok = True
            else:    
                prev_ok = True                

            if df.Type[i] == df.Type[i+1]:
                if (df.Type[i] == 'H' and df.Extrema[i] < df.Extrema[i+1]) or ( df.Type[i] == 'L' and df.Extrema[i] > df.Extrema[i+1]):
                    next_ok = False
                else:    
                    next_ok = True
            else:    
                next_ok = True

            if next_ok and prev_ok:
                d.append(df.Date[i])
                e.append(df.Extrema[i])     

    d.append(df.Date[len(df)-1])
    e.append(df.Extrema[len(df)-1])                      
    dfr = pd.DataFrame({'Date': d, 'Extrema':e})
    return dfr 


def get_break_days (df):
    dt_all = pd.date_range(start=df['Date'].iloc[0],end=df['Date'].iloc[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df['Date'])]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]    
    return dt_breaks

