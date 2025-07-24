# Turtle Trading System

A Python implementation of the famous Turtle Trading system - a trend-following algorithmic trading strategy developed by Richard Dennis and Bill Eckhardt in the 1980s.

## 🎯 Project Status

**Current Status**: FUNCTIONAL BUT INCOMPLETE ✅

**What's Working**:
- ✅ Configuration management with YAML
- ✅ Real-time data fetching from Yahoo Finance
- ✅ Technical indicator calculations (Donchian Channels, ATR)
- ✅ Signal generation engine with proper Turtle Trading rules
- ✅ Data quality validation and SQLite storage

**What's Missing**:
- ❌ Portfolio management and position sizing
- ❌ Risk management controls
- ❌ Execution engine and backtesting
- ❌ Performance monitoring

## 🐢 About Turtle Trading

The Turtle Trading system is based on breakout strategies using Donchian Channels:

- **System 1**: 20-day breakout system (more sensitive)
- **System 2**: 55-day breakout system (less sensitive)
- **Entry**: Buy when price breaks above channel highs
- **Exit**: Sell when price breaks below channel lows
- **Risk Management**: Position sizing based on ATR (Average True Range)

## 📋 Features

### Implemented
- **Multi-timeframe support**: Daily, hourly, and intraday data
- **Multiple market support**: S&P 500, NASDAQ 100, or custom stock lists
- **Technical indicators**: Donchian Channels, ATR, Moving Averages
- **Signal generation**: Entry/exit signals for both trading systems
- **Data management**: Automatic data fetching, caching, and storage
- **Configuration**: Flexible YAML-based configuration system

### Planned
- Portfolio management with proper position sizing
- Risk management and drawdown controls
- Backtesting engine with performance metrics
- Live trading execution capabilities
- Web dashboard for monitoring

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/turtle-trading-system.git
cd turtle-trading-system

# Install dependencies
pip install pandas numpy yfinance pydantic PyYAML loguru

# Or install from requirements.txt (when available)
pip install -r requirements.txt
```

### Basic Usage

```python
from turtle_trading.core.config import Config
from turtle_trading.core.data_manager import DataManager
from turtle_trading.core.signal_engine import SignalEngine

# Load configuration
config = Config.from_yaml("config.yaml")

# Initialize components
data_manager = DataManager(config)
signal_engine = SignalEngine(config)

# Get market data
data = data_manager.get_universe_data(lookback_days=100)

# Generate trading signals
signals = signal_engine.generate_signals(data)

# Analyze signals
for symbol, symbol_signals in signals.items():
    for signal in symbol_signals:
        print(f"{symbol}: {signal.signal_type.value} at ${signal.price:.2f}")
```

### Demo

Run the demonstration script to see the system in action:

```bash
python3 demo_turtle_trading.py
```

### Testing

Test the implemented components:

```bash
python3 test_implemented.py
```

## ⚙️ Configuration

The system uses a YAML configuration file (`config.yaml`) to control all parameters:

```yaml
# Trading Rules
trading:
  system1_length: 20          # System 1 breakout length
  system2_length: 55          # System 2 breakout length
  use_system2: true           # Enable System 2
  risk_per_unit: 0.01         # 1% risk per unit
  atr_period: 20              # ATR calculation period
  stop_atr_multiple: 2.0      # Stop loss distance in ATR

# Data Configuration
data:
  provider: "yfinance"        # Data provider
  universe: "sp500"           # Stock universe
  start_date: "2020-01-01"    # Data start date
  data_frequency: "1d"        # Data frequency

# Account Settings
account:
  initial_capital: 100000     # Starting capital
  currency: "USD"             # Account currency
```

## 📊 System Architecture

```
turtle_trading/
├── core/
│   ├── config.py           # Configuration management
│   ├── data_manager.py     # Data fetching and storage
│   └── signal_engine.py    # Signal generation
├── backtesting/            # [Planned] Backtesting engine
├── optimization/           # [Planned] Parameter optimization
└── monitoring/             # [Planned] Performance monitoring
```

## 📈 Performance Characteristics

**Expected Performance** (based on historical Turtle Trading results):
- **Win Rate**: ~40% (typical for trend-following systems)
- **Signal Frequency**: 1-3 signals per stock per year
- **Best Markets**: Strong trending markets (bull or bear)
- **Risk Management**: Designed to limit losses and ride trends

## 🔧 Development

### Project Structure

- `turtle_trading/` - Main package
- `config.yaml` - Configuration file
- `demo_turtle_trading.py` - Demonstration script
- `test_implemented.py` - Test script for implemented features
- `ANALYSIS_REPORT.md` - Detailed technical analysis

### Contributing

This project is in active development. Key areas needing implementation:

1. **Priority 1**: Portfolio Manager, Risk Manager, Backtesting
2. **Priority 2**: Execution Engine, Performance Monitoring
3. **Priority 3**: Parameter Optimization, Web Interface

### Dependencies

- `pandas` - Data manipulation
- `numpy` - Numerical calculations
- `yfinance` - Market data
- `pydantic` - Configuration validation
- `PyYAML` - Configuration files
- `loguru` - Logging

## 📄 License

This project is open source. See LICENSE file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves risk and this system is not guaranteed to be profitable. Always test thoroughly before using with real money.

## 📚 References

- **Original Turtle Trading Rules**: Way of the Turtle by Curtis M. Faith
- **Market Wizards**: By Jack Schwager (interviews with Richard Dennis)
- **Donchian Channels**: Technical analysis technique used for breakouts

## 🎯 Roadmap

- [ ] Complete portfolio management implementation
- [ ] Add comprehensive backtesting capabilities
- [ ] Implement risk management controls
- [ ] Add execution engine for live trading
- [ ] Create web-based dashboard
- [ ] Add support for crypto and forex markets
- [ ] Implement machine learning enhancements

---

**Built with Python 3.8+ | Market data by Yahoo Finance | Inspired by the original Turtle Traders**
