# screener/scoring.py

import config

def calculate_score(today, yesterday):
    """Menghitung skor berdasarkan parameter di config.py"""
    score = 0
    
    # 1. Volume Spike Score (Max 30)
    vol_ratio = today['Volume_Lot'] / today['Avg_Vol_20_Lot']
    if vol_ratio >= 3.0: score += 30
    elif vol_ratio >= 2.0: score += 22
    elif vol_ratio >= 1.5: score += 15
    elif vol_ratio >= 1.3: score += 8

    # 2. RSI Position Score (Max 20)
    rsi = today[f'RSI_{config.RSI_PERIOD}']
    if 45 <= rsi <= 55: score += 20
    elif 35 <= rsi <= 44: score += 14
    elif 56 <= rsi <= 60: score += 10

    # 3. Price vs EMA20 Score (Max 20)
    ema20 = today[f'EMA_{config.EMA_PERIOD}']
    close = today['Close']
    pct_ema = ((close - ema20) / ema20) * 100
    if 0 < pct_ema <= 1: score += 20
    elif 1 < pct_ema <= 3: score += 15
    elif 3 < pct_ema <= 5: score += 8
    elif pct_ema > 5: score += 3

    # 4. MACD Histogram Score (Max 15)
    macd_hist_col = f'MACDh_{config.MACD_FAST}_{config.MACD_SLOW}_{config.MACD_SIGNAL}'
    hist_today = today[macd_hist_col]
    hist_yday = yesterday[macd_hist_col]
    
    if hist_today > 0 and hist_today > hist_yday: score += 15
    elif hist_today > 0 and hist_today <= hist_yday: score += 8
    elif hist_today <= 0 and hist_today > hist_yday: score += 5

    # 5. Candle Body Score (Max 15)
    open_price = today['Open']
    body_pct = ((close - open_price) / open_price) * 100
    if body_pct >= 1.5: score += 15
    elif body_pct >= 0.5: score += 10
    elif body_pct >= 0: score += 5
    
    return score

def get_signal(score):
    if score >= config.SCORE_STRONG: return "STRONG"
    if score >= config.SCORE_MODERATE: return "MODERATE"
    return "WEAK"