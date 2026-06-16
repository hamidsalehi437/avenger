"""
QUANT MATRIX CONSOLE V14 - Core Analytical Engine
Real-time financial market analysis with 21 technical indicators
"""

import MetaTrader5 as mt5
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantMatrixEngine:
    """Core engine for all technical indicator calculations"""
    
    def __init__(self, account, password, server):
        self.account = account
        self.password = password
        self.server = server
        self.connected = False
        self.init_mt5()
    
    def init_mt5(self):
        """Initialize MT5 connection"""
        try:
            if mt5.initialize(login=self.account, password=self.password, server=self.server):
                self.connected = True
                logger.info(f"✓ MT5 Connected: {self.account}")
                return True
            else:
                logger.error(f"✗ MT5 Init Failed: {mt5.last_error()}")
                return False
        except Exception as e:
            logger.error(f"✗ Connection Error: {str(e)}")
            return False
    
    def get_account_info(self):
        """Fetch live account equity, balance, and spread"""
        try:
            account_info = mt5.account_info()
            if account_info is None:
                return {"equity": "N/A", "balance": "N/A", "spread": "N/A"}
            
            return {
                "equity": f"${account_info.equity:,.2f}",
                "balance": f"${account_info.balance:,.2f}",
                "spread": f"{account_info.spread} pts"
            }
        except Exception as e:
            logger.error(f"Account info error: {e}")
            return {"equity": "N/A", "balance": "N/A", "spread": "N/A"}
    
    def get_ohlcv(self, symbol, timeframe, bars=500):
        """Fetch OHLCV data from MT5"""
        try:
            tf_map = {
                "M1": mt5.TIMEFRAME_M1,
                "M5": mt5.TIMEFRAME_M5,
                "M15": mt5.TIMEFRAME_M15,
                "M30": mt5.TIMEFRAME_M30,
                "H1": mt5.TIMEFRAME_H1,
                "H4": mt5.TIMEFRAME_H4,
                "D1": mt5.TIMEFRAME_D1,
                "W1": mt5.TIMEFRAME_W1
            }
            
            rates = mt5.copy_rates_from_pos(symbol, tf_map[timeframe], 0, bars)
            if rates is None or len(rates) == 0:
                logger.warning(f"No data for {symbol} {timeframe}")
                return None
            
            df = pd.DataFrame(rates)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            return df
        except Exception as e:
            logger.error(f"OHLCV fetch error: {e}")
            return None
    
    # ==================== VOLUME INDICATORS ====================
    
    def calculate_vwap(self, df):
        """Volume Weighted Average Price"""
        try:
            df['TP'] = (df['high'] + df['low'] + df['close']) / 3
            df['VTP'] = df['TP'] * df['tick_volume']
            df['VWAP'] = df['VTP'].rolling(window=20).sum() / df['tick_volume'].rolling(window=20).sum()
            return str(round(df['VWAP'].iloc[-1], 4))
        except:
            return "N/A"
    
    def calculate_obv(self, df):
        """On-Balance Volume"""
        try:
            df['OBV'] = 0.0
            obv = 0
            for i in range(len(df)):
                if df['close'].iloc[i] > df['close'].iloc[i-1]:
                    obv += df['tick_volume'].iloc[i]
                elif df['close'].iloc[i] < df['close'].iloc[i-1]:
                    obv -= df['tick_volume'].iloc[i]
                df.loc[i, 'OBV'] = obv
            return str(int(df['OBV'].iloc[-1]))
        except:
            return "N/A"
    
    def calculate_mfi(self, df, period=14):
        """Money Flow Index"""
        try:
            df['TP'] = (df['high'] + df['low'] + df['close']) / 3
            df['MF'] = df['TP'] * df['tick_volume']
            
            positive_mf = 0
            negative_mf = 0
            
            for i in range(1, len(df)):
                if df['TP'].iloc[i] > df['TP'].iloc[i-1]:
                    positive_mf += df['MF'].iloc[i]
                else:
                    negative_mf += df['MF'].iloc[i]
            
            mfi_ratio = positive_mf / negative_mf if negative_mf != 0 else 0
            mfi = 100 - (100 / (1 + mfi_ratio))
            return str(round(mfi, 2))
        except:
            return "N/A"
    
    def calculate_volume_profile(self, df, bins=20):
        """Volume Profile - Price levels with highest volume"""
        try:
            price_range = df['high'].max() - df['low'].min()
            bin_size = price_range / bins
            profile = {}
            
            for price, vol in zip(df['close'], df['tick_volume']):
                bin_level = round((price - df['low'].min()) / bin_size) * bin_size + df['low'].min()
                profile[bin_level] = profile.get(bin_level, 0) + vol
            
            poc = max(profile, key=profile.get)
            return str(round(poc, 4))
        except:
            return "N/A"
    
    # ==================== TREND INDICATORS ====================
    
    def calculate_sma(self, df, period=20):
        """Simple Moving Average"""
        try:
            sma = df['close'].rolling(window=period).mean()
            return str(round(sma.iloc[-1], 4))
        except:
            return "N/A"
    
    def calculate_ema(self, df, period=20):
        """Exponential Moving Average"""
        try:
            ema = df['close'].ewm(span=period, adjust=False).mean()
            return str(round(ema.iloc[-1], 4))
        except:
            return "N/A"
    
    def calculate_ichimoku(self, df):
        """Ichimoku Cloud - Returns Tenkan, Kijun, Signal"""
        try:
            # Tenkan-sen (Conversion Line)
            high_9 = df['high'].rolling(window=9).max()
            low_9 = df['low'].rolling(window=9).min()
            tenkan = (high_9 + low_9) / 2
            
            # Kijun-sen (Base Line)
            high_26 = df['high'].rolling(window=26).max()
            low_26 = df['low'].rolling(window=26).min()
            kijun = (high_26 + low_26) / 2
            
            # Senkou Span A
            senkou_a = ((tenkan + kijun) / 2).iloc[-1]
            
            return {
                "tenkan": str(round(tenkan.iloc[-1], 4)),
                "kijun": str(round(kijun.iloc[-1], 4)),
                "signal": str(round(senkou_a, 4))
            }
        except:
            return {"tenkan": "N/A", "kijun": "N/A", "signal": "N/A"}
    
    def calculate_supertrend(self, df, period=10, multiplier=3):
        """Supertrend Indicator"""
        try:
            hl2 = (df['high'] + df['low']) / 2
            atr = self.calculate_atr_value(df, period)
            
            basic_ub = hl2 + multiplier * atr
            basic_lb = hl2 - multiplier * atr
            
            final_ub = basic_ub.copy()
            final_lb = basic_lb.copy()
            
            for i in range(1, len(df)):
                final_ub.iloc[i] = min(basic_ub.iloc[i], final_ub.iloc[i-1]) if df['close'].iloc[i-1] > final_ub.iloc[i-1] else basic_ub.iloc[i]
                final_lb.iloc[i] = max(basic_lb.iloc[i], final_lb.iloc[i-1]) if df['close'].iloc[i-1] < final_lb.iloc[i-1] else basic_lb.iloc[i]
            
            signal = "SELL" if df['close'].iloc[-1] < final_ub.iloc[-1] else "BUY"
            level = str(round(final_ub.iloc[-1] if signal == "SELL" else final_lb.iloc[-1], 4))
            
            return {"signal": signal, "level": level}
        except:
            return {"signal": "N/A", "level": "N/A"}
    
    # ==================== VOLATILITY INDICATORS ====================
    
    def calculate_atr(self, df, period=14):
        """Average True Range - returned as string"""
        try:
            atr_value = self.calculate_atr_value(df, period)
            return str(round(atr_value.iloc[-1], 4))
        except:
            return "N/A"
    
    def calculate_atr_value(self, df, period=14):
        """ATR as numeric for other calculations"""
        try:
            high_low = df['high'] - df['low']
            high_close = abs(df['high'] - df['close'].shift())
            low_close = abs(df['low'] - df['close'].shift())
            
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.rolling(period).mean()
            return atr
        except:
            return pd.Series([0] * len(df))
    
    def calculate_bollinger_bands(self, df, period=20, std_dev=2):
        """Bollinger Bands with Upper, Middle, Lower"""
        try:
            sma = df['close'].rolling(window=period).mean()
            std = df['close'].rolling(window=period).std()
            
            upper = sma + (std_dev * std)
            lower = sma - (std_dev * std)
            
            return {
                "upper": str(round(upper.iloc[-1], 4)),
                "middle": str(round(sma.iloc[-1], 4)),
                "lower": str(round(lower.iloc[-1], 4))
            }
        except:
            return {"upper": "N/A", "middle": "N/A", "lower": "N/A"}
    
    def calculate_fibonacci(self, df):
        """Fibonacci Retracement Levels"""
        try:
            high = df['high'].max()
            low = df['low'].min()
            diff = high - low
            
            levels = {
                "0.0": str(round(high, 4)),
                "23.6": str(round(high - diff * 0.236, 4)),
                "38.2": str(round(high - diff * 0.382, 4)),
                "50.0": str(round(high - diff * 0.5, 4)),
                "61.8": str(round(high - diff * 0.618, 4)),
                "100.0": str(round(low, 4))
            }
            return levels
        except:
            return {"0.0": "N/A", "23.6": "N/A", "38.2": "N/A", "50.0": "N/A", "61.8": "N/A", "100.0": "N/A"}
    
    # ==================== MOMENTUM INDICATORS ====================
    
    def calculate_rsi(self, df, period=14):
        """Relative Strength Index"""
        try:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss if loss.iloc[-1] != 0 else 0
            rsi = 100 - (100 / (1 + rs))
            return str(round(rsi.iloc[-1], 2))
        except:
            return "N/A"
    
    def calculate_macd(self, df, fast=12, slow=26, signal=9):
        """MACD with Signal and Histogram"""
        try:
            ema_fast = df['close'].ewm(span=fast).mean()
            ema_slow = df['close'].ewm(span=slow).mean()
            macd = ema_fast - ema_slow
            signal_line = macd.ewm(span=signal).mean()
            histogram = macd - signal_line
            
            return {
                "macd": str(round(macd.iloc[-1], 4)),
                "signal": str(round(signal_line.iloc[-1], 4)),
                "histogram": str(round(histogram.iloc[-1], 4))
            }
        except:
            return {"macd": "N/A", "signal": "N/A", "histogram": "N/A"}
    
    def calculate_stochastic(self, df, period=14, smooth_k=3, smooth_d=3):
        """Stochastic Oscillator"""
        try:
            low_min = df['low'].rolling(window=period).min()
            high_max = df['high'].rolling(window=period).max()
            
            k_percent = 100 * (df['close'] - low_min) / (high_max - low_min)
            k_smooth = k_percent.rolling(window=smooth_k).mean()
            d_smooth = k_smooth.rolling(window=smooth_d).mean()
            
            return {
                "k": str(round(k_smooth.iloc[-1], 2)),
                "d": str(round(d_smooth.iloc[-1], 2))
            }
        except:
            return {"k": "N/A", "d": "N/A"}
    
    def calculate_cci(self, df, period=20):
        """Commodity Channel Index"""
        try:
            tp = (df['high'] + df['low'] + df['close']) / 3
            sma_tp = tp.rolling(window=period).mean()
            mad = tp.rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))
            
            cci = (tp - sma_tp) / (0.015 * mad)
            return str(round(cci.iloc[-1], 2))
        except:
            return "N/A"
    
    def calculate_adx(self, df, period=14):
        """Average Directional Index"""
        try:
            high_diff = df['high'].diff()
            low_diff = -df['low'].diff()
            
            plus_dm = pd.Series(0.0, index=df.index)
            minus_dm = pd.Series(0.0, index=df.index)
            
            plus_dm = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0)
            minus_dm = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0)
            
            tr = self.calculate_atr_value(df, 1).rolling(window=period).sum()
            plus_di = 100 * (pd.Series(plus_dm).rolling(window=period).sum() / tr)
            minus_di = 100 * (pd.Series(minus_dm).rolling(window=period).sum() / tr)
            
            dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
            adx = dx.rolling(window=period).mean()
            
            return str(round(adx.iloc[-1], 2))
        except:
            return "N/A"
    
    def calculate_chaikin(self, df, period=20):
        """Chaikin Money Flow"""
        try:
            mfv = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low']) * df['tick_volume']
            cmf = mfv.rolling(window=period).sum() / df['tick_volume'].rolling(window=period).sum()
            return str(round(cmf.iloc[-1], 4))
        except:
            return "N/A"
    
    def calculate_parabolic_sar(self, df, af_start=0.02, af_max=0.2):
        """Parabolic SAR"""
        try:
            sar = df['close'].copy()
            af = af_start
            
            for i in range(2, len(df)):
                if i % 2 == 0:
                    sar.iloc[i] = sar.iloc[i-1] + af * (df['high'].iloc[:i].max() - sar.iloc[i-1])
                    af = min(af + af_start, af_max)
                else:
                    sar.iloc[i] = sar.iloc[i-1] + af * (df['low'].iloc[:i].min() - sar.iloc[i-1])
            
            return str(round(sar.iloc[-1], 4))
        except:
            return "N/A"
    
    def calculate_pivot_points(self, df):
        """Pivot Points - Standard"""
        try:
            h = df['high'].iloc[-1]
            l = df['low'].iloc[-1]
            c = df['close'].iloc[-1]
            
            pivot = (h + l + c) / 3
            r1 = (2 * pivot) - l
            s1 = (2 * pivot) - h
            r2 = pivot + (h - l)
            s2 = pivot - (h - l)
            
            return {
                "r2": str(round(r2, 4)),
                "r1": str(round(r1, 4)),
                "pivot": str(round(pivot, 4)),
                "s1": str(round(s1, 4)),
                "s2": str(round(s2, 4))
            }
        except:
            return {"r2": "N/A", "r1": "N/A", "pivot": "N/A", "s1": "N/A", "s2": "N/A"}
    
    # ==================== SMART MONEY CONCEPTS ====================
    
    def calculate_smc(self, df):
        """Smart Money Concepts - Structure Analysis"""
        try:
            # Order Block, Breaker Block, Change of Character (ChoCh), Break of Structure (BOS)
            recent_high = df['high'].iloc[-5:].max()
            recent_low = df['low'].iloc[-5:].min()
            current_price = df['close'].iloc[-1]
            
            # Detect structure
            if current_price > recent_high:
                structure = "HH"  # Higher High
                signal = "BUY"
            elif current_price < recent_low:
                structure = "LL"  # Lower Low
                signal = "SELL"
            elif current_price > df['high'].iloc[-10:-5].max():
                structure = "BOS"  # Break of Structure
                signal = "BUY"
            elif current_price < df['low'].iloc[-10:-5].min():
                structure = "BOS"
                signal = "SELL"
            else:
                structure = "CONSOLIDATION"
                signal = "NEUTRAL"
            
            return {
                "structure": structure,
                "signal": signal,
                "level": str(round(current_price, 4))
            }
        except:
            return {"structure": "N/A", "signal": "N/A", "level": "N/A"}
    
    # ==================== MULTI-TIMEFRAME SIGNAL GENERATION ====================
    
    def generate_scalping_signal(self, symbol, entry_price_str):
        """Generate scalping signal (M5 timeframe)"""
        try:
            df = self.get_ohlcv(symbol, "M5", 100)
            if df is None:
                return self._blank_signal()
            
            entry = float(entry_price_str)
            atr = float(self.calculate_atr(df, 14)) if self.calculate_atr(df, 14) != "N/A" else 0.01
            
            return {
                "timeframe": "Scalping (M5)",
                "entry": str(round(entry, 4)),
                "sl": str(round(entry - (atr * 1.5), 4)),
                "tp1": str(round(entry + (atr * 0.5), 4)),
                "tp2": str(round(entry + (atr * 1.0), 4)),
                "tp3": str(round(entry + (atr * 1.5), 4)),
                "risk_reward": "1:1.5",
                "signal": "BUY" if float(self.calculate_rsi(df)) < 70 else "SELL" if float(self.calculate_rsi(df)) > 30 else "NEUTRAL"
            }
        except:
            return self._blank_signal()
    
    def generate_swing_signal(self, symbol, entry_price_str):
        """Generate swing trading signal (H4 timeframe)"""
        try:
            df = self.get_ohlcv(symbol, "H4", 100)
            if df is None:
                return self._blank_signal()
            
            entry = float(entry_price_str)
            atr = float(self.calculate_atr(df, 14)) if self.calculate_atr(df, 14) != "N/A" else 0.01
            
            return {
                "timeframe": "Swing (H4)",
                "entry": str(round(entry, 4)),
                "sl": str(round(entry - (atr * 2), 4)),
                "tp1": str(round(entry + (atr * 1), 4)),
                "tp2": str(round(entry + (atr * 2), 4)),
                "tp3": str(round(entry + (atr * 3), 4)),
                "risk_reward": "1:2.5",
                "signal": self.calculate_smc(df)["signal"]
            }
        except:
            return self._blank_signal()
    
    def generate_longterm_signal(self, symbol, entry_price_str):
        """Generate long-term signal (D1 timeframe)"""
        try:
            df = self.get_ohlcv(symbol, "D1", 100)
            if df is None:
                return self._blank_signal()
            
            entry = float(entry_price_str)
            atr = float(self.calculate_atr(df, 14)) if self.calculate_atr(df, 14) != "N/A" else 0.01
            
            return {
                "timeframe": "Long-term (D1)",
                "entry": str(round(entry, 4)),
                "sl": str(round(entry - (atr * 3), 4)),
                "tp1": str(round(entry + (atr * 2), 4)),
                "tp2": str(round(entry + (atr * 4), 4)),
                "tp3": str(round(entry + (atr * 6), 4)),
                "risk_reward": "1:4",
                "signal": self.calculate_ichimoku(df)["signal"]
            }
        except:
            return self._blank_signal()
    
    @staticmethod
    def _blank_signal():
        """Return blank signal template"""
        return {
            "timeframe": "N/A",
            "entry": "N/A",
            "sl": "N/A",
            "tp1": "N/A",
            "tp2": "N/A",
            "tp3": "N/A",
            "risk_reward": "N/A",
            "signal": "N/A"
        }
    
    # ==================== CONFIDENCE SCORING ====================
    
    def calculate_confluence_score(self, df):
        """Calculate System Confidence based on indicator agreement"""
        try:
            score = 0
            weight = 0
            
            # SMC (weight: 25%)
            try:
                smc_signal = self.calculate_smc(df)["signal"]
                if smc_signal in ["BUY", "SELL"]:
                    score += 25
                    weight += 25
            except:
                pass
            
            # VWAP (weight: 20%)
            try:
                vwap = float(self.calculate_vwap(df))
                if vwap > df['close'].iloc[-1]:
                    score += 10
                elif vwap < df['close'].iloc[-1]:
                    score += 10
                weight += 20
            except:
                pass
            
            # Bollinger Bands (weight: 15%)
            try:
                bb = self.calculate_bollinger_bands(df)
                bb_upper = float(bb["upper"])
                bb_lower = float(bb["lower"])
                if df['close'].iloc[-1] > bb_upper:
                    score += 10
                elif df['close'].iloc[-1] < bb_lower:
                    score += 10
                weight += 15
            except:
                pass
            
            # MACD (weight: 15%)
            try:
                macd_val = self.calculate_macd(df)
                macd = float(macd_val["macd"])
                signal = float(macd_val["signal"])
                if macd > signal:
                    score += 7
                elif macd < signal:
                    score += 7
                weight += 15
            except:
                pass
            
            # RSI (weight: 10%)
            try:
                rsi = float(self.calculate_rsi(df))
                if 40 < rsi < 60:
                    score += 5
                weight += 10
            except:
                pass
            
            # Supertrend (weight: 15%)
            try:
                st = self.calculate_supertrend(df)
                if st["signal"] in ["BUY", "SELL"]:
                    score += 8
                weight += 15
            except:
                pass
            
            if weight == 0:
                return "50%"
            
            confidence = (score / weight) * 100
            
            if confidence >= 75:
                bias = "STRONG BUY"
            elif confidence >= 60:
                bias = "BUY"
            elif confidence >= 40:
                bias = "NEUTRAL"
            elif confidence >= 25:
                bias = "SELL"
            else:
                bias = "STRONG SELL"
            
            return f"{confidence:.0f}% {bias}"
        except:
            return "N/A"
    
    def shutdown(self):
        """Close MT5 connection"""
        if self.connected:
            mt5.shutdown()
            logger.info("✓ MT5 Disconnected")
