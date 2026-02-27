"""
Prediction Engine - Make predictions using trained models
"""
import pandas as pd
import numpy as np
import logging
from src.ml_model.trainer import MLModelTrainer
import config

logger = logging.getLogger(__name__)

class PredictionEngine:
    """Makes market predictions using trained models"""
    
    def __init__(self):
        self.trainer = MLModelTrainer()
        self.models = {}
    
    def load_model(self, instrument, filename):
        """Load a trained model for an instrument"""
        try:
            self.trainer.load_model(filename)
            self.models[instrument] = self.trainer
            logger.info(f"Loaded model for {instrument}")
            return True
        except Exception as e:
            logger.error(f"Error loading model for {instrument}: {str(e)}")
            return False
    
    def predict_next_day(self, data, instrument, confidence_threshold=config.PREDICTION_THRESHOLD):
        """
        Predict if next day will be bullish or bearish
        
        Args:
            data: Current features DataFrame
            instrument: Instrument name
            confidence_threshold: Minimum confidence for alert
            
        Returns:
            dict: Prediction result
        """
        try:
            if instrument not in self.models:
                logger.error(f"No model loaded for {instrument}")
                return None
            
            trainer = self.models[instrument]
            
            # Get the last row of data
            last_record = data.iloc[[-1]]
            
            # Select only feature columns
            exclude_cols = ['open', 'high', 'low', 'close', 'volume']
            feature_cols = [col for col in last_record.columns if col not in exclude_cols]
            X = last_record[feature_cols]
            
            # Scale features
            X_scaled = trainer.scaler.transform(X)
            
            # Predict
            prediction = trainer.model.predict(X_scaled)[0]
            
            # Get probability
            if hasattr(trainer.model, 'predict_proba'):
                probabilities = trainer.model.predict_proba(X_scaled)[0]
                confidence = max(probabilities)
            else:
                confidence = 0.5
            
            # Determine signal
            signal = "BULL" if prediction == 1 else "BEAR"
            alert_triggered = confidence >= confidence_threshold
            
            result = {
                'instrument': instrument,
                'signal': signal,
                'prediction': prediction,
                'confidence': float(confidence),
                'alert_triggered': alert_triggered,
                'timestamp': data.index[-1],
                'features_used': feature_cols,
            }
            
            logger.info(f"{instrument} Prediction: {signal} (Confidence: {confidence:.2%})")
            return result
            
        except Exception as e:
            logger.error(f"Error making prediction for {instrument}: {str(e)}")
            return None
    
    def predict_batch(self, data_dict, confidence_threshold=config.PREDICTION_THRESHOLD):
        """
        Make predictions for multiple instruments
        
        Args:
            data_dict: Dict of {instrument: features_dataframe}
            confidence_threshold: Minimum confidence for alert
            
        Returns:
            list: List of predictions
        """
        predictions = []
        
        for instrument, data in data_dict.items():
            result = self.predict_next_day(data, instrument, confidence_threshold)
            if result:
                predictions.append(result)
        
        return predictions
    
    def get_prediction_summary(self, predictions):
        """
        Get a summary of all predictions
        
        Args:
            predictions: List of predictions
            
        Returns:
            dict: Summary statistics
        """
        try:
            bull_signals = sum(1 for p in predictions if p['signal'] == 'BULL')
            bear_signals = sum(1 for p in predictions if p['signal'] == 'BEAR')
            alerts = sum(1 for p in predictions if p['alert_triggered'])
            avg_confidence = np.mean([p['confidence'] for p in predictions])
            
            return {
                'total_predictions': len(predictions),
                'bull_signals': bull_signals,
                'bear_signals': bear_signals,
                'triggered_alerts': alerts,
                'average_confidence': float(avg_confidence),
                'details': predictions
            }
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return None
