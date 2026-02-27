# NSE Market Prediction Agent

A machine learning-based agent that analyzes NSE Index and Banknifty market data to predict bullish or bearish trends for the next trading day.

## Project Overview

This agent performs the following tasks:

1. **Data Collection**: Fetches historical 1-hour candlestick data from yfinance
2. **Technical Analysis**: Extracts features including:
   - Moving Averages (SMA 20, 50)
   - RSI (Relative Strength Index)
   - MACD
   - Bollinger Bands
   - Volume ratios
   - Price patterns (peaks, troughs)

3. **ML Model Training**: Trains XGBoost/Random Forest models to predict Bull/Bear markets
4. **Prediction**: Analyzes previous day's data and predicts next day's direction
5. **Alerts**: Sends notifications via email/Telegram when predictions cross confidence threshold

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  NSE Prediction Agent                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Data Collection Layer                                  │
│  ├── yfinance (NIFTY50, BANKNIFTY)                     │
│  └── Upstox API (optional)                             │
│                                                         │
│  Technical Analysis Layer                               │
│  ├── Peak/Trough Detection                             │
│  ├── Moving Averages                                    │
│  ├── RSI, MACD, Bollinger Bands                        │
│  └── Volume Analysis                                   │
│                                                         │
│  ML Model Layer                                         │
│  ├── Feature Engineering                               │
│  ├── Model Training (XGBoost/Random Forest)            │
│  ├── Model Evaluation & Validation                     │
│  └── Model Persistence (joblib)                        │
│                                                         │
│  Prediction Engine                                      │
│  ├── Load trained models                               │
│  ├── Generate predictions                              │
│  └── Calculate confidence scores                       │
│                                                         │
│  Alert System                                           │
│  ├── Email alerts                                       │
│  ├── Telegram notifications                            │
│  └── Webhook integration                               │
│                                                         │
│  Scheduler                                              │
│  ├── Daily analysis (3:30 PM IST)                     │
│  └── Weekly model retraining (Sundays)                │
└─────────────────────────────────────────────────────────┘
```

## Installation

### 1. Clone and Setup

```bash
cd nse-analysis
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

Edit `config.py` for:
- Model type (xgboost, random_forest, svm)
- Prediction threshold
- Alert channels
- Retraining interval

## Usage

### Train Models

```bash
python agent.py --train
```

This will:
1. Download 2 years of historical data for NSE Index and Banknifty
2. Extract technical features
3. Train ML models
4. Save trained models to `models/` directory

### Make Predictions

```bash
python agent.py --predict
```

Analyzes previous day's data and predicts next day's direction.

### Run Full Pipeline (Train + Predict)

```bash
python agent.py --full
```

### Run Scheduler

```bash
python scheduler.py
```

Runs the agent automatically:
- Daily at 3:30 PM IST (market close)
- Weekly on Sundays at 6:00 PM IST (model retraining)

## File Structure

```
nse-analysis/
├── config.py                          # Configuration settings
├── agent.py                           # Main agent orchestrator
├── scheduler.py                       # Task scheduling
├── requirements.txt                   # Dependencies
├── .env.example                       # Environment template
│
├── src/
│   ├── data_collection/
│   │   └── collector.py              # Data fetching (yfinance, Upstox)
│   │
│   ├── analysis/
│   │   └── technical_analyzer.py     # Technical indicators & peak/trough detection
│   │
│   ├── ml_model/
│   │   ├── trainer.py                # Model training pipeline
│   │   └── predictor.py              # Prediction engine
│   │
│   └── alerts/
│       └── alert_manager.py          # Email, Telegram, webhook alerts
│
├── data/                             # Historical data (CSV files)
├── models/                           # Trained ML models (PKL files)
└── logs/                             # Log files
```

## Configuration

### Key Settings in `config.py`

```python
# Data
DATA_INTERVAL = "1h"                    # 1-hour candles
HISTORY_PERIOD = "2y"                   # 2 years for training

# Model
MODEL_TYPE = "xgboost"                  # Model type
PREDICTION_THRESHOLD = 0.6              # Confidence threshold for alerts
RETRAIN_INTERVAL = 7                    # Days between retraining

# Instruments
INSTRUMENTS = {
    "NIFTY50": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
}
```

### Environment Variables (.env)

```env
# Email
SMS_SERVER=smtp.gmail.com
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENTS=alert@example.com

# Telegram (optional)
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
```

## Features & Technical Indicators

### Extracted Features

1. **Simple Moving Averages**: SMA 20, SMA 50
2. **Relative Strength Index (RSI)**: Momentum indicator
3. **MACD**: Moving Average Convergence Divergence
4. **Bollinger Bands**: Volatility bands
5. **Volume Ratio**: Current vs average volume
6. **Price Ratios**: High-Low and Close-Open ratios
7. **Peak/Trough Detection**: Local highs and lows

### Peak & Bottom Analysis

The agent identifies:
- **Peaks**: Local price highs in the 1-hour chart
- **Troughs**: Local price lows in the 1-hour chart
- **Patterns**:
  - `bullish_breakout`: Price breaks above last peak
  - `bearish_breakdown`: Price breaks below last trough
  - `consolidation`: Price between peak and trough

## Model Training

### Training Data
- **Period**: Last 2 years of historical data
- **Interval**: 1-hour candles
- **Train/Test Split**: 80/20

### Labels
- **Bull (1)**: Close price next day > Close price current day
- **Bear (0)**: Close price next day ≤ Close price current day

### Models Available
- **XGBoost**: Default, best performance
- **Random Forest**: Alternative, more interpretable
- **SVM**: Alternative with different learning curve

### Metrics
The agent tracks:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

## Predictions & Alerts

### Prediction Output

```json
{
  "instrument": "NIFTY50",
  "signal": "BULL",
  "confidence": 0.72,
  "alert_triggered": true,
  "timestamp": "2024-01-15 15:30:00"
}
```

### Alert Conditions

Alerts are triggered when:
- Confidence score > PREDICTION_THRESHOLD (default: 60%)
- AND alert channels are enabled

### Alert Channels

1. **Email**: HTML formatted with prediction details
2. **Telegram**: Rich text with emojis
3. **Webhook**: JSON payload for integration with trading platforms

## Dependencies

### Core Libraries
- **yfinance**: Market data collection
- **pandas/numpy**: Data manipulation
- **scikit-learn**: ML utilities
- **xgboost**: XGBoost models
- **ta-lib**: Technical analysis

### Scheduling & Alerts
- **APScheduler**: Task scheduling
- **python-telegram-bot**: Telegram integration
- **python-dotenv**: Environment management

## Limitations & Considerations

⚠️ **Important**: This is a prediction tool, not financial advice.

1. **Historical Data**: NSE data from yfinance may lag real-time data
2. **Market Hours**: Predictions based on 1-hour candles during market hours (9:15 AM - 3:30 PM IST)
3. **Accuracy**: Model accuracy depends on market conditions and historical data
4. **False Signals**: Confidence threshold should be tuned based on risk tolerance
5. **No Guarantee**: Past performance ≠ Future results

## Getting Started Example

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your email credentials

# 3. Train models (first run)
python agent.py --train

# 4. Make predictions
python agent.py --predict

# 5. Run scheduler for automated daily analysis
python scheduler.py
```

## Troubleshooting

### Issue: "No data fetched for ticker"
- **Cause**: yfinance cannot fetch data (may be throttled)
- **Solution**: Wait a few minutes and try again, or use Upstox API

### Issue: "Insufficient data for training"
- **Cause**: Less than 100 data points available
- **Solution**: Ensure you have internet connection, try fetching fresh data

### Issue: "Email not sent"
- **Cause**: SMTP credentials incorrect
- **Solution**: Check .env file, use app-specific password for Gmail

### Issue: "Model file not found"
- **Cause**: Models not trained yet
- **Solution**: Run `python agent.py --train` first

## Next Steps

1. **Backtesting**: Add historical backtesting module
2. **Risk Management**: Implement position sizing and stop-loss logic
3. **Multi-Timeframe**: Analyze daily/weekly charts in addition to hourly
4. **Advanced ML**: Add deep learning models (LSTM, Transformer)
5. **Platform Integration**: Connect to broker APIs for automated trading
6. **Live Monitoring**: Web dashboard for real-time monitoring

## License

MIT License

## Support

For issues, create a GitHub issue with:
- Error messages (from logs/)
- Steps to reproduce
- System information (OS, Python version)

---

**Last Updated**: 2026-02-18
**Version**: 1.0.0
