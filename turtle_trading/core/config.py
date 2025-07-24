"""Configuration management for Turtle Trading System."""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


class DataConfig(BaseModel):
    """Data configuration settings."""
    provider: str = "yfinance"
    universe: str = "sp500"
    custom_symbols: List[str] = []
    start_date: str = "2020-01-01"
    end_date: Optional[str] = None
    data_frequency: str = "1d"


class TradingConfig(BaseModel):
    """Trading rules configuration."""
    system1_length: int = 20
    system2_length: int = 55
    use_system2: bool = True
    risk_per_unit: float = 0.01
    max_risk_per_position: float = 0.02
    max_units_per_position: int = 5
    pyramid_increment: float = 0.5
    atr_period: int = 20
    stop_atr_multiple: float = 2.0
    exit_length_s1: int = 10
    exit_length_s2: int = 20
    max_position_time: int = 252
    order_type: str = "market"
    slippage_bps: float = 5.0
    commission_per_share: float = 0.005

    @validator('risk_per_unit', 'max_risk_per_position')
    def validate_risk(cls, v):
        if not 0 < v <= 1:
            raise ValueError('Risk values must be between 0 and 1')
        return v


class AccountConfig(BaseModel):
    """Account configuration."""
    initial_capital: float = 100000
    currency: str = "USD"


class BacktestConfig(BaseModel):
    """Backtesting configuration."""
    start_date: str = "2010-01-01"
    end_date: str = "2023-12-31"
    benchmark: str = "SPY"


class OptimizationConfig(BaseModel):
    """Optimization configuration."""
    enabled: bool = True
    frequency: str = "monthly"
    param_ranges: Dict[str, List[float]] = {
        "system1_length": [10, 30],
        "system2_length": [40, 80],
        "atr_period": [10, 30],
        "stop_atr_multiple": [1.5, 3.0],
        "risk_per_unit": [0.005, 0.02]
    }
    objective: str = "sharpe_ratio"
    min_trades: int = 50
    max_drawdown_threshold: float = 0.25
    min_sharpe: float = 1.0


class EmailConfig(BaseModel):
    """Email notification configuration."""
    enabled: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    username: str = ""
    password: str = ""
    recipients: List[str] = []


class SlackConfig(BaseModel):
    """Slack notification configuration."""
    enabled: bool = False
    webhook_url: str = ""
    channel: str = "#trading"


class NotificationConfig(BaseModel):
    """Notification configuration."""
    email: EmailConfig = EmailConfig()
    slack: SlackConfig = SlackConfig()


class MonitoringConfig(BaseModel):
    """Monitoring configuration."""
    max_drawdown_alert: float = 0.15
    daily_loss_alert: float = 0.05
    position_size_alert: float = 0.10


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = "INFO"
    file: str = "logs/turtle_trading.log"
    max_size: str = "10MB"
    backup_count: int = 5


class Config(BaseModel):
    """Main configuration class."""
    data: DataConfig = DataConfig()
    trading: TradingConfig = TradingConfig()
    account: AccountConfig = AccountConfig()
    backtest: BacktestConfig = BacktestConfig()
    optimization: OptimizationConfig = OptimizationConfig()
    notifications: NotificationConfig = NotificationConfig()
    monitoring: MonitoringConfig = MonitoringConfig()
    logging: LoggingConfig = LoggingConfig()

    @classmethod
    def from_yaml(cls, config_path: str) -> 'Config':
        """Load configuration from YAML file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return cls(**config_data)
    
    def to_yaml(self, config_path: str) -> None:
        """Save configuration to YAML file."""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            yaml.dump(self.dict(), f, default_flow_style=False, indent=2)
    
    def update_trading_params(self, **kwargs) -> 'Config':
        """Update trading parameters and return new config."""
        trading_dict = self.trading.dict()
        trading_dict.update(kwargs)
        
        new_config = self.copy(deep=True)
        new_config.trading = TradingConfig(**trading_dict)
        return new_config
    
    def get_universe_symbols(self) -> List[str]:
        """Get list of symbols based on universe configuration."""
        if self.data.universe == "custom":
            return self.data.custom_symbols
        elif self.data.universe == "sp500":
            return self._get_sp500_symbols()
        elif self.data.universe == "nasdaq100":
            return self._get_nasdaq100_symbols()
        elif self.data.universe == "all_us":
            return self._get_all_us_symbols()
        else:
            raise ValueError(f"Unknown universe: {self.data.universe}")
    
    def _get_sp500_symbols(self) -> List[str]:
        """Get S&P 500 symbols."""
        # This would typically fetch from a data provider
        # For now, return a sample list
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK-B",
            "UNH", "JNJ", "V", "PG", "JPM", "HD", "CVX", "MA", "PFE", "ABBV",
            "BAC", "KO", "AVGO", "PEP", "TMO", "COST", "WMT", "DIS", "ABT",
            "DHR", "VZ", "ADBE", "NFLX", "CRM", "XOM", "NKE", "CMCSA", "ACN",
            "TXN", "QCOM", "NEE", "LIN", "PM", "HON", "UPS", "T", "LOW", "SPGI",
            "IBM", "INTU", "GS", "CAT", "AMD", "AMGN", "ISRG", "RTX", "BKNG"
        ]
    
    def _get_nasdaq100_symbols(self) -> List[str]:
        """Get NASDAQ 100 symbols."""
        # Sample NASDAQ 100 symbols
        return [
            "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "TSLA", "META", "NVDA",
            "AVGO", "PEP", "COST", "ADBE", "NFLX", "CMCSA", "TXN", "QCOM",
            "HON", "INTU", "AMD", "AMGN", "ISRG", "BKNG", "GILD", "MDLZ",
            "ADP", "VRTX", "SBUX", "FISV", "CSX", "REGN", "ATVI", "PYPL"
        ]
    
    def _get_all_us_symbols(self) -> List[str]:
        """Get all US symbols (would need external data source)."""
        # This would require a comprehensive data source
        # For demo purposes, return extended list
        return self._get_sp500_symbols() + self._get_nasdaq100_symbols()