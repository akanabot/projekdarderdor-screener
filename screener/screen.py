# screener/screen.py

import yfinance as yf
import pandas as pd
import json
import os
import time
from datetime import datetime, timezone, timedelta
import config
from universe import get_universe
from indicators import calculate_indicators
from scoring import calculate_score, get_signal

def run_screener():
    tickers = get_universe() # Memanggil fungsi dari universe.py
    results = []
    fetch_errors = []
    
    print(f"Mulai screening {len(tickers)} saham...")
    
    for ticker in tickers:
        success = False
        for attempt in range(config.MAX_RETRY):
            try:
                # Ambil data
                df = yf.download(ticker, period=config.HISTORY_PERIOD, interval=config.DATA_INTERVAL, progress=False)
                
                # --- JEDA UNTUK KEAMANAN (ANTI-BOT) ---
                time.sleep(0.5) 
                
                if df.empty or len(df) < 30:
                    raise ValueError("Data kosong/tidak cukup")
                
                # Perbaikan MultiIndex jika diperlukan
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                success = True
                break
            except Exception as e:
                print(f"Gagal ambil {ticker} (Percobaan {attempt+1}): {e}")
                time.sleep(config.RETRY_DELAY_SEC)
        
        if not success:
            fetch_errors.append(ticker)
            continue

        try:
            df = calculate_indicators(df)
            today = df.iloc[-1]
            yesterday = df.iloc[-2]
            
            if pd.isna(today[f'RSI_{config.RSI_PERIOD}']) or pd.isna(today[f'EMA_{config.EMA_PERIOD}']):
                fetch_errors.append(ticker)
                continue

            price_close = int(today['Close'])
            vol_today = int(today['Volume_Lot'])
            vol_avg = int(today['Avg_Vol_20_Lot'])
            
            pass_hard = True
            if not (config.MIN_PRICE <= price_close <= config.MAX_PRICE): pass_hard = False
            if vol_today < config.MIN_VOLUME_LOT: pass_hard = False
            if vol_today < (vol_avg * config.MIN_VOLUME_RATIO): pass_hard = False
            
            price_prev = int(yesterday['Close'])
            change_pct = round(((price_close - price_prev) / price_prev) * 100, 2)
            ema20 = round(float(today[f'EMA_{config.EMA_PERIOD}']), 2)
            price_vs_ema_pct = round(((price_close - ema20) / ema20) * 100, 2)

            score = calculate_score(today, yesterday)
            signal = get_signal(score)
            
            if signal == "WEAK" or not pass_hard:
                continue

            macd_col = f'MACDh_{config.MACD_FAST}_{config.MACD_SLOW}_{config.MACD_SIGNAL}'
            
            results.append({
                "ticker": ticker,
                "ticker_display": ticker.replace(".JK", ""),
                "price_close": price_close,
                "price_prev_close": price_prev,
                "price_change_pct": change_pct,
                "volume_today": vol_today * 100,
                "volume_avg_20d": vol_avg * 100,
                "volume_ratio": round(vol_today / vol_avg, 1),
                "rsi_14": round(float(today[f'RSI_{config.RSI_PERIOD}']), 1),
                "ema_20": ema20,
                "price_vs_ema_pct": price_vs_ema_pct,
                "macd_histogram": round(float(today[macd_col]), 3),
                "bb_upper": round(float(today[f'BBU_{config.BB_PERIOD}_{config.BB_STD}']), 1),
                "bb_middle": round(float(today[f'BBM_{config.BB_PERIOD}_{config.BB_STD}']), 1),
                "bb_lower": round(float(today[f'BBL_{config.BB_PERIOD}_{config.BB_STD}']), 1),
                "score": score,
                "signal": signal,
                "pass_hard_filter": pass_hard
            })

        except Exception as e:
            print(f"Error proses {ticker}: {str(e)}")
            fetch_errors.append(ticker)

    results = sorted(results, key=lambda x: x['score'], reverse=True)

    total_screened = len(tickers)
    error_count = len(fetch_errors)
    
    if error_count / total_screened > config.FAIL_THRESHOLD_PCT:
        status = "error"
        print("CRITICAL: Gagal total (>50% ticker gagal). JSON tidak di-overwrite.")
        return
    elif error_count > 0:
        status = "partial"
    else:
        status = "ok"

    wib_tz = timezone(timedelta(hours=7))
    now = datetime.now(wib_tz)
    today_str = now.strftime("%Y-%m-%d")

    daily_entry = {
        "date": today_str,
        "metadata": {
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "generated_by": "github-actions",
            "total_screened": total_screened,
            "total_passed": len(results),
            "fetch_errors": fetch_errors,
            "data_date": today_str,
            "status": status
        },
        "results": results
    }

    os.makedirs(os.path.dirname(config.OUTPUT_PATH), exist_ok=True)
    save_path = f"../{config.OUTPUT_PATH}" if not os.path.exists(config.OUTPUT_PATH)