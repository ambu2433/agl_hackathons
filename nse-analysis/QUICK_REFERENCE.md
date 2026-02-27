# NSE Agent - Quick Reference

## ⚡ Most Common Commands

```bash
# Activate environment
source venv/bin/activate

# Make a prediction (analyze yesterday's data)
python agent.py --predict

# Train model (first time, ~15 min)
python agent.py --train

# Run scheduler (daily 3:30 PM IST, weekly retraining)
python scheduler.py

# Run example
python quickstart.py 1      # Fetch data
python quickstart.py 2      # Analyze
python quickstart.py 3      # Train
python quickstart.py 4      # Predict
python quickstart.py 5      # Full pipeline

# Backtest model
python backtest.py --period 6m
```

## 📊 Output Example

```
🟢 NIFTY50   - BULL (72%) ✅ ALERT
🔴 BANKNIFTY - BEAR (68%) ✅ ALERT

Summary:
  Total: 2
  Bulls: 1
  Bears: 1
  Alerts: 2
```

## ⚙️ Key Files

| File | Purpose |
|------|---------|
| `agent.py` | Main program |
| `config.py` | Settings (model type, threshold, etc.) |
| `.env` | Email/Telegram credentials |
| `scheduler.py` | Automated daily/weekly runs |
| `quickstart.py` | 5 learning examples |
| `backtest.py` | Model validation |
| `logs/agent.log` | Execution log |

## 📈 Workflow

1. **Setup** (one-time): `source setup.sh`
2. **Train** (one-time): `python agent.py --train`
3. **Predict** (daily): `python agent.py --predict`
4. **Schedule** (optional): `python scheduler.py`

## 🔧 Configure Alerts (Optional)

Edit `.env`:
```
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENTS=recipient@example.com
```

For Gmail: Use [App Password](https://myaccount.google.com/apppasswords), not regular password.

## 📚 Documentation

- `SETUP_COMPLETE.md` - This setup
- `GETTING_STARTED.md` - Detailed guide
- `README.md` - Full documentation
- `ARCHITECTURE.md` - Technical design
- `PROJECT_SUMMARY.md` - Feature overview

## ⚠️ Remember

- This is analysis tool, NOT financial advice
- Accuracy ~70%, varies with market conditions
- Always verify predictions independently
- Keep `.env` credentials secure
