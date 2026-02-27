# Getting Started - NSE Prediction Agent

Complete step-by-step guide to get the agent running in 10 minutes.

## Prerequisites

- Python 3.8+
- pip or conda
- Internet connection (for market data)

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd nse-analysis
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Email alerts (Optional but recommended)
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENTS=your_email@gmail.com

# Other settings (Optional)
TELEGRAM_BOT_TOKEN=xxx (leave blank to skip)
UPSTOX_API_KEY=xxx (leave blank to skip)
```

**Note for Gmail**: 
- Use [Google App Passwords](https://myaccount.google.com/apppasswords)
- Not your regular Gmail password

### Step 3: Run Quick Example

Test data collection:

```bash
python quickstart.py 1
```

This fetches 7 days of NIFTY50 data and displays it.

## Training Your Model (First Time)

```bash
# Train model on 2 years of historical data
python agent.py --train
```

This process:
1. Fetches 2 years of historical 1-hour candles
2. Extracts 11 technical features
3. Creates Bull/Bear labels
4. Trains XGBoost model
5. Saves model to `models/` directory

⏱️ **Time**: 10-15 minutes (mostly download time)

📊 **Output**: Model accuracy, precision, recall, F1-score

## Making Predictions

### Option 1: Single Prediction Run

```bash
python agent.py --predict
```

Analyzes yesterday's data and predicts today's market direction.

### Option 2: Continuous Monitoring (Recommended)

```bash
python scheduler.py
```

Runs automatically:
- **Daily at 3:30 PM IST**: Analyzes and makes prediction
- **Every Sunday 6 PM IST**: Retrains model with latest data

Press `Ctrl+C` to stop.

## Quick Test Examples

Run individual examples to understand each component:

```bash
# Example 1: Fetch data
python quickstart.py 1

# Example 2: Technical analysis
python quickstart.py 2

# Example 3: Train model
python quickstart.py 3

# Example 4: Make predictions
python quickstart.py 4

# Example 5: Full pipeline
python quickstart.py 5
```

## Backtest Model

Validate model performance on historical data:

```bash
python backtest.py --ticker ^NSEI --model nifty_model --period 6m
```

Output:
- Win rate
- Precision/Recall for Bull and Bear signals
- High-confidence trade performance

## Project Structure

```
nse-analysis/
├── agent.py                    # Main agent
├── scheduler.py                # Run on schedule
├── quickstart.py               # Examples
├── backtest.py                 # Backtesting
│
├── src/
│   ├── data_collection/        # Fetch market data
│   ├── analysis/               # Technical indicators
│   ├── ml_model/               # ML training & prediction
│   ├── alerts/                 # Email/Telegram alerts
│   └── utils.py                # Helper functions
│
├── data/                       # Market data (CSV)
├── models/                     # Trained ML models
├── logs/                       # Log files
│
├── config.py                   # Configuration
├── requirements.txt            # Dependencies
├── .env.example                # Environment template
└── README.md                   # Full documentation
```

## Configuration

Edit `config.py` to customize:

```python
# Change model type
MODEL_TYPE = "xgboost"  # or "random_forest", "svm"

# Adjust prediction threshold (confidence required for alert)
PREDICTION_THRESHOLD = 0.6  # 60% confidence

# Retrain interval
RETRAIN_INTERVAL = 7  # days

# Enable/disable alert channels
ALERT_CHANNELS = {
    "email": True,
    "telegram": False,
    "webhook": False,
}
```

## Understanding Predictions

### Output Example

```
🟢 NIFTY50   - BULL (72%) ✅ ALERT
🔴 BANKNIFTY - BEAR (68%) ✅ ALERT
```

### What It Means

- 🟢 = Bullish prediction (price likely to go up)
- 🔴 = Bearish prediction (price likely to go down)
- Percentage = Confidence level
- ✅ ALERT = Confidence exceeds threshold (action signals)

### Confidence Levels

- 90%+ : Very high confidence
- 70-90% : High confidence
- 60-70% : Moderate confidence
- <60% : Low confidence (needs tuning)

## Troubleshooting

### Problem: "No data fetched"

```
Error: No data fetched for ^NSEI
```

**Solution**:
- Wait 5 minutes (yfinance rate limiting)
- Check internet connection
- Try a different ticker

### Problem: "Insufficient data for training"

```
Error: Insufficient data for training
```

**Solution**:
- Ensure you have internet (needs to download 2 years of data)
- Try manually: `python quickstart.py 1`

### Problem: "Email not sent"

```
Error: SMTP connection failed
```

**Solutions**:
- Check .env EMAIL_SENDER and EMAIL_PASSWORD
- For Gmail: Use App Password, NOT regular password
- Enable "Less secure app access" if not using App Password

### Problem: "Model file not found"

```
Error: Model not found
```

**Solution**: Train first with `python agent.py --train`

## Next Steps

1. **Train your model**: `python agent.py --train`
2. **Test predictions**: `python quickstart.py 5`
3. **Backtest**: `python backtest.py`
4. **Set up scheduler**: `python scheduler.py`
5. **Monitor logs**: `tail -f logs/agent.log`

## Getting Help

- Check [README.md](README.md) for detailed documentation
- Review `logs/agent.log` for error details
- See example problems in Troubleshooting section

## Common Tasks

### Train on Latest Data

```bash
python agent.py --train
```

### Test Prediction Once

```bash
python agent.py --predict
```

### Train + Predict (Full Pipeline)

```bash
python agent.py --full
```

### Validate Model (6-month backtest)

```bash
python backtest.py --period 6m
```

### Run on Schedule (Recommended)

```bash
python scheduler.py
```

---

**Congratulations!** You now have a working NSE market prediction agent. 🎉

For more information, see [README.md](README.md)
