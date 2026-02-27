"""
Data Collection Module - Fetch historical data from yfinance
"""
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
from pathlib import Path
import config

logger = logging.getLogger(__name__)

class DataCollector:
    """Collects market data from yfinance"""
    
    def __init__(self, data_dir=config.DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
    def fetch_historical_data(self, ticker, period=config.HISTORY_PERIOD, interval=config.DATA_INTERVAL):
        """
        Fetch historical data for a ticker
        
        Args:
            ticker: yfinance ticker symbol
            period: Time period (e.g., '2y', '1y')
            interval: Candle interval (e.g., '1h', '1d')
            
        Returns:
            pd.DataFrame: Historical OHLCV data
        """
        try:
            logger.info(f"Fetching {ticker} data for period {period}...")
            data = yf.download(ticker, period=period, interval=interval, progress=False)
            
            if data.empty:
                logger.warning(f"No data fetched for {ticker}")
                return None
                
            # Ensure required columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            data = data[required_cols]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            logger.info(f"Successfully fetched {len(data)} records for {ticker}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return None
    
    def fetch_intraday_data(self, ticker, days=1):
        """
        Fetch latest 1-hour intraday data
        
        Args:
            ticker: yfinance ticker symbol
            days: Number of days of data to fetch
            
        Returns:
            pd.DataFrame: Latest 1-hour OHLCV data
        """
        try:
            logger.info(f"Fetching intraday data for {ticker}...")
            data = yf.download(ticker, period=f"{days}d", interval="1h", progress=False)
            
            if data.empty:
                logger.warning(f"No intraday data for {ticker}")
                return None
                
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            data = data[required_cols]
            data.columns = ['open', 'high', 'low', 'close', 'volume']
            
            logger.info(f"Fetched {len(data)} intraday records for {ticker}")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching intraday data for {ticker}: {str(e)}")
            return None
    
    def save_data(self, data, filename):
        """Save data to CSV"""
        try:
            filepath = self.data_dir / f"{filename}.csv"
            data.to_csv(filepath)
            logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            return None
    
    def load_data(self, filename):
        """Load data from CSV"""
        try:
            filepath = self.data_dir / f"{filename}.csv"
            data = pd.read_csv(filepath, index_col=0, parse_dates=True)
            logger.info(f"Data loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return None
    
    def get_previous_day_data(self, ticker):
        """
        Get the previous trading day's 1-hour candles
        
        Args:
            ticker: yfinance ticker symbol
            
        Returns:
            pd.DataFrame: Previous day's 1-hour data
        """
        try:
            # Fetch last 2 days to ensure we get previous complete day
            data = self.fetch_intraday_data(ticker, days=2)
            
            if data is None or len(data) < 5:
                logger.warning(f"Insufficient data for {ticker}")
                return None
            
            # Get yesterday's data (skip today's incomplete data)
            today = pd.Timestamp.now().normalize()
            yesterday_data = data[data.index.date < today.date()]
            
            logger.info(f"Retrieved {len(yesterday_data)} candles for previous day")
            return yesterday_data
            
        except Exception as e:
            logger.error(f"Error getting previous day data: {str(e)}")
            return None


class UpstoxDataCollector:
    """
    Upstox API data collector (optional)
    Requires API key from https://upstox.com/
    """
    
    def __init__(self, api_key=config.UPSTOX_API_KEY):
        self.api_key = api_key
        if self.api_key:
            logger.info("Upstox API key configured")
        else:
            logger.warning("Upstox API key not configured")
    
    def fetch_data(self, instrument_key, interval="1h", count=100):
        """
        Fetch data from Upstox API
        
        Args:
            instrument_key: Upstox instrument key (e.g., 'NSE_INDEX|Nifty 50')
            interval: Candle interval
            count: Number of candles
            
        Returns:
            pd.DataFrame: OHLCV data
        """
        if not self.api_key:
            logger.error("Upstox API key not configured")
            return None
        
        try:
            # Implementation would go here
            # This is a placeholder - Upstox SDK integration
            logger.info(f"Fetching {instrument_key} from Upstox...")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching from Upstox: {str(e)}")
            return None
