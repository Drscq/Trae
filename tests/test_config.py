"""Unit tests for configuration module."""

import pytest
import tempfile
import yaml
from pathlib import Path

from turtle_trading.core.config import Config, TradingConfig, DataConfig


class TestConfig:
    """Test configuration loading and validation."""
    
    def test_config_from_yaml(self, sample_config):
        """Test loading configuration from YAML."""
        assert isinstance(sample_config, Config)
        assert sample_config.trading.system1_length == 20
        assert sample_config.trading.system2_length == 55
        assert sample_config.data.provider == "yfinance"
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test invalid risk values
        with pytest.raises(ValueError):
            TradingConfig(risk_per_unit=1.5)  # > 1.0
        
        with pytest.raises(ValueError):
            TradingConfig(risk_per_unit=-0.1)  # < 0
    
    def test_universe_symbols(self, sample_config):
        """Test universe symbol retrieval."""
        symbols = sample_config.get_universe_symbols()
        assert isinstance(symbols, list)
        assert len(symbols) > 0
        assert "AAPL" in symbols  # Should be in S&P 500
    
    def test_config_to_yaml(self, sample_config):
        """Test saving configuration to YAML."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            sample_config.to_yaml(temp_path)
            
            # Load it back and verify
            loaded_config = Config.from_yaml(temp_path)
            assert loaded_config.trading.system1_length == sample_config.trading.system1_length
            assert loaded_config.data.provider == sample_config.data.provider
        finally:
            Path(temp_path).unlink()
    
    def test_update_trading_params(self, sample_config):
        """Test updating trading parameters."""
        new_config = sample_config.update_trading_params(
            system1_length=30,
            risk_per_unit=0.015
        )
        
        assert new_config.trading.system1_length == 30
        assert new_config.trading.risk_per_unit == 0.015
        # Original should be unchanged
        assert sample_config.trading.system1_length == 20
