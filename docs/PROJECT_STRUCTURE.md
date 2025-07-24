# Project Structure

This document describes the organization and structure of the Turtle Trading System project.

## Directory Structure

```
turtle-trading-system/
├── README.md                      # Project overview and quick start
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history and changes
├── MANIFEST.in                    # Package manifest for distribution
├── setup.py                       # Python package setup configuration
├── requirements.txt               # Python dependencies
├── config.yaml                    # Default system configuration
├── .gitignore                     # Git ignore patterns
│
├── docs/                          # Documentation
│   ├── ANALYSIS_REPORT.md         # Detailed technical analysis
│   └── api/                       # API documentation (future)
│
├── examples/                      # Example scripts and tutorials
│   ├── demo_turtle_trading.py     # Main demonstration script
│   └── basic_usage.py             # Basic usage examples (future)
│
├── scripts/                       # Utility scripts
│   ├── setup_environment.py       # Environment setup (future)
│   └── data_downloader.py         # Bulk data download (future)
│
├── tests/                         # Test suite
│   ├── __init__.py                # Test package
│   ├── conftest.py                # Test configuration and fixtures
│   ├── test_config.py             # Configuration tests
│   ├── test_signal_engine.py      # Signal engine tests
│   ├── test_implemented.py        # Integration tests for implemented features
│   └── test_turtle_trading.py     # Legacy comprehensive test
│
├── turtle_trading/                # Main package
│   ├── __init__.py                # Package initialization
│   │
│   ├── core/                      # Core trading components
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── data_manager.py        # Data fetching and storage
│   │   └── signal_engine.py       # Signal generation
│   │
│   ├── backtesting/               # Backtesting framework (planned)
│   │   ├── __init__.py
│   │   ├── backtest_engine.py     # Main backtesting engine (future)
│   │   ├── performance.py         # Performance calculations (future)
│   │   └── results.py             # Results analysis (future)
│   │
│   ├── optimization/              # Parameter optimization (planned)
│   │   ├── __init__.py
│   │   ├── optimizer.py           # Parameter optimization (future)
│   │   ├── genetic.py             # Genetic algorithm (future)
│   │   └── grid_search.py         # Grid search optimization (future)
│   │
│   ├── monitoring/                # Performance monitoring (planned)
│   │   ├── __init__.py
│   │   ├── performance_monitor.py # Real-time monitoring (future)
│   │   ├── risk_monitor.py        # Risk monitoring (future)
│   │   └── alerts.py              # Alert system (future)
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── math_utils.py          # Mathematical utilities (future)
│       ├── date_utils.py          # Date/time utilities (future)
│       └── validation.py          # Data validation (future)
│
└── data/                          # Data storage (created at runtime)
    ├── market_data.db             # SQLite database for market data
    └── logs/                      # Log files
```

## Key Files and Their Purpose

### Root Level Files

- **README.md**: Main project documentation with installation and usage instructions
- **setup.py**: Python package configuration for pip installation
- **requirements.txt**: Python dependencies list
- **config.yaml**: Default configuration with trading parameters
- **LICENSE**: MIT license for open source distribution
- **CHANGELOG.md**: Version history and release notes

### Core Package (`turtle_trading/`)

#### `core/` - Implemented Core Components
- **config.py**: Configuration management with YAML support and validation
- **data_manager.py**: Market data fetching, storage, and technical indicator calculation
- **signal_engine.py**: Trading signal generation based on Turtle Trading rules

#### `backtesting/` - Planned Backtesting Framework
- Future implementation of historical performance testing
- Performance metric calculations
- Results analysis and reporting

#### `optimization/` - Planned Optimization Tools
- Parameter optimization algorithms
- Genetic algorithm implementation
- Grid search functionality

#### `monitoring/` - Planned Monitoring System
- Real-time performance monitoring
- Risk management alerts
- System health monitoring

#### `utils/` - Planned Utility Functions
- Mathematical calculations
- Date/time handling
- Data validation helpers

### Testing (`tests/`)

- **conftest.py**: Pytest configuration and shared fixtures
- **test_config.py**: Unit tests for configuration module
- **test_signal_engine.py**: Unit tests for signal generation
- **test_implemented.py**: Integration tests for working features
- **test_turtle_trading.py**: Legacy comprehensive system test

### Examples (`examples/`)

- **demo_turtle_trading.py**: Full system demonstration with real market data
- Future: Additional tutorial and example scripts

### Documentation (`docs/`)

- **ANALYSIS_REPORT.md**: Comprehensive technical analysis and assessment
- Future: API documentation, user guides, and tutorials

## Module Dependencies

```
Config ← DataManager ← SignalEngine
  ↓         ↓           ↓
  └── BacktestEngine ←──┘
          ↓
    PerformanceMonitor
```

## Configuration Flow

1. `config.yaml` → `Config` class validation
2. `Config` → `DataManager` initialization
3. `Config` → `SignalEngine` initialization
4. Components work together through well-defined interfaces

## Data Flow

1. **Data Ingestion**: Yahoo Finance → DataManager → SQLite Database
2. **Processing**: Raw Data → Technical Indicators → Signal Engine
3. **Signal Generation**: Market Data → Trading Signals → Portfolio Manager (future)
4. **Execution**: Signals → Execution Engine (future) → Broker API (future)

## Development Workflow

1. **Feature Development**: Implement in appropriate module
2. **Testing**: Add unit tests in `tests/` directory
3. **Documentation**: Update relevant documentation
4. **Integration**: Test with existing components
5. **Example**: Add usage example if significant feature

## Future Expansion

The structure is designed to accommodate:
- Additional data providers
- Multiple trading strategies
- Different asset classes (crypto, forex)
- Real-time trading capabilities
- Web interface components
- Advanced analytics and reporting

## Code Style and Standards

- **Type Hints**: All functions use Python type hints
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Proper exception handling
- **Logging**: Structured logging with loguru
- **Configuration**: YAML-based configuration
- **Testing**: Unit tests with pytest
