# Development Guide

This guide provides instructions for setting up the development environment and contributing to the Turtle Trading System.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Environment Setup

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/turtle-trading-system.git
cd turtle-trading-system
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt

# For development (includes testing tools)
pip install -e ".[dev]"
```

4. **Verify installation**:
```bash
python -m pytest tests/
python examples/demo_turtle_trading.py
```

## Project Architecture

### Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Configurability**: All parameters controlled via YAML configuration
3. **Extensibility**: Easy to add new features and data sources
4. **Testability**: Comprehensive unit and integration tests
5. **Performance**: Efficient data handling and caching

### Key Components

#### 1. Configuration System (`core/config.py`)
- **Purpose**: Centralized configuration management
- **Features**: YAML-based, validated with Pydantic
- **Extensibility**: Easy to add new configuration sections

#### 2. Data Management (`core/data_manager.py`)
- **Purpose**: Market data fetching, storage, and processing
- **Features**: Multiple data providers, SQLite caching, technical indicators
- **Extensibility**: Plugin architecture for new data sources

#### 3. Signal Engine (`core/signal_engine.py`)
- **Purpose**: Trading signal generation
- **Features**: Turtle Trading rules, multiple timeframes
- **Extensibility**: Easy to add new trading strategies

## Development Workflow

### 1. Feature Development

1. **Create feature branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Implement feature**:
   - Add code in appropriate module
   - Follow existing code style
   - Add comprehensive docstrings
   - Include type hints

3. **Add tests**:
```bash
# Add unit tests
touch tests/test_your_feature.py

# Run tests
python -m pytest tests/test_your_feature.py -v
```

4. **Update documentation**:
   - Add docstrings to new functions/classes
   - Update README.md if needed
   - Add example usage

### 2. Testing

#### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_config.py -v

# Run with coverage
python -m pytest --cov=turtle_trading tests/

# Run integration tests
python tests/test_implemented.py
```

#### Test Structure
- **Unit Tests**: Test individual functions/classes
- **Integration Tests**: Test component interactions
- **End-to-End Tests**: Test complete workflows

#### Adding New Tests
```python
import pytest
from turtle_trading.core.your_module import YourClass

class TestYourClass:
    def test_basic_functionality(self, sample_config):
        # Test implementation
        instance = YourClass(sample_config)
        result = instance.your_method()
        assert result is not None
```

### 3. Code Style

#### Python Standards
- **PEP 8**: Follow Python style guidelines
- **Type Hints**: Use type annotations
- **Docstrings**: Google-style docstrings
- **Error Handling**: Proper exception handling

#### Example Code Style
```python
"""Module docstring describing the module purpose."""

from typing import Dict, List, Optional
import pandas as pd

class ExampleClass:
    """Class docstring describing the class purpose.
    
    Args:
        config: Configuration object
        data: Market data dictionary
    """
    
    def __init__(self, config: Config, data: Dict[str, pd.DataFrame]) -> None:
        self.config = config
        self.data = data
    
    def process_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Process data for a specific symbol.
        
        Args:
            symbol: Stock symbol to process
            
        Returns:
            Processed DataFrame or None if no data
            
        Raises:
            ValueError: If symbol is invalid
        """
        if symbol not in self.data:
            raise ValueError(f"Symbol {symbol} not found in data")
        
        return self.data[symbol].copy()
```

## Contributing Guidelines

### 1. Code Requirements

- **Functionality**: Code must work correctly
- **Tests**: Minimum 80% test coverage for new code
- **Documentation**: All public methods must have docstrings
- **Style**: Follow project coding standards

### 2. Pull Request Process

1. **Before submitting**:
   - Run all tests: `python -m pytest`
   - Check code style: `flake8 turtle_trading/`
   - Update documentation

2. **Pull request**:
   - Clear description of changes
   - Reference any related issues
   - Include test results

3. **Review process**:
   - Code review by maintainers
   - Address feedback
   - Merge when approved

### 3. Issue Reporting

When reporting bugs or requesting features:

1. **Search existing issues** first
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Code examples

## Priority Development Areas

### Phase 1: Core Trading System
1. **Portfolio Manager**: Position sizing and management
2. **Risk Manager**: Risk controls and limits
3. **Backtesting Engine**: Historical performance testing

### Phase 2: Advanced Features
1. **Execution Engine**: Order management and execution
2. **Performance Monitor**: Real-time monitoring
3. **Parameter Optimization**: Automated parameter tuning

### Phase 3: Infrastructure
1. **Web Interface**: Dashboard and controls
2. **API Layer**: REST API for external access
3. **Deployment**: Production deployment tools

## Getting Help

### Resources
- **Documentation**: Check `docs/` directory
- **Examples**: See `examples/` for usage patterns
- **Tests**: Look at test files for usage examples

### Communication
- **Issues**: Use GitHub issues for bugs and features
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact maintainers for private matters

## Best Practices

### Performance
- **Vectorization**: Use pandas/numpy operations when possible
- **Caching**: Cache expensive computations
- **Memory Management**: Be mindful of large datasets

### Security
- **No hardcoded secrets**: Use environment variables
- **Input validation**: Validate all external inputs
- **Error handling**: Don't expose internal details

### Maintainability
- **Simple functions**: Keep functions focused and small
- **Clear naming**: Use descriptive variable/function names
- **Consistent patterns**: Follow established patterns in codebase

---

Happy coding! 🐢📈
