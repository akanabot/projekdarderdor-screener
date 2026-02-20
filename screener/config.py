# screener/config.py

# Universe
UNIVERSE_FILE = "screener/universe.py"

# Data fetch
HISTORY_PERIOD = "3mo"
DATA_INTERVAL = "1d"

# Hard filter
MIN_VOLUME_LOT = 500_000
MIN_VOLUME_RATIO = 1.3
MIN_PRICE = 200
MAX_PRICE = 20_000
MIN_FREQUENCY = 1_000 # (Disimpan sesuai spek, meski yfinance tidak sediakan data frekuensi)

# Indikator teknikal
RSI_PERIOD = 14
EMA_PERIOD = 20
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2.0

# RSI range
RSI_MIN = 35
RSI_MAX = 60

# Scoring weights
WEIGHT_VOLUME_SPIKE = 30
WEIGHT_RSI_POSITION = 20
WEIGHT_PRICE_VS_EMA = 20
WEIGHT_MACD_SIGNAL = 15
WEIGHT_CANDLE_BODY = 15

# Threshold score
SCORE_STRONG = 70
SCORE_MODERATE = 50

# Error handling
MAX_RETRY = 3
RETRY_DELAY_SEC = 10
FAIL_THRESHOLD_PCT = 0.5

# Output
OUTPUT_PATH = "data/result.json"
TIMEZONE = "Asia/Jakarta"