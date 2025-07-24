"""Signal generation engine for Turtle Trading System."""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, NamedTuple
from enum import Enum
from loguru import logger

from .config import Config


class SignalType(Enum):
    """Signal types."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    PYRAMID = "PYRAMID"
    EXIT = "EXIT"


class Signal(NamedTuple):
    """Trading signal."""
    symbol: str
    signal_type: SignalType
    timestamp: pd.Timestamp
    price: float
    system: int  # 1 or 2
    confidence: float = 1.0
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    units: int = 1


class SignalEngine:
    """Generates trading signals based on Turtle Trading rules."""
    
    def __init__(self, config: Config):
        self.config = config
        self.last_signals: Dict[str, List[Signal]] = {}
    
    def generate_signals(self, data: Dict[str, pd.DataFrame]) -> Dict[str, List[Signal]]:
        """Generate signals for all symbols in the data."""
        all_signals = {}
        
        for symbol, df in data.items():
            try:
                signals = self._generate_symbol_signals(symbol, df)
                if signals:
                    all_signals[symbol] = signals
                    self.last_signals[symbol] = signals
                    
            except Exception as e:
                logger.error(f"Error generating signals for {symbol}: {e}")
                continue
        
        return all_signals
    
    def _generate_symbol_signals(self, symbol: str, df: pd.DataFrame) -> List[Signal]:
        """Generate signals for a single symbol."""
        if len(df) < max(self.config.trading.system1_length, self.config.trading.system2_length):
            return []
        
        signals = []
        latest_row = df.iloc[-1]
        latest_date = latest_row.name
        
        # System 1 signals (20-day breakout)
        system1_signals = self._check_system1_signals(symbol, df, latest_row, latest_date)
        signals.extend(system1_signals)
        
        # System 2 signals (55-day breakout) if enabled
        if self.config.trading.use_system2:
            system2_signals = self._check_system2_signals(symbol, df, latest_row, latest_date)
            signals.extend(system2_signals)
        
        return signals
    
    def _check_system1_signals(self, symbol: str, df: pd.DataFrame, latest_row: pd.Series, latest_date: pd.Timestamp) -> List[Signal]:
        """Check for System 1 (20-day) signals."""
        signals = []
        length = self.config.trading.system1_length
        
        # Get required data
        if f'donchian_high_{length}' not in df.columns:
            return signals
        
        current_price = latest_row['close']
        donchian_high = latest_row[f'donchian_high_{length}']
        donchian_low = latest_row[f'donchian_low_{length}']
        atr = latest_row.get(f'atr_{self.config.trading.atr_period}', 0)
        
        # Entry signals - breakout above high
        if current_price > donchian_high and not pd.isna(donchian_high):
            stop_price = current_price - (self.config.trading.stop_atr_multiple * atr)
            
            signal = Signal(
                symbol=symbol,
                signal_type=SignalType.BUY,
                timestamp=latest_date,
                price=current_price,
                system=1,
                confidence=1.0,
                stop_price=stop_price
            )
            signals.append(signal)
            logger.info(f"System 1 BUY signal for {symbol} at {current_price}")
        
        # Exit signals - breakout below low
        exit_length = self.config.trading.exit_length_s1
        if f'donchian_low_{exit_length}' in df.columns:
            exit_low = latest_row[f'donchian_low_{exit_length}']
            
            if current_price < exit_low and not pd.isna(exit_low):
                signal = Signal(
                    symbol=symbol,
                    signal_type=SignalType.EXIT,
                    timestamp=latest_date,
                    price=current_price,
                    system=1,
                    confidence=1.0
                )
                signals.append(signal)
                logger.info(f"System 1 EXIT signal for {symbol} at {current_price}")
        
        return signals
    
    def _check_system2_signals(self, symbol: str, df: pd.DataFrame, latest_row: pd.Series, latest_date: pd.Timestamp) -> List[Signal]:
        """Check for System 2 (55-day) signals."""
        signals = []
        length = self.config.trading.system2_length
        
        # Get required data
        if f'donchian_high_{length}' not in df.columns:
            return signals
        
        current_price = latest_row['close']
        donchian_high = latest_row[f'donchian_high_{length}']
        donchian_low = latest_row[f'donchian_low_{length}']
        atr = latest_row.get(f'atr_{self.config.trading.atr_period}', 0)
        
        # Entry signals - breakout above high
        if current_price > donchian_high and not pd.isna(donchian_high):
            stop_price = current_price - (self.config.trading.stop_atr_multiple * atr)
            
            signal = Signal(
                symbol=symbol,
                signal_type=SignalType.BUY,
                timestamp=latest_date,
                price=current_price,
                system=2,
                confidence=1.0,
                stop_price=stop_price
            )
            signals.append(signal)
            logger.info(f"System 2 BUY signal for {symbol} at {current_price}")
        
        # Exit signals - breakout below low
        exit_length = self.config.trading.exit_length_s2
        if f'donchian_low_{exit_length}' in df.columns:
            exit_low = latest_row[f'donchian_low_{exit_length}']
            
            if current_price < exit_low and not pd.isna(exit_low):
                signal = Signal(
                    symbol=symbol,
                    signal_type=SignalType.EXIT,
                    timestamp=latest_date,
                    price=current_price,
                    system=2,
                    confidence=1.0
                )
                signals.append(signal)
                logger.info(f"System 2 EXIT signal for {symbol} at {current_price}")
        
        return signals
    
    def check_pyramid_signals(self, symbol: str, df: pd.DataFrame, current_position_price: float, current_units: int) -> Optional[Signal]:
        """Check for pyramid (add to position) signals."""
        if current_units >= self.config.trading.max_units_per_position:
            return None
        
        latest_row = df.iloc[-1]
        current_price = latest_row['close']
        atr = latest_row.get(f'atr_{self.config.trading.atr_period}', 0)
        
        # Pyramid condition: price moved favorably by ATR increment
        pyramid_threshold = current_position_price + (self.config.trading.pyramid_increment * atr * current_units)
        
        if current_price > pyramid_threshold:
            stop_price = current_price - (self.config.trading.stop_atr_multiple * atr)
            
            return Signal(
                symbol=symbol,
                signal_type=SignalType.PYRAMID,
                timestamp=latest_row.name,
                price=current_price,
                system=1,  # Default to system 1
                confidence=1.0,
                stop_price=stop_price,
                units=1
            )
        
        return None
    
    def get_stop_loss_price(self, symbol: str, df: pd.DataFrame, entry_price: float) -> float:
        """Calculate stop loss price based on ATR."""
        latest_row = df.iloc[-1]
        atr = latest_row.get(f'atr_{self.config.trading.atr_period}', 0)
        
        return entry_price - (self.config.trading.stop_atr_multiple * atr)
    
    def get_signal_summary(self) -> Dict[str, any]:
        """Get summary of recent signals."""
        summary = {
            "total_symbols": len(self.last_signals),
            "signals_by_type": {},
            "signals_by_system": {}
        }
        
        all_signals = []
        for signals in self.last_signals.values():
            all_signals.extend(signals)
        
        # Count by signal type
        for signal_type in SignalType:
            count = len([s for s in all_signals if s.signal_type == signal_type])
            if count > 0:
                summary["signals_by_type"][signal_type.value] = count
        
        # Count by system
        for system in [1, 2]:
            count = len([s for s in all_signals if s.system == system])
            if count > 0:
                summary["signals_by_system"][f"system_{system}"] = count
        
        return summary