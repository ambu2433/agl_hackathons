"""
NSE Market Prediction Agent - Main orchestrator
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

import config
from src.data_collection.collector import DataCollector
from src.analysis.technical_analyzer import TechnicalAnalyzer
from src.ml_model.trainer import MLModelTrainer
from src.ml_model.predictor import PredictionEngine
from src.alerts.alert_manager import AlertManager


class NSEPredictionAgent:
    """Main agent for NSE market prediction"""
    
    def __init__(self):
        self.collector = DataCollector()
        self.analyzer = TechnicalAnalyzer()
        self.trainer = MLModelTrainer()
        self.predictor = PredictionEngine()
        self.alert_manager = AlertManager()
        
        logger.info("NSE Prediction Agent initialized")
    
    def train_models(self, instruments=None):
        """
        Train ML models for given instruments
        
        Args:
            instruments: Dict of {name: ticker} or None to use defaults
            
        Returns:
            dict: Training results for each instrument
        """
        if instruments is None:
            instruments = config.INSTRUMENTS
        
        logger.info("Starting model training pipeline...")
        results = {}
        
        for name, ticker in instruments.items():
            logger.info(f"\n{'='*50}")
            logger.info(f"Training model for {name} ({ticker})")
            logger.info(f"{'='*50}")
            
            try:
                # 1. Fetch historical data
                logger.info(f"Step 1: Fetching historical data...")
                data = self.collector.fetch_historical_data(
                    ticker,
                    period=config.HISTORY_PERIOD,
                    interval=config.DATA_INTERVAL
                )
                
                if data is None or len(data) < 100:
                    logger.error(f"Insufficient data for {name}")
                    results[name] = {'status': 'failed', 'reason': 'Insufficient data'}
                    continue
                
                # 2. Extract technical features
                logger.info(f"Step 2: Extracting technical features...")
                features_data = self.analyzer.extract_all_features(data)
                
                if features_data is None or len(features_data) < 50:
                    logger.error(f"Failed to extract features for {name}")
                    results[name] = {'status': 'failed', 'reason': 'Feature extraction failed'}
                    continue
                
                # 3. Train model
                logger.info(f"Step 3: Training ML model...")
                model_name = f"{name.lower()}_model"
                training_result = self.trainer.train_from_data(features_data, model_name)
                
                if training_result is None:
                    logger.error(f"Model training failed for {name}")
                    results[name] = {'status': 'failed', 'reason': 'Model training failed'}
                    continue
                
                results[name] = training_result
                logger.info(f"✓ Model trained successfully for {name}")
                logger.info(f"  Metrics: {training_result['metrics']}")
                
                # Load model for predictor
                self.predictor.load_model(name, model_name)
                
            except Exception as e:
                logger.error(f"Error training model for {name}: {str(e)}")
                results[name] = {'status': 'failed', 'reason': str(e)}
        
        return results
    
    def analyze_and_predict(self, instruments=None):
        """
        Analyze previous day data and make predictions
        
        Args:
            instruments: Dict of {name: ticker} or None to use defaults
            
        Returns:
            dict: Prediction summary
        """
        if instruments is None:
            instruments = config.INSTRUMENTS
        
        logger.info("\n" + "="*50)
        logger.info("Starting prediction analysis...")
        logger.info("="*50)
        
        data_dict = {}
        
        try:
            # Fetch previous day data for all instruments
            for name, ticker in instruments.items():
                logger.info(f"Fetching previous day data for {name}...")
                prev_day_data = self.collector.get_previous_day_data(ticker)
                
                if prev_day_data is None or len(prev_day_data) == 0:
                    logger.warning(f"No previous day data for {name}")
                    continue
                
                # Analyze peaks and troughs
                logger.info(f"Analyzing peaks/troughs for {name}...")
                peak_analysis = self.analyzer.get_peak_trough_analysis(prev_day_data)
                logger.info(f"Peak Analysis for {name}:")
                logger.info(f"  - Highest: {peak_analysis.get('highest_price')}")
                logger.info(f"  - Lowest: {peak_analysis.get('lowest_price')}")
                logger.info(f"  - Pattern: {peak_analysis.get('pattern_type')}")
                
                # Extract features
                features_data = self.analyzer.extract_all_features(prev_day_data)
                
                if features_data is not None and len(features_data) > 0:
                    data_dict[name] = features_data
            
            if not data_dict:
                logger.warning("No data available for prediction")
                return None
            
            # Make predictions
            logger.info("\nMaking predictions...")
            predictions = self.predictor.predict_batch(
                data_dict,
                confidence_threshold=config.PREDICTION_THRESHOLD
            )
            
            # Get summary
            summary = self.predictor.get_prediction_summary(predictions)
            
            if summary:
                logger.info("\n" + "="*50)
                logger.info("PREDICTION SUMMARY")
                logger.info("="*50)
                logger.info(f"Total Predictions: {summary['total_predictions']}")
                logger.info(f"Bull Signals: {summary['bull_signals']}")
                logger.info(f"Bear Signals: {summary['bear_signals']}")
                logger.info(f"Triggered Alerts: {summary['triggered_alerts']}")
                logger.info(f"Average Confidence: {summary['average_confidence']:.2%}")
                
                for pred in summary['details']:
                    emoji = "🟢" if pred['signal'] == 'BULL' else "🔴"
                    alert_mark = "✅ ALERT" if pred['alert_triggered'] else "❌"
                    logger.info(f"{emoji} {pred['instrument']:10s} - {pred['signal']:5s} ({pred['confidence']:.1%}) {alert_mark}")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error in prediction analysis: {str(e)}")
            return None
    
    def send_alerts(self, predictions):
        """Send alerts if predictions trigger conditions"""
        try:
            if predictions and predictions.get('triggered_alerts', 0) > 0:
                logger.info("Sending alerts...")
                self.alert_manager.send_all_alerts(predictions)
            else:
                logger.info("No alerts to send")
        except Exception as e:
            logger.error(f"Error sending alerts: {str(e)}")
    
    def run_full_pipeline(self, train=False):
        """
        Run complete pipeline: train models and make predictions
        
        Args:
            train: Whether to train models first
        """
        try:
            # Train models if requested
            if train:
                training_results = self.train_models()
                logger.info(f"\nTraining Results: {training_results}")
            
            # Make predictions
            predictions = self.analyze_and_predict()
            
            # Send alerts
            if predictions:
                self.send_alerts(predictions)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error in full pipeline: {str(e)}")
            return None


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NSE Market Prediction Agent')
    parser.add_argument('--train', action='store_true', help='Train models')
    parser.add_argument('--predict', action='store_true', help='Make predictions')
    parser.add_argument('--full', action='store_true', help='Run full pipeline')
    
    args = parser.parse_args()
    
    agent = NSEPredictionAgent()
    
    if args.train:
        agent.train_models()
    elif args.predict:
        agent.analyze_and_predict()
    elif args.full:
        agent.run_full_pipeline(train=True)
    else:
        # Default: predict only
        agent.analyze_and_predict()


if __name__ == "__main__":
    main()
