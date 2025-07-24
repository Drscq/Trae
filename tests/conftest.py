"""Test configuration for Turtle Trading System."""

import pytest
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture
def sample_config():
    """Sample configuration for testing."""
    from turtle_trading.core.config import Config
    return Config.from_yaml(project_root / "config.yaml")

@pytest.fixture
def sample_data():
    """Sample market data for testing."""
    import pandas as pd
    import numpy as np
    
    # Create sample OHLCV data
    dates = pd.date_range(start='2024-01-01', end='2024-06-30', freq='D')
    n_days = len(dates)
    
    # Generate realistic price data
    np.random.seed(42)
    base_price = 100
    returns = np.random.normal(0.001, 0.02, n_days)
    prices = base_price * (1 + returns).cumprod()
    
    data = pd.DataFrame({
        'open': prices * (1 + np.random.normal(0, 0.005, n_days)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, n_days))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, n_days))),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, n_days),
        'adj_close': prices,
    }, index=dates)
    
    # Ensure OHLC relationships are correct
    data['high'] = data[['open', 'high', 'close']].max(axis=1)
    data['low'] = data[['open', 'low', 'close']].min(axis=1)
    
    return data
