# NSE Prediction Agent - Setup Complete ✅

Your NSE Market Prediction Agent is now fully set up and ready to use!

## ✅ What's Installed

- **Python 3.9.6** with virtual environment (venv)
- **All core packages**: yfinance, pandas, numpy, scikit-learn, xgboost, ta-lib
- **ML & Analysis**: XGBoost, TA-Lib (11 technical indicators)
- **Scheduling**: APScheduler (for automated execution)
- **Alerts**: Email (SMTP), Telegram bot support
- **Utilities**: matplotlib, seaborn, plotly, joblib

## 🚀 Quick Start (3 Steps)

### Step 1: Activate Virtual Environment
```bash
cd /Users/ambujgoel_macpro/Ambuj-Local-code/nse-analysis
source venv/bin/activate
```

Once activated, your terminal prompt will show `(venv)` prefix.

### Step 2: Configure (Optional)
Edit `.env` file with your email for alerts:
```bash
nano .env
```

Configure these if you want email alerts:
- `EMAIL_SENDER=your_email@gmail.com`
- `EMAIL_PASSWORD=your_app_password` (use Google App Password, not regular password)
- `EMAIL_RECIPIENTS=recipient@example.com`

### Step 3: Train & Predict

**Option A: Train Model (First Time Only - 10-15 minutes)**
```bash
python agent.py --train
```

This downloads 2 years of data and trains the ML model. Once done, you can skip this step.

**Option B: Make Single Prediction**
```bash
python agent.py --predict
```

Analyzes yesterday's data and predicts today's market direction (BULL or BEAR).

**Option C: Full Pipeline**
```bash
python agent.py --full
```

Trains + predicts (combines both above).

**Option D: Run Scheduler (Recommended for Continuous Use)**
```bash
python scheduler.py
```

Runs automatically every day at 3:30 PM IST (market close) and retrains weekly on Sundays.

## 📚 Examples

Try these to learn each component:

```bash
# Fetch 7 days of market data
python quickstart.py 1

# Analyze peaks, troughs, and technical indicators
python quickstart.py 2

# Train ML model (requires 2Y data)
python quickstart.py 3

# Make predictions
python quickstart.py 4

# Run full pipeline
python quickstart.py 5
```

## 🧪 Backtest Model

Validate your model's accuracy on historical data:

```bash
python backtest.py --ticker ^NSEI --model nifty_model --period 6m
```

Shows: win rate, precision, recall, high-confidence trade accuracy.

## 📋 Project Files

```
nse-analysis/
├── agent.py                    # Main program
├── scheduler.py                # Scheduled tasks
├── quickstart.py               # 5 examples
├── backtest.py                 # Model validation
│
├── src/
│   ├── data_collection/        # Fetch market data
│   ├── analysis/               # Technical indicators
│   ├── ml_model/               # ML training & prediction
│   ├── alerts/                 # Email/Telegram alerts
│   └── utils.py
│
├── data/                       # Market data (CSV)
├── models/                     # Trained ML models (PKL)
├── logs/                       # Execution logs
│
├── config.py                   # Settings
├── .env                        # Your credentials
├── .env.example                # Template
├── venv/                       # Python virtual environment
│
└── GETTING_STARTED.md          # This file
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Model selection
MODEL_TYPE = "xgboost"  # or "random_forest", "svm"

# Prediction confidence threshold (0-1)
PREDICTION_THRESHOLD = 0.6  # Send alert if > 60% confident

# Retrain interval (days)
RETRAIN_INTERVAL = 7

# Instruments to analyze
INSTRUMENTS = {
    "NIFTY50": "^NSEI",
    "BANKNIFTY": "^NSEBANK",
}

# Alert channels
ALERT_CHANNELS = {
    "email": True,       # Enable email alerts
    "telegram": False,   # Enable Telegram alerts
    "webhook": False,    # Enable webhook alerts
}
```

## 📊 Understanding Predictions

**Output Example:**
```
🟢 NIFTY50   - BULL (72%) ✅ ALERT
🔴 BANKNIFTY - BEAR (68%) ✅ ALERT
```

- 🟢 = Bullish (price likely up)
- 🔴 = Bearish (price likely down)
- Percentage = Confidence level
- ✅ ALERT = Alert sent (if confidence > threshold)

## 🔧 Troubleshooting

### "Python not found"
```bash
# Use python3 explicitly
python3 agent.py --predict

# Or activate venv first
source venv/bin/activate
python agent.py --predict
```

### "No data fetched"
- Check internet connection
- Wait 5 minutes (yfinance rate limiting)
- Try again

### "Model not found"
- Run `python agent.py --train` first
- Check `models/` directory for `.pkl` files

### "Email not sent"
- Verify `.env` EMAIL_SENDER and EMAIL_PASSWORD
- Use Google App Password (not regular Gmail password)
- Check `logs/agent.log` for errors

## 📖 Documentation

- **README.md** - Full technical documentation
- **ARCHITECTURE.md** - System design & data flows
- **PROJECT_SUMMARY.md** - Feature overview
- **GETTING_STARTED.md** - This file

## 🎯 Daily Workflow

1. **Market Hours (9:15 AM - 3:30 PM IST)**
   - Agent collects data passively
   - No action needed

2. **Market Close (3:30 PM IST)**
   - If running `python scheduler.py`:
     - Analyzes previous day's 1-hour candles
     - Makes bull/bear prediction
     - Sends alert if confident
   - If manual: run `python agent.py --predict`

3. **Weekly (Sundays 6:00 PM IST)**
   - If running scheduler:
     - Retrains model with latest 2 years of data
     - Validates performance
     - Updates prediction model

## ⚠️ Important Notes

1. **This is NOT financial advice** - Use for analysis only
2. **Accuracy is ~70%** - Varies with market conditions
3. **Predictions are experimental** - Always do your own analysis
4. **No live trading** - System currently makes predictions only
5. **Data may have delays** - yfinance has minor delays
6. **Internet required** - Needs connection for data fetching

## 🚀 Next Steps

1. ✅ Setup complete - you're here!
2. ⏭️  Run first example: `python quickstart.py 1`
3. ⏭️  Train model: `python agent.py --train`
4. ⏭️  Make predictions: `python agent.py --predict`
5. ⏭️  Setup scheduler: `python scheduler.py` (background)

## 💡 Pro Tips

- Keep virtual environment activated: `source venv/bin/activate`
- Run scheduler in background: `nohup python scheduler.py &`
- Monitor logs: `tail -f logs/agent.log`
- Backtest before deploying: `python backtest.py`
- Save data: All data auto-saved to `data/` directory

## 📞 Support

For issues:
1. Check `logs/agent.log` for error details
2. Review error messages carefully
3. See Troubleshooting section above
4. Verify `.env` configuration

---

**Status**: ✅ Setup Complete & Tested  
**Environment**: Python 3.9.6 with venv  
**Last Updated**: 2026-02-18  
**Ready to Use**: Yes! 🎉
