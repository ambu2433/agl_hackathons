"""
Backtesting Module - Backtest predictions on historical data
"""
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
from src.data_collection.collector import DataCollector
from src.analysis.technical_analyzer import TechnicalAnalyzer
from src.ml_model.trainer import MLModelTrainer

logger = logging.getLogger(__name__)

class Backtester:
    """Backtest model predictions on historical data"""
    
    def __init__(self):
        self.collector = DataCollector()
        self.analyzer = TechnicalAnalyzer()
        self.trainer = MLModelTrainer()
    
    def backtest_model(self, ticker, model_name, period="6m", interval="1h"):
        """
        Backtest model on historical data
        
        Args:
            ticker: Instrument ticker
            model_name: Name of trained model
            period: Period to backtest
            interval: Candle interval
            
        Returns:
            dict: Backtest results
        """
        try:
            logger.info(f"Starting backtest for {ticker}...")
            
            # Load model
            if not self.trainer.load_model(model_name):
                logger.error("Model not found")
                return None
            
            # Fetch data
            data = self.collector.fetch_historical_data(ticker, period=period, interval=interval)
            
            if data is None or len(data) < 100:
                logger.error("Insufficient data for backtest")
                return None
            
            # Extract features
            features = self.analyzer.extract_all_features(data)
            
            if features is None:
                logger.error("Failed to extract features")
                return None
            
            # Make predictions
            predictions = []
            actuals = []
            confidences = []
            
            for i in range(len(features) - 1):
                try:
                    # Get features for this row
                    row_features = features.iloc[[i]]
                    
                    # Get actual next day result
                    if features['close'].iloc[i + 1] > features['close'].iloc[i]:
                        actual = 1  # Bull
                    else:
                        actual = 0  # Bear
                    
                    # Prepare data for prediction
                    exclude_cols = ['open', 'high', 'low', 'close', 'volume']
                    feature_cols = [col for col in row_features.columns if col not in exclude_cols]
                    X = row_features[feature_cols]
                    
                    # Scale and predict
                    X_scaled = self.trainer.scaler.transform(X)
                    pred = self.trainer.model.predict(X_scaled)[0]
                    
                    # Get confidence
                    if hasattr(self.trainer.model, 'predict_proba'):
                        probs = self.trainer.model.predict_proba(X_scaled)[0]
                        conf = max(probs)
                    else:
                        conf = 0.5
                    
                    predictions.append(pred)
                    actuals.append(actual)
                    confidences.append(conf)
                    
                except Exception as e:
                    logger.warning(f"Error in prediction row {i}: {str(e)}")
                    continue
            
            # Calculate metrics
            results = self._calculate_backtest_metrics(predictions, actuals, confidences)
            results['total_backtests'] = len(predictions)
            results['ticker'] = ticker
            results['period'] = period
            
            logger.info(f"Backtest completed. Win Rate: {results['win_rate']:.2%}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error in backtest: {str(e)}")
            return None
    
    def _calculate_backtest_metrics(self, predictions, actuals, confidences):
        """Calculate backtest performance metrics"""
        try:
            predictions = np.array(predictions)
            actuals = np.array(actuals)
            confidences = np.array(confidences)
            
            # Win rate
            correct = np.sum(predictions == actuals)
            win_rate = correct / len(predictions) if len(predictions) > 0 else 0
            
            # Directional accuracy
            bull_predictions = np.sum(predictions == 1)
            bear_predictions = np.sum(predictions == 0)
            bull_actuals = np.sum(actuals == 1)
            bear_actuals = np.sum(actuals == 0)
            
            # Calculate precision and recall for each signal
            bull_tp = np.sum((predictions == 1) & (actuals == 1))
            bull_fp = np.sum((predictions == 1) & (actuals == 0))
            bear_tp = np.sum((predictions == 0) & (actuals == 0))
            bear_fp = np.sum((predictions == 0) & (actuals == 1))
            
            bull_precision = bull_tp / bull_predictions if bull_predictions > 0 else 0
            bear_precision = bear_tp / bear_predictions if bear_predictions > 0 else 0
            
            bull_recall = bull_tp / bull_actuals if bull_actuals > 0 else 0
            bear_recall = bear_tp / bear_actuals if bear_actuals > 0 else 0
            
            # Confidence analysis
            avg_confidence = np.mean(confidences)
            high_confidence_trades = np.sum(confidences >= 0.7)
            high_conf_win_rate = np.sum((predictions == actuals) & (confidences >= 0.7)) / high_confidence_trades if high_confidence_trades > 0 else 0
            
            return {
                'win_rate': win_rate,
                'total_correct': int(correct),
                'bull_predictions': int(bull_predictions),
                'bear_predictions': int(bear_predictions),
                'bull_actuals': int(bull_actuals),
                'bear_actuals': int(bear_actuals),
                'bull_precision': bull_precision,
                'bear_precision': bear_precision,
                'bull_recall': bull_recall,
                'bear_recall': bear_recall,
                'avg_confidence': avg_confidence,
                'high_confidence_trades': int(high_confidence_trades),
                'high_conf_win_rate': high_conf_win_rate,
            }
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return {}
    
    def print_backtest_report(self, results):
        """Print formatted backtest report"""
        print("\n" + "="*60)
        print("BACKTEST REPORT")
        print("="*60)
        
        print(f"\nInstrument: {results.get('ticker', 'N/A')}")
        print(f"Period: {results.get('period', 'N/A')}")
        print(f"Total Predictions: {results.get('total_backtests', 0)}")
        
        print(f"\n--- ACCURACY ---")
        print(f"Win Rate: {results.get('win_rate', 0):.2%}")
        print(f"Correct Predictions: {results.get('total_correct', 0)}")
        
        print(f"\n--- BULL SIGNALS ---")
        print(f"Predictions: {results.get('bull_predictions', 0)}")
        print(f"Actuals: {results.get('bull_actuals', 0)}")
        print(f"Precision: {results.get('bull_precision', 0):.2%}")
        print(f"Recall: {results.get('bull_recall', 0):.2%}")
        
        print(f"\n--- BEAR SIGNALS ---")
        print(f"Predictions: {results.get('bear_predictions', 0)}")
        print(f"Actuals: {results.get('bear_actuals', 0)}")
        print(f"Precision: {results.get('bear_precision', 0):.2%}")
        print(f"Recall: {results.get('bear_recall', 0):.2%}")
        
        print(f"\n--- CONFIDENCE ANALYSIS ---")
        print(f"Average Confidence: {results.get('avg_confidence', 0):.2%}")
        print(f"High Confidence Trades (≥70%): {results.get('high_confidence_trades', 0)}")
        print(f"High Confidence Win Rate: {results.get('high_conf_win_rate', 0):.2%}")
        
        print("\n" + "="*60)


def main():
    """Run backtest"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Backtest model predictions')
    parser.add_argument('--ticker', default='^NSEI', help='Ticker symbol')
    parser.add_argument('--model', default='nifty_model', help='Model name')
    parser.add_argument('--period', default='6m', help='Backtest period')
    
    args = parser.parse_args()
    
    backtester = Backtester()
    results = backtester.backtest_model(args.ticker, args.model, args.period)
    
    if results:
        backtester.print_backtest_report(results)


if __name__ == "__main__":
    main()
