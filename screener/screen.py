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
    tickers = get_universe() 
    results = []
    fetch_errors = []
    
    print(f"Mulai screening {len(tickers)} saham...")
    
    for ticker in tickers:
        success = False
        for attempt in range(config.MAX_RETRY):
            try:
                df = yf.download(ticker, period=config.HISTORY_PERIOD, interval=config.DATA_INTERVAL, progress=False)
                time.sleep(0.5) 
                
                if df.empty or len(df) < 30:
                    raise ValueError("Data kosong/tidak cukup")
                
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
            
            price_close = int(today['Close'])
            vol_today = int(today['Volume_Lot'])
            vol_avg = int(today['Avg_Vol_20_Lot'])
            
            pass_hard = True
            if not (config.MIN_PRICE <= price_close <= config.MAX_PRICE): pass_hard = False
            if vol_today < config.MIN_VOLUME_LOT: pass_hard = False
            if vol_today < (vol_avg * config.MIN_VOLUME_RATIO): pass_hard = False
            
            price_prev = int(yesterday['Close'])
            change_pct = round(((price_close - price_prev) / price_prev) * 100, 2)
            score = calculate_score(today, yesterday)
            signal = get_signal(score)
            
            if signal == "WEAK" or not pass_hard:
                continue

            results.append({
                "ticker": ticker,
                "ticker_display": ticker.replace(".JK", ""),
                "price_close": price_close,
                "price_change_pct": change_pct,
                "volume_ratio": round(vol_today / vol_avg, 1),
                "rsi_14": round(float(today[f'RSI_{config.RSI_PERIOD}']), 1),
                "score": score,
                "signal": signal,
                "outcome": "PENDING" # Untuk evaluasi winrate nantinya
            })
        except Exception as e:
            fetch_errors.append(ticker)

    # Metadata & Status
    wib_tz = timezone(timedelta(hours=7))
    now = datetime.now(wib_tz)
    today_str = now.strftime("%Y-%m-%d")
    status = "ok" if len(fetch_errors) == 0 else "partial"

    daily_entry = {
        "date": today_str,
        "metadata": {
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "status": status,
            "total_passed": len(results)
        },
        "results": sorted(results, key=lambda x: x['score'], reverse=True)
    }

    # --- LOGIKA PENULISAN FILE (FIX) ---
    save_path = "data/result.json" # Pastikan path sesuai dengan struktur repo
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    final_data = {"history": []}
    if os.path.exists(save_path):
        with open(save_path, 'r') as f:
            try:
                old_data = json.load(f)
                final_data["history"] = old_data.get("history", [])
            except: pass

    # Timpa data hari ini jika sudah ada (mencegah duplikat saat run berkali-kali)
    final_data["history"] = [h for h in final_data["history"] if h["date"] != today_str]
    final_data["history"].append(daily_entry)

    with open(save_path, 'w') as f:
        json.dump(final_data, f, indent=2)
    print(f"Sukses update data untuk {today_str}")

if __name__ == "__main__":
    run_screener()
