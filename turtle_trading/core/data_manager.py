"""Data management for Turtle Trading System."""

import pandas as pd
import numpy as np
import yfinance as yf
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from loguru import logger

from .config import Config


class DataManager:
    """Manages data ingestion, storage, and retrieval."""
    
    def __init__(self, config: Config):
        self.config = config
        self.data_cache: Dict[str, pd.DataFrame] = {}
        self.db_path = Path("data/market_data.db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize SQLite database for data storage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_data (
                symbol TEXT,
                date DATE,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                adj_close REAL,
                PRIMARY KEY (symbol, date)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS corporate_actions (
                symbol TEXT,
                date DATE,
                action_type TEXT,
                ratio REAL,
                PRIMARY KEY (symbol, date, action_type)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def fetch_data(self, symbols: List[str], start_date: str, end_date: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """Fetch market data for given symbols."""
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        data = {}
        
        for symbol in symbols:
            try:
                # Check cache first
                if symbol in self.data_cache:
                    cached_data = self.data_cache[symbol]
                    if (cached_data.index.min() <= pd.to_datetime(start_date) and 
                        cached_data.index.max() >= pd.to_datetime(end_date)):
                        filtered_data = cached_data.loc[start_date:end_date].copy()
                        # Ensure technical indicators are present
                        if 'donchian_high_20' not in filtered_data.columns:
                            filtered_data = self.calculate_technical_indicators(filtered_data)
                        data[symbol] = filtered_data
                        continue
                
                # Fetch from provider
                if self.config.data.provider == "yfinance":
                    df = self._fetch_yfinance_data(symbol, start_date, end_date)
                else:
                    raise ValueError(f"Unsupported data provider: {self.config.data.provider}")
                
                if df is not None and not df.empty:
                    # Normalize data
                    df = self._normalize_data(df, symbol)
                    
                    # Calculate technical indicators
                    df = self.calculate_technical_indicators(df)
                    
                    data[symbol] = df
                    self.data_cache[symbol] = df
                    
                    # Store in database
                    self._store_data(symbol, df)
                    
                    logger.info(f"Fetched {len(df)} records for {symbol}")
                else:
                    logger.warning(f"No data available for {symbol}")
                    
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
                continue
        
        return data
    
    def _fetch_yfinance_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Fetch data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date, auto_adjust=False)
            
            if df.empty:
                return None
            
            # Standardize column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            df.index.name = 'date'
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            return None
    
    def _normalize_data(self, df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Normalize data for splits and dividends."""
        df = df.copy()
        
        # Calculate adjustment factor from adj_close
        if 'adj_close' in df.columns:
            adj_factor = df['adj_close'] / df['close']
            
            # Apply adjustment to OHLC
            df['open'] = df['open'] * adj_factor
            df['high'] = df['high'] * adj_factor
            df['low'] = df['low'] * adj_factor
            df['close'] = df['adj_close']
            
            # Adjust volume (inverse of price adjustment)
            df['volume'] = df['volume'] / adj_factor
        
        # Remove any rows with missing data
        df = df.dropna()
        
        # Ensure positive prices
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df.columns:
                df = df[df[col] > 0]
        
        return df
    
    def _store_data(self, symbol: str, df: pd.DataFrame) -> None:
        """Store data in SQLite database."""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Prepare data for insertion
            df_to_store = df.copy()
            df_to_store['symbol'] = symbol
            df_to_store = df_to_store.reset_index()
            
            # Insert or replace data
            df_to_store.to_sql('price_data', conn, if_exists='replace', index=False)
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error storing data for {symbol}: {e}")
    
    def get_latest_data(self, symbols: List[str], lookback_days: int = 100) -> Dict[str, pd.DataFrame]:
        """Get latest data for symbols with specified lookback."""
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=lookback_days)).strftime('%Y-%m-%d')
        
        return self.fetch_data(symbols, start_date, end_date)
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for the data."""
        df = df.copy()
        
        # Donchian Channels
        for period in [10, 20, 55]:
            df[f'donchian_high_{period}'] = df['high'].rolling(window=period).max()
            df[f'donchian_low_{period}'] = df['low'].rolling(window=period).min()
        
        # Average True Range (ATR)
        df['prev_close'] = df['close'].shift(1)
        df['tr1'] = df['high'] - df['low']
        df['tr2'] = abs(df['high'] - df['prev_close'])
        df['tr3'] = abs(df['low'] - df['prev_close'])
        df['true_range'] = df[['tr1', 'tr2', 'tr3']].max(axis=1)
        
        for period in [10, 20, 30]:
            df[f'atr_{period}'] = df['true_range'].rolling(window=period).mean()
        
        # Simple Moving Averages
        for period in [10, 20, 50, 200]:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
        
        # Volatility measures
        df['returns'] = df['close'].pct_change()
        for period in [10, 20, 30]:
            df[f'volatility_{period}'] = df['returns'].rolling(window=period).std() * np.sqrt(252)
        
        # Clean up temporary columns
        temp_cols = ['prev_close', 'tr1', 'tr2', 'tr3']
        df = df.drop(columns=[col for col in temp_cols if col in df.columns])
        
        return df
    
    def get_universe_data(self, lookback_days: int = 100) -> Dict[str, pd.DataFrame]:
        """Get data for the entire configured universe."""
        symbols = self.config.get_universe_symbols()
        data = self.get_latest_data(symbols, lookback_days)
        
        # Calculate technical indicators for all symbols
        for symbol in data:
            data[symbol] = self.calculate_technical_indicators(data[symbol])
        
        return data
    
    def validate_data_quality(self, df: pd.DataFrame, symbol: str) -> Tuple[bool, List[str]]:
        """Validate data quality and return issues found."""
        issues = []
        
        # Check for missing data
        if df.isnull().any().any():
            issues.append("Missing data found")
        
        # Check for negative prices
        price_cols = ['open', 'high', 'low', 'close']
        for col in price_cols:
            if col in df.columns and (df[col] <= 0).any():
                issues.append(f"Negative or zero prices in {col}")
        
        # Check for invalid OHLC relationships
        if 'high' in df.columns and 'low' in df.columns:
            if (df['high'] < df['low']).any():
                issues.append("High < Low found")
        
        # Check for extreme price movements (>50% in one day)
        if 'close' in df.columns:
            daily_returns = df['close'].pct_change().abs()
            if (daily_returns > 0.5).any():
                issues.append("Extreme price movements detected")
        
        # Check for sufficient data
        if len(df) < 60:  # Need at least 60 days for 55-day breakout
            issues.append("Insufficient data for analysis")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def get_benchmark_data(self, start_date: str, end_date: Optional[str] = None) -> pd.DataFrame:
        """Get benchmark data for performance comparison."""
        benchmark_symbol = self.config.backtest.benchmark
        data = self.fetch_data([benchmark_symbol], start_date, end_date)
        
        if benchmark_symbol in data:
            return self.calculate_technical_indicators(data[benchmark_symbol])
        else:
            raise ValueError(f"Could not fetch benchmark data for {benchmark_symbol}")
    
    def clear_cache(self) -> None:
        """Clear the data cache."""
        self.data_cache.clear()
        logger.info("Data cache cleared")
    
    def get_data_summary(self) -> Dict[str, any]:
        """Get summary of available data."""
        summary = {
            "cached_symbols": list(self.data_cache.keys()),
            "cache_size": len(self.data_cache),
            "database_path": str(self.db_path),
            "database_exists": self.db_path.exists()
        }
        
        # Get database statistics
        if self.db_path.exists():
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute("SELECT COUNT(DISTINCT symbol) FROM price_data")
                summary["db_symbols_count"] = cursor.fetchone()[0]
                
                cursor.execute("SELECT MIN(date), MAX(date) FROM price_data")
                date_range = cursor.fetchone()
                summary["db_date_range"] = date_range
                
                conn.close()
                
            except Exception as e:
                logger.error(f"Error getting database summary: {e}")
                summary["db_error"] = str(e)
        
        return summary