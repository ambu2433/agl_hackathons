"""
ML Model Training Module - Train and manage prediction models
"""
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
from pathlib import Path
import config

logger = logging.getLogger(__name__)

class MLModelTrainer:
    """Train and manage ML models for prediction"""
    
    def __init__(self, model_type=config.MODEL_TYPE, models_dir=config.MODELS_DIR):
        self.model_type = model_type
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
        self.model = None
        self.scaler = None
        self.feature_columns = None
    
    def create_labels(self, data):
        """
        Create labels for training (Bull=1, Bear=0)
        
        Bull: Close next day > Close current day
        Bear: Close next day <= Close current day
        """
        try:
            labels = []
            for i in range(len(data) - 1):
                if data['close'].iloc[i + 1] > data['close'].iloc[i]:
                    labels.append(1)  # Bull
                else:
                    labels.append(0)  # Bear
            
            # Remove last row since it doesn't have a label
            return np.array(labels)
        except Exception as e:
            logger.error(f"Error creating labels: {str(e)}")
            return None
    
    def prepare_data(self, data, test_size=config.TRAIN_TEST_SPLIT):
        """
        Prepare data for model training
        
        Args:
            data: DataFrame with features
            test_size: Train/test split ratio
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        try:
            # Drop OHLCV columns, keep only features
            exclude_cols = ['open', 'high', 'low', 'close', 'volume']
            feature_cols = [col for col in data.columns if col not in exclude_cols]
            
            self.feature_columns = feature_cols
            X = data[feature_cols].dropna()
            
            # Create labels for the data
            y = self.create_labels(data)
            
            # Match X and y lengths
            if len(X) > len(y):
                X = X[:-1]
            
            if len(y) > len(X):
                y = y[:len(X)]
            
            logger.info(f"Data shape: {X.shape}, Labels: {y.shape}")
            
            # Normalize features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y,
                test_size=1 - test_size,
                random_state=42,
                stratify=y
            )
            
            logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
            return X_train, X_test, y_train, y_test
            
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            return None, None, None, None
    
    def create_model(self):
        """Create model based on config"""
        try:
            if self.model_type == "xgboost":
                self.model = XGBClassifier(
                    n_estimators=100,
                    max_depth=5,
                    learning_rate=0.1,
                    random_state=42,
                    eval_metric='logloss',
                    verbosity=0
                )
                logger.info("Created XGBoost model")
                
            elif self.model_type == "random_forest":
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    min_samples_split=5,
                    random_state=42,
                    n_jobs=-1
                )
                logger.info("Created Random Forest model")
                
            elif self.model_type == "svm":
                self.model = SVC(
                    kernel='rbf',
                    C=1.0,
                    probability=True,
                    random_state=42
                )
                logger.info("Created SVM model")
            else:
                logger.error(f"Unknown model type: {self.model_type}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error creating model: {str(e)}")
            return False
    
    def train(self, X_train, y_train):
        """Train the model"""
        try:
            logger.info("Starting model training...")
            self.model.fit(X_train, y_train)
            logger.info("Model training completed")
            return True
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        try:
            y_pred = self.model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            metrics = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
            }
            
            logger.info(f"Model Metrics - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            return None
    
    def save_model(self, filename):
        """Save trained model and scaler"""
        try:
            model_path = self.models_dir / f"{filename}_model.pkl"
            scaler_path = self.models_dir / f"{filename}_scaler.pkl"
            
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)
            
            # Save feature columns
            features_path = self.models_dir / f"{filename}_features.txt"
            with open(features_path, 'w') as f:
                f.write('\n'.join(self.feature_columns))
            
            logger.info(f"Model saved to {model_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def load_model(self, filename):
        """Load trained model and scaler"""
        try:
            model_path = self.models_dir / f"{filename}_model.pkl"
            scaler_path = self.models_dir / f"{filename}_scaler.pkl"
            features_path = self.models_dir / f"{filename}_features.txt"
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            
            with open(features_path, 'r') as f:
                self.feature_columns = f.read().strip().split('\n')
            
            logger.info(f"Model loaded from {model_path}")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def train_from_data(self, data, filename):
        """
        Complete training pipeline
        
        Args:
            data: DataFrame with features
            filename: Name to save model
            
        Returns:
            dict: Training results and metrics
        """
        try:
            # Prepare data
            X_train, X_test, y_train, y_test = self.prepare_data(data)
            if X_train is None:
                return None
            
            # Create model
            if not self.create_model():
                return None
            
            # Train
            if not self.train(X_train, y_train):
                return None
            
            # Evaluate
            metrics = self.evaluate(X_test, y_test)
            if metrics is None:
                return None
            
            # Save
            if not self.save_model(filename):
                return None
            
            return {
                'status': 'success',
                'metrics': metrics,
                'model_path': str(self.models_dir / f"{filename}_model.pkl")
            }
            
        except Exception as e:
            logger.error(f"Error in training pipeline: {str(e)}")
            return None
