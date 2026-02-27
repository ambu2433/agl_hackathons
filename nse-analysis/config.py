"""
Configuration settings for NSE Market Prediction Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application Settings
APP_NAME = "NSE Market Prediction Agent"
LOG_LEVEL = "INFO"
LOG_FILE = "logs/agent.log"

# Data Collection
DATA_INTERVAL = "1h"  # 1-hour candles for analysis
HISTORY_PERIOD = "2y"  # 2 years of historical data for training
DATA_DIR = "data"
MODELS_DIR = "models"

# Instruments
INSTRUMENTS = {
    "NIFTY50": "^NSEI",  # yfinance ticker
    "BANKNIFTY": "^NSEBANK",  # yfinance ticker
}

# Upstox API (Optional - if you have API key)
UPSTOX_API_KEY = os.getenv("UPSTOX_API_KEY", "")

# ML Model Settings
TRAIN_TEST_SPLIT = 0.8
MODEL_TYPE = "xgboost"  # xgboost, random_forest, svm
PREDICTION_THRESHOLD = 0.6  # Confidence threshold for alerts
RETRAIN_INTERVAL = 7  # Retrain model every 7 days

# Alert Settings
ALERT_ENABLED = True
ALERT_CHANNELS = {
    "email": True,
    "telegram": False,
    "webhook": False,
}

# Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENTS = os.getenv("EMAIL_RECIPIENTS", "").split(",")

# Telegram Settings (Optional)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Feature Engineering
FEATURES = [
    "sma_20",      # Simple Moving Average 20
    "sma_50",      # Simple Moving Average 50
    "rsi",         # Relative Strength Index
    "macd",        # MACD
    "bollinger_upper",  # Bollinger Bands Upper
    "bollinger_lower",  # Bollinger Bands Lower
    "volume_ratio",  # Volume compared to average
    "candle_pattern",  # Candlestick pattern
    "high_low_ratio",  # High to Low ratio
    "close_open_ratio",  # Close to Open ratio
]

# Market Hours (IST)
MARKET_OPEN = "09:15"
MARKET_CLOSE = "15:30"
TRADE_ANALYSIS_TIME = "15:30"  # Analyze previous day data at market close
