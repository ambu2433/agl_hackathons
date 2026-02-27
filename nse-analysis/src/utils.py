"""
Utilities - Helper functions for the agent
"""
import pandas as pd
import numpy as np
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class DataUtils:
    """Data manipulation utilities"""
    
    @staticmethod
    def get_market_hours():
        """Get NSE market hours"""
        return {
            'open': '09:15',
            'close': '15:30',
            'timezone': 'Asia/Kolkata'
        }
    
    @staticmethod
    def is_market_open():
        """Check if market is currently open"""
        from datetime import datetime
        import pytz
        
        tz = pytz.timezone('Asia/Kolkata')
        now = datetime.now(tz)
        
        # Market is open Monday-Friday, 9:15 AM to 3:30 PM
        if now.weekday() >= 5:  # Weekend
            return False
        
        market_open = now.replace(hour=9, minute=15, second=0)
        market_close = now.replace(hour=15, minute=30, second=0)
        
        return market_open <= now <= market_close
    
    @staticmethod
    def get_last_trading_day():
        """Get last trading day"""
        from datetime import datetime, timedelta
        import pytz
        
        tz = pytz.timezone('Asia/Kolkata')
        today = datetime.now(tz).date()
        
        # Go back to find last trading day (exclude weekends)
        last_day = today - timedelta(days=1)
        while last_day.weekday() >= 5:  # Weekend
            last_day -= timedelta(days=1)
        
        return last_day
    
    @staticmethod
    def round_to_nearest_step(value, step=0.05):
        """Round price to nearest step (for NSE, usually 0.05)"""
        return round(value / step) * step


class MetricsUtils:
    """Model metrics utilities"""
    
    @staticmethod
    def get_model_score_interpretation(accuracy):
        """Interpret model accuracy score"""
        if accuracy >= 0.9:
            return "Excellent", "🟢"
        elif accuracy >= 0.8:
            return "Very Good", "🟢"
        elif accuracy >= 0.7:
            return "Good", "🟡"
        elif accuracy >= 0.6:
            return "Fair", "🟡"
        else:
            return "Poor", "🔴"
    
    @staticmethod
    def get_confidence_interpretation(confidence):
        """Interpret confidence level"""
        confidence_pct = confidence * 100
        if confidence_pct >= 80:
            return "Very High", "🟢"
        elif confidence_pct >= 70:
            return "High", "🟢"
        elif confidence_pct >= 60:
            return "Moderate", "🟡"
        elif confidence_pct >= 50:
            return "Low", "🔴"
        else:
            return "Very Low", "🔴"
    
    @staticmethod
    def format_metrics_report(metrics):
        """Format metrics as readable report"""
        report = f"""
Model Performance Report
========================
Accuracy:   {metrics['accuracy']:.2%}
Precision:  {metrics['precision']:.2%}
Recall:     {metrics['recall']:.2%}
F1-Score:   {metrics['f1_score']:.2%}

Confusion Matrix:
{np.array(metrics['confusion_matrix'])}
"""
        return report


class FileUtils:
    """File handling utilities"""
    
    @staticmethod
    def save_json(data, filepath):
        """Save data as JSON"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            logger.info(f"Saved JSON to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving JSON: {str(e)}")
            return False
    
    @staticmethod
    def load_json(filepath):
        """Load JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            logger.info(f"Loaded JSON from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading JSON: {str(e)}")
            return None
    
    @staticmethod
    def ensure_directory(directory):
        """Ensure directory exists"""
        Path(directory).mkdir(parents=True, exist_ok=True)


class AnalysisUtils:
    """Analysis utilities"""
    
    @staticmethod
    def calculate_win_rate(predictions, actual_values):
        """Calculate win rate from predictions"""
        correct = sum(1 for pred, actual in zip(predictions, actual_values) if pred == actual)
        return correct / len(predictions) if len(predictions) > 0 else 0
    
    @staticmethod
    def calculate_risk_reward_ratio(entry, stop_loss, take_profit):
        """Calculate risk/reward ratio"""
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)
        
        if risk == 0:
            return 0
        
        return reward / risk
    
    @staticmethod
    def calculate_position_size(capital, risk_percent, entry, stop_loss):
        """Calculate position size for risk management"""
        risk_amount = capital * (risk_percent / 100)
        price_risk = abs(entry - stop_loss)
        
        if price_risk == 0:
            return 0
        
        quantity = risk_amount / price_risk
        return quantity


class MarketUtils:
    """Market data utilities"""
    
    @staticmethod
    def get_market_sentiment(bull_signals, bear_signals):
        """Determine overall market sentiment"""
        if bull_signals == 0 and bear_signals == 0:
            return "Neutral", "⚪"
        
        total = bull_signals + bear_signals
        bull_ratio = bull_signals / total
        
        if bull_ratio > 0.65:
            return "Strongly Bullish", "🟢"
        elif bull_ratio > 0.50:
            return "Bullish", "🟢"
        elif bull_ratio > 0.35:
            return "Bearish", "🔴"
        else:
            return "Strongly Bearish", "🔴"
    
    @staticmethod
    def format_price_display(price, decimal_places=2):
        """Format price for display"""
        return f"₹{price:,.{decimal_places}f}"


def main():
    """Test utilities"""
    print("Market Status:")
    print(f"  Open: {DataUtils.is_market_open()}")
    print(f"  Last Trading Day: {DataUtils.get_last_trading_day()}")
    
    print("\nSentiment Test:")
    sentiment, emoji = MarketUtils.get_market_sentiment(3, 1)
    print(f"  3 Bull + 1 Bear: {emoji} {sentiment}")
    
    print("\nMetrics Test:")
    metrics = {
        'accuracy': 0.75,
        'precision': 0.78,
        'recall': 0.72,
        'f1_score': 0.75,
        'confusion_matrix': [[10, 3], [2, 15]]
    }
    print(MetricsUtils.format_metrics_report(metrics))


if __name__ == "__main__":
    main()
