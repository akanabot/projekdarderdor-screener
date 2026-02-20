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
                
                if df.empty or len(df) < 30:
                    raise ValueError("Data tidak cukup (< 30 hari)")
                
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                    
                success = True
                break # Keluar dari loop retry jika sukses
            except Exception as e:
                time.sleep(config.RETRY_DELAY_SEC)
        
        if not success:
            fetch_errors.append(ticker)
            continue

        try:
            # Kalkulasi Indikator
            df = calculate_indicators(df)
            today = df.iloc[-1]
            yesterday = df.iloc[-2]
            
            # Cek NaN (indikator belum terbentuk)
            if pd.isna(today[f'RSI_{config.RSI_PERIOD}']) or pd.isna(today[f'EMA_{config.EMA_PERIOD}']):
                fetch_errors.append(ticker)
                continue

            # Hard Filters
            price_close = int(today['Close'])
            vol_today = int(today['Volume_Lot'])
            vol_avg = int(today['Avg_Vol_20_Lot'])
            
            pass_hard = True
            if not (config.MIN_PRICE <= price_close <= config.MAX_PRICE): pass_hard = False
            if vol_today < config.MIN_VOLUME_LOT: pass_hard = False
            if vol_today < (vol_avg * config.MIN_VOLUME_RATIO): pass_hard = False
            
            # Hitung persentase
            price_prev = int(yesterday['Close'])
            change_pct = round(((price_close - price_prev) / price_prev) * 100, 2)
            ema20 = round(float(today[f'EMA_{config.EMA_PERIOD}']), 2)
            price_vs_ema_pct = round(((price_close - ema20) / ema20) * 100, 2)

            # Hitung Skor & Signal
            score = calculate_score(today, yesterday)
            signal = get_signal(score)
            
            # Sesuai Schema: Buang yang "WEAK" atau tidak lolos hard filter
            if signal == "WEAK" or not pass_hard:
                continue

            # Bentuk Objek Sesuai Contract
            macd_col = f'MACDh_{config.MACD_FAST}_{config.MACD_SLOW}_{config.MACD_SIGNAL}'
            
            results.append({
                "ticker": ticker,
                "ticker_display": ticker.replace(".JK", ""),
                "price_close": price_close,
                "price_prev_close": price_prev,
                "price_change_pct": change_pct,
                "volume_today": vol_today * 100, # Kembalikan ke lembar untuk output JSON jika diperlukan, atau keep Lot. Mengikuti spec: 125000000
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

    # Sort DESC by score
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    # Status handling (Error Rule: Bagian 8)
    total_screened = len(tickers)
    error_count = len(fetch_errors)
    
    if error_count / total_screened > config.FAIL_THRESHOLD_PCT:
        status = "error"
        print("CRITICAL: Gagal total (>50% ticker gagal). JSON tidak di-overwrite.")
        return # Keluar tanpa simpan JSON
    elif error_count > 0:
        status = "partial"
    else:
        status = "ok"

    # Waktu WIB (UTC+7)
    wib_tz = timezone(timedelta(hours=7))
    now = datetime.now(wib_tz)

    # Susun Metadata Schema
    output = {
        "metadata": {
            "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S+07:00"),
            "generated_by": "github-actions",
            "total_screened": total_screened,
            "total_passed": len(results),
            "fetch_errors": fetch_errors,
            "data_date": now.strftime("%Y-%m-%d"),
            "status": status
        },
        "results": results
    }

    # Pastikan folder ada
    os.makedirs(os.path.dirname(config.OUTPUT_PATH), exist_ok=True)
    
    # Save JSON
    # Kita menggunakan root direktori '../data/result.json' karena script ini dijalankan dari root oleh GitHub Actions
    save_path = f"../{config.OUTPUT_PATH}" if not os.path.exists(config.OUTPUT_PATH) else config.OUTPUT_PATH
    
    with open(config.OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
        
    print(f"Selesai! {len(results)} lolos. Status: {status}. Output: {config.OUTPUT_PATH}")

if __name__ == "__main__":
    run_screener()