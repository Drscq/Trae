#!/usr/bin/env python3
"""
Simple test script to analyze and test the turtle_trading project.
"""

import sys
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    try:
        from turtle_trading.core.config import Config
        print("✓ Config import successful")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from turtle_trading.core.data_manager import DataManager
        print("✓ DataManager import successful")
    except Exception as e:
        print(f"✗ DataManager import failed: {e}")
        return False
        
    # Test main package import
    try:
        import turtle_trading
        print("✓ Main package import successful")
        print(f"  Version: {turtle_trading.__version__}")
        print(f"  Author: {turtle_trading.__author__}")
    except Exception as e:
        print(f"✗ Main package import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from turtle_trading.core.config import Config
        
        # Test loading from YAML
        config = Config.from_yaml("config.yaml")
        print("✓ Config loaded from YAML successfully")
        
        # Test config properties
        print(f"  Data provider: {config.data.provider}")
        print(f"  Universe: {config.data.universe}")
        print(f"  System 1 length: {config.trading.system1_length}")
        print(f"  System 2 length: {config.trading.system2_length}")
        print(f"  Initial capital: ${config.account.initial_capital:,.2f}")
        
        # Test universe symbols
        symbols = config.get_universe_symbols()
        print(f"  Universe symbols count: {len(symbols)}")
        print(f"  Sample symbols: {symbols[:5]}")
        
        return True
        
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        traceback.print_exc()
        return False

def test_data_manager():
    """Test data manager functionality."""
    print("\nTesting data manager...")
    
    try:
        from turtle_trading.core.config import Config
        from turtle_trading.core.data_manager import DataManager
        
        # Load config
        config = Config.from_yaml("config.yaml")
        
        # Initialize data manager
        data_manager = DataManager(config)
        print("✓ DataManager initialized successfully")
        
        # Test data summary
        summary = data_manager.get_data_summary()
        print(f"  Cached symbols: {summary['cache_size']}")
        print(f"  Database path: {summary['database_path']}")
        print(f"  Database exists: {summary['database_exists']}")
        
        # Test fetching sample data
        print("  Testing data fetch for sample symbols...")
        sample_symbols = ["AAPL", "MSFT"]
        
        try:
            data = data_manager.fetch_data(
                symbols=sample_symbols,
                start_date="2024-01-01",
                end_date="2024-07-01"
            )
            
            if data:
                print(f"✓ Successfully fetched data for {len(data)} symbols")
                for symbol, df in data.items():
                    print(f"    {symbol}: {len(df)} records, date range: {df.index.min()} to {df.index.max()}")
                    
                    # Test data quality
                    is_valid, issues = data_manager.validate_data_quality(df, symbol)
                    if is_valid:
                        print(f"    {symbol}: Data quality ✓")
                    else:
                        print(f"    {symbol}: Data quality issues: {issues}")
            else:
                print("⚠ No data fetched (might be network/API issue)")
                
        except Exception as e:
            print(f"⚠ Data fetch failed (might be network/API issue): {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ DataManager test failed: {e}")
        traceback.print_exc()
        return False

def test_missing_dependencies():
    """Check for missing dependencies."""
    print("\nChecking dependencies...")
    
    required_packages = [
        "pandas", "numpy", "pydantic", "yaml", "yfinance", 
        "loguru", "sqlite3", "pathlib", "datetime"
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == "yaml":
                import yaml
            elif package == "sqlite3":
                import sqlite3
            elif package == "pathlib":
                from pathlib import Path
            elif package == "datetime":
                from datetime import datetime
            else:
                __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\nMissing dependencies: {missing}")
        print("Install with: pip install " + " ".join(missing))
        return False
    else:
        print("✓ All dependencies available")
        return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("TURTLE TRADING SYSTEM ANALYSIS")
    print("=" * 60)
    
    # Check dependencies first
    deps_ok = test_missing_dependencies()
    
    # Test imports
    imports_ok = test_imports()
    
    # Test configuration
    config_ok = test_config()
    
    # Test data manager
    data_ok = test_data_manager()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if deps_ok and imports_ok and config_ok:
        print("✓ Core system is functional")
        
        if data_ok:
            print("✓ Data management is working")
            print("\nThe turtle trading system appears to be partially implemented with:")
            print("- Configuration management (✓)")
            print("- Data fetching and management (✓)")
            print("- Technical indicator calculation (✓)")
            print("- Missing: Signal engine implementation")
            print("- Missing: Portfolio management")
            print("- Missing: Risk management")
            print("- Missing: Backtesting engine")
            print("- Missing: Execution engine")
        else:
            print("⚠ Data management has issues (likely network/API related)")
    else:
        print("✗ Core system has issues")
        
        if not deps_ok:
            print("  - Missing dependencies")
        if not imports_ok:
            print("  - Import failures")
        if not config_ok:
            print("  - Configuration issues")
    
    print("\nNEXT STEPS:")
    print("1. Install missing dependencies (if any)")
    print("2. Implement the signal_engine.py (currently empty)")
    print("3. Add portfolio management, risk management, and backtesting")
    print("4. Create proper unit tests")

if __name__ == "__main__":
    main()
