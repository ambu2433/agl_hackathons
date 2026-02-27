"""
Technical Analysis Module - Feature extraction from price data
"""
import pandas as pd
import numpy as np
import logging
from talib import RSI, MACD, BBANDS, SMA
import warnings

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Extract technical indicators and features"""
    
    def __init__(self):
        self.features = {}
    
    def identify_candle_patterns(self, data):
        """
        Identify candlestick patterns and find peaks/troughs
        
        Args:
            data: DataFrame with open, high, low, close columns
            
        Returns:
            dict: Pattern information
        """
        patterns = {
            'peaks': [],
            'troughs': [],
            'pattern_type': 'none'
        }
        
        try:
            if len(data) < 3:
                return patterns
            
            # Find local peaks (high points)
            for i in range(1, len(data) - 1):
                if data['high'].iloc[i] > data['high'].iloc[i-1] and \
                   data['high'].iloc[i] > data['high'].iloc[i+1]:
                    patterns['peaks'].append({
                        'index': i,
                        'price': data['high'].iloc[i],
                        'time': data.index[i]
                    })
            
            # Find local troughs (low points)
            for i in range(1, len(data) - 1):
                if data['low'].iloc[i] < data['low'].iloc[i-1] and \
                   data['low'].iloc[i] < data['low'].iloc[i+1]:
                    patterns['troughs'].append({
                        'index': i,
                        'price': data['low'].iloc[i],
                        'time': data.index[i]
                    })
            
            # Identify pattern type
            if len(patterns['peaks']) > 0 and len(patterns['troughs']) > 0:
                last_peak = patterns['peaks'][-1]['price']
                last_trough = patterns['troughs'][-1]['price']
                current_close = data['close'].iloc[-1]
                
                if current_close > last_peak:
                    patterns['pattern_type'] = 'bullish_breakout'
                elif current_close < last_trough:
                    patterns['pattern_type'] = 'bearish_breakdown'
                else:
                    patterns['pattern_type'] = 'consolidation'
            
            logger.info(f"Identified {len(patterns['peaks'])} peaks and {len(patterns['troughs'])} troughs")
            return patterns
            
        except Exception as e:
            logger.error(f"Error identifying patterns: {str(e)}")
            return patterns
    
    def calculate_rsi(self, data, period=14):
        """Calculate Relative Strength Index"""
        try:
            if len(data) < period:
                return None
            rsi = RSI(data['close'].values, timeperiod=period)
            return pd.Series(rsi, index=data.index, name='rsi')
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return None
    
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
        """Calculate MACD indicator"""
        try:
            if len(data) < slow:
                return None
            macd, signal_line, histogram = MACD(
                data['close'].values,
                fastperiod=fast,
                slowperiod=slow,
                signalperiod=signal
            )
            return pd.DataFrame({
                'macd': macd,
                'signal': signal_line,
                'histogram': histogram
            }, index=data.index)
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return None
    
    def calculate_bollinger_bands(self, data, period=20, std_dev=2):
        """Calculate Bollinger Bands"""
        try:
            if len(data) < period:
                return None
            upper, middle, lower = BBANDS(
                data['close'].values,
                timeperiod=period,
                nbdevup=std_dev,
                nbdevdn=std_dev
            )
            return pd.DataFrame({
                'upper': upper,
                'middle': middle,
                'lower': lower
            }, index=data.index)
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return None
    
    def calculate_moving_averages(self, data, periods=[20, 50]):
        """Calculate Simple Moving Averages"""
        try:
            result = {}
            for period in periods:
                if len(data) < period:
                    continue
                sma = SMA(data['close'].values, timeperiod=period)
                result[f'sma_{period}'] = pd.Series(sma, index=data.index)
            return result
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            return {}
    
    def calculate_volume_ratio(self, data, period=20):
        """Calculate volume compared to average"""
        try:
            if len(data) < period:
                return None
            avg_volume = data['volume'].rolling(window=period).mean()
            volume_ratio = data['volume'] / avg_volume
            return volume_ratio
        except Exception as e:
            logger.error(f"Error calculating volume ratio: {str(e)}")
            return None
    
    def calculate_price_ratios(self, data):
        """Calculate High-Low and Close-Open ratios"""
        try:
            hl_ratio = (data['high'] - data['low']) / data['close']
            co_ratio = (data['close'] - data['open']) / data['open']
            
            return pd.DataFrame({
                'hl_ratio': hl_ratio,
                'co_ratio': co_ratio
            }, index=data.index)
        except Exception as e:
            logger.error(f"Error calculating price ratios: {str(e)}")
            return None
    
    def extract_all_features(self, data):
        """
        Extract all technical features from data
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            DataFrame: Features for ML model
        """
        try:
            features_df = data.copy()
            
            # Moving Averages
            sma_20 = self.calculate_moving_averages(data, [20]).get('sma_20')
            if sma_20 is not None:
                features_df['sma_20'] = sma_20
            
            sma_50 = self.calculate_moving_averages(data, [50]).get('sma_50')
            if sma_50 is not None:
                features_df['sma_50'] = sma_50
            
            # RSI
            rsi = self.calculate_rsi(data)
            if rsi is not None:
                features_df['rsi'] = rsi
            
            # MACD
            macd_data = self.calculate_macd(data)
            if macd_data is not None:
                features_df['macd'] = macd_data['macd']
                features_df['macd_signal'] = macd_data['signal']
                features_df['macd_hist'] = macd_data['histogram']
            
            # Bollinger Bands
            bb_data = self.calculate_bollinger_bands(data)
            if bb_data is not None:
                features_df['bb_upper'] = bb_data['upper']
                features_df['bb_middle'] = bb_data['middle']
                features_df['bb_lower'] = bb_data['lower']
                
                # Bollinger Band position
                features_df['bb_position'] = (
                    (data['close'] - bb_data['lower']) / 
                    (bb_data['upper'] - bb_data['lower'])
                )
            
            # Volume
            volume_ratio = self.calculate_volume_ratio(data)
            if volume_ratio is not None:
                features_df['volume_ratio'] = volume_ratio
            
            # Price Ratios
            price_ratios = self.calculate_price_ratios(data)
            if price_ratios is not None:
                features_df['hl_ratio'] = price_ratios['hl_ratio']
                features_df['co_ratio'] = price_ratios['co_ratio']
            
            # Drop NaN values
            features_df = features_df.dropna()
            
            logger.info(f"Extracted features for {len(features_df)} records")
            return features_df
            
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return None
    
    def get_peak_trough_analysis(self, data):
        """
        Analyze peaks and troughs for previous day
        
        Returns:
            dict: Analysis results
        """
        analysis = self.identify_candle_patterns(data)
        
        if len(data) > 0:
            analysis['highest_price'] = data['high'].max()
            analysis['lowest_price'] = data['low'].min()
            analysis['opening_price'] = data['open'].iloc[0]
            analysis['closing_price'] = data['close'].iloc[-1]
            analysis['avg_price'] = data['close'].mean()
            
            # Calculate resistance and support
            if len(analysis['peaks']) >= 2:
                analysis['resistance'] = analysis['peaks'][-1]['price']
            if len(analysis['troughs']) >= 2:
                analysis['support'] = analysis['troughs'][-1]['price']
        
        return analysis
