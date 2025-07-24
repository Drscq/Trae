"""Turtle Trading System - Automated Trading with Continuous Improvement"""

__version__ = "1.0.0"
__author__ = "Turtle Trading System"

# Import only the implemented modules
from .core.config import Config
from .core.data_manager import DataManager
from .core.signal_engine import SignalEngine

__all__ = [
    "Config",
    "DataManager",
    "SignalEngine",
]

# TODO: Add these imports when modules are implemented
# from .core.portfolio_manager import PortfolioManager
# from .core.execution_engine import ExecutionEngine
# from .core.risk_manager import RiskManager
# from .backtesting.backtest_engine import BacktestEngine
# from .optimization.optimizer import ParameterOptimizer
# from .monitoring.performance_monitor import PerformanceMonitor