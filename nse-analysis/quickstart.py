#!/usr/bin/env python3
"""
Quick Start Example - Get started with NSE Prediction Agent
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def example_1_fetch_data():
    """Example 1: Fetch market data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Fetch Market Data")
    print("="*60)
    
    from src.data_collection.collector import DataCollector
    
    collector = DataCollector()
    
    # Fetch last 7 days of NIFTY50 data
    data = collector.fetch_historical_data(
        ticker="^NSEI",
        period="7d",
        interval="1h"
    )
    
    if data is not None:
        print(f"\nFetched {len(data)} records")
        print("\nLast 5 records:")
        print(data.tail())
        
        # Save data
        collector.save_data(data, "nifty_sample")
    else:
        print("Failed to fetch data")


def example_2_technical_analysis():
    """Example 2: Extract technical features"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Technical Analysis")
    print("="*60)
    
    from src.data_collection.collector import DataCollector
    from src.analysis.technical_analyzer import TechnicalAnalyzer
    
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    
    # Fetch data
    data = collector.fetch_historical_data("^NSEI", period="30d", interval="1h")
    
    if data is not None:
        # Analyze peaks and troughs
        print("\nAnalyzing peaks and troughs...")
        analysis = analyzer.get_peak_trough_analysis(data)
        
        print(f"Highest Price: ₹{analysis.get('highest_price', 0):.2f}")
        print(f"Lowest Price: ₹{analysis.get('lowest_price', 0):.2f}")
        print(f"Opening Price: ₹{analysis.get('opening_price', 0):.2f}")
        print(f"Closing Price: ₹{analysis.get('closing_price', 0):.2f}")
        print(f"Pattern: {analysis.get('pattern_type', 'unknown')}")
        print(f"Peaks Found: {len(analysis.get('peaks', []))}")
        print(f"Troughs Found: {len(analysis.get('troughs', []))}")
        
        # Extract all features
        print("\nExtracting technical features...")
        features = analyzer.extract_all_features(data)
        
        if features is not None:
            print(f"Features shape: {features.shape}")
            print(f"Feature columns: {list(features.columns)}")
            print("\nFirst 3 features:")
            print(features.head(3))


def example_3_train_model():
    """Example 3: Train ML model"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Train ML Model")
    print("="*60)
    
    from src.data_collection.collector import DataCollector
    from src.analysis.technical_analyzer import TechnicalAnalyzer
    from src.ml_model.trainer import MLModelTrainer
    
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    trainer = MLModelTrainer()
    
    # Fetch data
    print("Fetching historical data...")
    data = collector.fetch_historical_data("^NSEI", period="1y", interval="1h")
    
    if data is not None and len(data) > 100:
        # Extract features
        print("Extracting features...")
        features = analyzer.extract_all_features(data)
        
        if features is not None:
            # Train model
            print("Training model...")
            result = trainer.train_from_data(features, "nifty_quickstart")
            
            if result:
                print(f"\n✓ Model trained successfully!")
                print(f"Accuracy: {result['metrics']['accuracy']:.2%}")
                print(f"Precision: {result['metrics']['precision']:.2%}")
                print(f"Recall: {result['metrics']['recall']:.2%}")
                print(f"F1-Score: {result['metrics']['f1_score']:.2%}")
                print(f"\nModel saved to: {result['model_path']}")


def example_4_make_predictions():
    """Example 4: Make predictions"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Make Predictions")
    print("="*60)
    
    from src.data_collection.collector import DataCollector
    from src.analysis.technical_analyzer import TechnicalAnalyzer
    from src.ml_model.trainer import MLModelTrainer
    from src.ml_model.predictor import PredictionEngine
    
    collector = DataCollector()
    analyzer = TechnicalAnalyzer()
    predictor = PredictionEngine()
    
    # Load trained model
    print("Loading trained model...")
    if not predictor.load_model("NIFTY50", "nifty_quickstart"):
        print("Model not found. Run example 3 first to train model.")
        return
    
    # Get latest data
    print("Fetching latest data...")
    data = collector.fetch_historical_data("^NSEI", period="7d", interval="1h")
    
    if data is not None and len(data) > 10:
        # Extract features
        print("Extracting features...")
        features = analyzer.extract_all_features(data)
        
        if features is not None:
            # Make prediction
            print("Making prediction...")
            result = predictor.predict_next_day(features, "NIFTY50")
            
            if result:
                print(f"\n{'='*40}")
                print(f"Instrument: {result['instrument']}")
                print(f"Signal: {result['signal']}")
                print(f"Confidence: {result['confidence']:.1%}")
                print(f"Alert Triggered: {'Yes ⚠️' if result['alert_triggered'] else 'No'}")
                print(f"Timestamp: {result['timestamp']}")
                print(f"{'='*40}")


def example_5_full_agent():
    """Example 5: Run full agent"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Full Agent Pipeline")
    print("="*60)
    
    from agent import NSEPredictionAgent
    
    agent = NSEPredictionAgent()
    
    # Option 1: Just make predictions (requires trained model)
    print("\nRunning analysis and predictions...")
    predictions = agent.analyze_and_predict()
    
    if predictions:
        print(f"\nPrediction Summary:")
        print(f"  Total: {predictions['total_predictions']}")
        print(f"  Bull: {predictions['bull_signals']}")
        print(f"  Bear: {predictions['bear_signals']}")
        print(f"  Alerts: {predictions['triggered_alerts']}")


def main():
    """Run examples"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NSE Agent Quick Start Examples')
    parser.add_argument('example', type=int, nargs='?', default=1,
                       help='Example number (1-5, default: 1)')
    
    args = parser.parse_args()
    
    examples = {
        1: example_1_fetch_data,
        2: example_2_technical_analysis,
        3: example_3_train_model,
        4: example_4_make_predictions,
        5: example_5_full_agent,
    }
    
    if args.example in examples:
        try:
            examples[args.example]()
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Example {args.example} not found")
        print("\nAvailable examples:")
        print("  1. Fetch market data")
        print("  2. Technical analysis")
        print("  3. Train ML model")
        print("  4. Make predictions")
        print("  5. Full agent pipeline")
        print("\nUsage: python quickstart.py [1-5]")


if __name__ == "__main__":
    main()
