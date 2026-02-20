# screener/indicators.py

import pandas as pd
import pandas_ta as ta
import config

def calculate_indicators(df):
    """Menghitung RSI, EMA, MACD, BB menggunakan pandas-ta"""
    df.ta.rsi(length=config.RSI_PERIOD, append=True)
    df.ta.ema(length=config.EMA_PERIOD, append=True)
    df.ta.macd(fast=config.MACD_FAST, slow=config.MACD_SLOW, signal=config.MACD_SIGNAL, append=True)
    df.ta.bbands(length=config.BB_PERIOD, std=config.BB_STD, append=True)
    
    # Kalkulasi custom untuk lot dan rata-rata volume
    df['Volume_Lot'] = df['Volume'] / 100
    df['Avg_Vol_20_Lot'] = df['Volume_Lot'].rolling(window=20).mean()
    
    return df