"""Unit tests for signal engine module."""

import pytest
import pandas as pd
import numpy as np

from turtle_trading.core.signal_engine import SignalEngine, SignalType, Signal
from turtle_trading.core.data_manager import DataManager


class TestSignalEngine:
    """Test signal generation functionality."""
    
    def test_signal_engine_init(self, sample_config):
        """Test signal engine initialization."""
        engine = SignalEngine(sample_config)
        assert engine.config == sample_config
        assert isinstance(engine.last_signals, dict)
    
    def test_generate_signals_with_sample_data(self, sample_config, sample_data):
        """Test signal generation with sample data."""
        # Add technical indicators to sample data
        data_manager = DataManager(sample_config)
        sample_data_with_indicators = data_manager.calculate_technical_indicators(sample_data)
        
        engine = SignalEngine(sample_config)
        signals = engine.generate_signals({"TEST": sample_data_with_indicators})
        
        assert isinstance(signals, dict)
        # Signals may or may not be generated depending on data
        if "TEST" in signals:
            assert isinstance(signals["TEST"], list)
            for signal in signals["TEST"]:
                assert isinstance(signal, Signal)
                assert signal.symbol == "TEST"
                assert signal.signal_type in SignalType
    
    def test_system1_breakout_signal(self, sample_config, sample_data):
        """Test System 1 breakout signal generation."""
        data_manager = DataManager(sample_config)
        df = data_manager.calculate_technical_indicators(sample_data)
        
        # Manually create a breakout condition
        df.iloc[-1, df.columns.get_loc('close')] = df['donchian_high_20'].iloc[-1] + 1
        
        engine = SignalEngine(sample_config)
        signals = engine._generate_symbol_signals("TEST", df)
        
        # Should generate a buy signal
        buy_signals = [s for s in signals if s.signal_type == SignalType.BUY]
        assert len(buy_signals) > 0
        assert buy_signals[0].system == 1
    
    def test_pyramid_signal(self, sample_config, sample_data):
        """Test pyramid signal generation."""
        data_manager = DataManager(sample_config)
        df = data_manager.calculate_technical_indicators(sample_data)
        
        engine = SignalEngine(sample_config)
        
        # Test pyramid signal
        current_position_price = 100.0
        current_units = 1
        
        pyramid_signal = engine.check_pyramid_signals("TEST", df, current_position_price, current_units)
        
        # May or may not generate pyramid signal depending on price movement
        if pyramid_signal:
            assert pyramid_signal.signal_type == SignalType.PYRAMID
            assert pyramid_signal.units == 1
    
    def test_stop_loss_calculation(self, sample_config, sample_data):
        """Test stop loss price calculation."""
        data_manager = DataManager(sample_config)
        df = data_manager.calculate_technical_indicators(sample_data)
        
        engine = SignalEngine(sample_config)
        entry_price = 100.0
        
        stop_price = engine.get_stop_loss_price("TEST", df, entry_price)
        
        assert isinstance(stop_price, (int, float))
        assert stop_price < entry_price  # Stop should be below entry for long position
    
    def test_signal_summary(self, sample_config):
        """Test signal summary generation."""
        engine = SignalEngine(sample_config)
        
        # Add some mock signals
        mock_signals = [
            Signal("TEST1", SignalType.BUY, pd.Timestamp.now(), 100.0, 1),
            Signal("TEST2", SignalType.SELL, pd.Timestamp.now(), 90.0, 2),
        ]
        engine.last_signals = {"TEST1": [mock_signals[0]], "TEST2": [mock_signals[1]]}
        
        summary = engine.get_signal_summary()
        
        assert isinstance(summary, dict)
        assert "total_symbols" in summary
        assert "signals_by_type" in summary
        assert summary["total_symbols"] == 2
