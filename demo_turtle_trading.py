#!/usr/bin/env python3
"""
Demonstration script for the Turtle Trading System.
This script shows the system in action with real market data.
"""

import sys
from pathlib import Path
import pandas as pd

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from turtle_trading.core.config import Config
from turtle_trading.core.data_manager import DataManager
from turtle_trading.core.signal_engine import SignalEngine, SignalType

def analyze_signals_for_symbol(symbol: str, data_manager: DataManager, signal_engine: SignalEngine):
    """Analyze signals for a specific symbol."""
    print(f"\n=== ANALYZING {symbol} ===")
    
    try:
        # Get more data for better signal analysis
        data = data_manager.fetch_data(
            symbols=[symbol],
            start_date="2023-01-01",
            end_date="2024-07-01"
        )
        
        if symbol not in data:
            print(f"No data available for {symbol}")
            return
        
        df = data[symbol]
        print(f"Data period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
        print(f"Total records: {len(df)}")
        
        # Check recent price action
        recent_data = df.tail(20)
        current_price = df.iloc[-1]['close']
        
        # Get Donchian levels
        donchian_high_20 = df.iloc[-1]['donchian_high_20']
        donchian_low_20 = df.iloc[-1]['donchian_low_20']
        donchian_high_55 = df.iloc[-1]['donchian_high_55']
        donchian_low_55 = df.iloc[-1]['donchian_low_55']
        atr = df.iloc[-1]['atr_20']
        
        print(f"\nCurrent Price: ${current_price:.2f}")
        print(f"20-day High:   ${donchian_high_20:.2f} ({((current_price/donchian_high_20-1)*100):+.1f}%)")
        print(f"20-day Low:    ${donchian_low_20:.2f} ({((current_price/donchian_low_20-1)*100):+.1f}%)")
        print(f"55-day High:   ${donchian_high_55:.2f} ({((current_price/donchian_high_55-1)*100):+.1f}%)")
        print(f"55-day Low:    ${donchian_low_55:.2f} ({((current_price/donchian_low_55-1)*100):+.1f}%)")
        print(f"ATR (20-day):  ${atr:.2f}")
        
        # Generate signals
        signals = signal_engine.generate_signals({symbol: df})
        
        if symbol in signals and signals[symbol]:
            print(f"\n🚨 ACTIVE SIGNALS:")
            for signal in signals[symbol]:
                print(f"  {signal.signal_type.value} - System {signal.system}")
                print(f"    Price: ${signal.price:.2f}")
                if signal.stop_price:
                    print(f"    Stop Loss: ${signal.stop_price:.2f}")
                print(f"    Confidence: {signal.confidence}")
        else:
            print(f"\n📊 No signals - analyzing breakout potential...")
            
            # Check how close we are to breakouts
            pct_to_high_20 = ((donchian_high_20 / current_price) - 1) * 100
            pct_to_high_55 = ((donchian_high_55 / current_price) - 1) * 100
            
            print(f"  Distance to 20-day breakout: {pct_to_high_20:.1f}%")
            print(f"  Distance to 55-day breakout: {pct_to_high_55:.1f}%")
            
            if pct_to_high_20 < 2:
                print(f"  ⚠️  Close to 20-day breakout!")
            if pct_to_high_55 < 2:
                print(f"  ⚠️  Close to 55-day breakout!")
        
        # Show recent volatility
        recent_volatility = df['volatility_20'].iloc[-1]
        print(f"\nRecent volatility (20-day): {recent_volatility:.1f}%")
        
        # Show trend information
        sma_20 = df.iloc[-1]['sma_20']
        sma_50 = df.iloc[-1]['sma_50']
        print(f"20-day SMA: ${sma_20:.2f}")
        print(f"50-day SMA: ${sma_50:.2f}")
        
        if current_price > sma_20 > sma_50:
            print("📈 Uptrend: Price > 20-day SMA > 50-day SMA")
        elif current_price < sma_20 < sma_50:
            print("📉 Downtrend: Price < 20-day SMA < 50-day SMA")
        else:
            print("🔄 Mixed trend")
            
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")

def scan_for_signals(data_manager: DataManager, signal_engine: SignalEngine, symbols: list):
    """Scan multiple symbols for active signals."""
    print("\n" + "="*60)
    print("SCANNING FOR ACTIVE SIGNALS")
    print("="*60)
    
    active_signals = {}
    
    for symbol in symbols:
        try:
            data = data_manager.fetch_data(
                symbols=[symbol],
                start_date="2023-01-01",
                end_date="2024-07-01"
            )
            
            if symbol in data:
                signals = signal_engine.generate_signals({symbol: data[symbol]})
                if symbol in signals and signals[symbol]:
                    active_signals[symbol] = signals[symbol]
                    
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")
            continue
    
    if active_signals:
        print("🚨 ACTIVE SIGNALS FOUND:")
        for symbol, signals in active_signals.items():
            print(f"\n{symbol}:")
            for signal in signals:
                print(f"  {signal.signal_type.value} - System {signal.system} at ${signal.price:.2f}")
    else:
        print("📊 No active signals found in the scanned symbols")
        print("This is normal - Turtle Trading generates signals infrequently")

def main():
    """Main demonstration function."""
    print("=" * 60)
    print("TURTLE TRADING SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    try:
        # Load configuration
        config = Config.from_yaml("config.yaml")
        print(f"✓ Configuration loaded")
        print(f"  System 1 length: {config.trading.system1_length} days")
        print(f"  System 2 length: {config.trading.system2_length} days")
        print(f"  Risk per unit: {config.trading.risk_per_unit*100:.1f}%")
        print(f"  Stop ATR multiple: {config.trading.stop_atr_multiple}")
        
        # Initialize components
        data_manager = DataManager(config)
        signal_engine = SignalEngine(config)
        print(f"✓ Components initialized")
        
        # Analyze specific high-profile stocks
        symbols_to_analyze = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"]
        
        for symbol in symbols_to_analyze:
            analyze_signals_for_symbol(symbol, data_manager, signal_engine)
        
        # Scan a broader set of symbols for signals
        scan_symbols = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX",
            "AMD", "CRM", "PYPL", "ZOOM", "SQ", "SHOP", "ROKU", "PELOTON"
        ]
        scan_for_signals(data_manager, signal_engine, scan_symbols)
        
        print("\n" + "="*60)
        print("SYSTEM STATUS SUMMARY")
        print("="*60)
        
        summary = data_manager.get_data_summary()
        print(f"Cached symbols: {summary['cache_size']}")
        
        signal_summary = signal_engine.get_signal_summary()
        print(f"Signals generated: {signal_summary}")
        
        print("\n📋 TURTLE TRADING RULES SUMMARY:")
        print("- BUY when price breaks above 20-day (System 1) or 55-day (System 2) high")
        print("- SELL when price breaks below 10-day (System 1) or 20-day (System 2) low")
        print("- Position size based on ATR and account risk")
        print("- Stop loss at 2x ATR below entry price")
        print("- Add to winning positions (pyramid) at 0.5x ATR increments")
        
        print("\n🎯 This system works best in trending markets")
        print("📈 Signals are infrequent but aim for large trend-following gains")
        
    except Exception as e:
        print(f"Error in demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
