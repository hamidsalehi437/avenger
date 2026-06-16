# QUANT MATRIX CONSOLE V14 - SETUP & DEPLOYMENT GUIDE

## 📋 SYSTEM OVERVIEW

**QUANT MATRIX CONSOLE V14** is a real-time financial analytics dashboard featuring:

- ✅ **21 Technical Indicators** (all calculated on backend as strings)
- ✅ **Multi-Timeframe Trading Signals** (Scalping/M5, Swing/H4, Long-term/D1)
- ✅ **Smart Money Concepts** (SMC) Structure Analysis
- ✅ **Confluence Voting Board** - Indicator Agreement Matrix
- ✅ **Live Account Metrics** (Equity, Balance, Spread)
- ✅ **Dark Cyberpunk UI** - Matrix green theme
- ✅ **Zero Client-Side Calculations** - All math on Python backend
- ✅ **4 Symbol Watchlist** - XAUUSD, EURUSD, GBPUSD, BTCUSD

---

## 🔧 INSTALLATION

### 1. **Clone Repository**
```bash
git clone https://github.com/hamidsalehi437/avenger.git
cd avenger
git checkout quant-matrix-dashboard
```

### 2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure Credentials Securely**

**⚠️ CRITICAL: NEVER commit credentials to Git**

Create `.env` file in project root:
```ini
MT5_ACCOUNT=50035319
MT5_PASSWORD=your_actual_password_here
MT5_SERVER=LiteFinance-MT5-Live
FLASK_HOST=127.0.0.1
FLASK_PORT=9000
FLASK_ENV=production
```

Add `.env` to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

---

## 🚀 RUNNING THE APPLICATION

### Start Flask Server
```bash
python app.py
```

**Expected Output:**
```
✓ MT5 Connected: 50035319
* Running on http://127.0.0.1:9000
```

### Open Dashboard
```
http://127.0.0.1:9000
```

---

## 📊 INDICATOR DESCRIPTIONS

### **VOLUME INDICATORS**
1. **VWAP** - Volume Weighted Average Price (session anchor)
2. **OBV** - On-Balance Volume (cumulative volume analysis)
3. **MFI** - Money Flow Index (volume-weighted momentum)
4. **Volume Profile POC** - Point of Control (highest volume level)
5. **Chaikin MF** - Chaikin Money Flow (price/volume correlation)

### **TREND INDICATORS**
6. **SMA** - Simple Moving Average (20, 50)
7. **EMA** - Exponential Moving Average (12, 26)
8. **Supertrend** - Trend reversal detector with ATR
9. **Parabolic SAR** - Stop and Reverse levels
10. **Ichimoku** - Tenkan, Kijun, Senkou signals

### **VOLATILITY INDICATORS**
11. **ATR** - Average True Range (volatility measure)
12. **Bollinger Bands** - Upper, Middle, Lower bands (20, 2)
13. **Fibonacci Levels** - Retracement levels (0%, 23.6%, 38.2%, 50%, 61.8%, 100%)

### **MOMENTUM INDICATORS**
14. **RSI** - Relative Strength Index (14) - Overbought/Oversold
15. **MACD** - Moving Average Convergence Divergence
16. **Stochastic** - K% and D% (momentum oscillator)
17. **CCI** - Commodity Channel Index (trend strength)
18. **ADX** - Average Directional Index (trend direction)

### **STRUCTURE ANALYSIS**
19. **SMC** - Smart Money Concepts (HH, LL, BOS, ChoCh)
20. **Pivot Points** - R2, R1, Pivot, S1, S2 levels

### **ADDITIONAL**
21. **Confluence Scoring** - System Confidence % (weighted indicator agreement)

---

## 📈 TRADING SIGNALS BREAKDOWN

### **SCALPING (M5 Timeframe)**
- **Entry**: Current market price
- **SL**: Entry - (ATR × 1.5)
- **TP1**: Entry + (ATR × 0.5)
- **TP2**: Entry + (ATR × 1.0)
- **TP3**: Entry + (ATR × 1.5)
- **Risk/Reward**: 1:1.5

### **SWING TRADING (H4 Timeframe)**
- **Entry**: Current market price
- **SL**: Entry - (ATR × 2.0)
- **TP1**: Entry + (ATR × 1.0)
- **TP2**: Entry + (ATR × 2.0)
- **TP3**: Entry + (ATR × 3.0)
- **Risk/Reward**: 1:2.5

### **LONG-TERM (D1 Timeframe)**
- **Entry**: Current market price
- **SL**: Entry - (ATR × 3.0)
- **TP1**: Entry + (ATR × 2.0)
- **TP2**: Entry + (ATR × 4.0)
- **TP3**: Entry + (ATR × 6.0)
- **Risk/Reward**: 1:4.0

---

## 🎯 CONFLUENCE VOTING BOARD

The right sidebar displays individual indicator signals:
- 🟢 **GREEN (BUY)** - Indicator suggests bullish movement
- 🔴 **RED (SELL)** - Indicator suggests bearish movement
- 🟡 **YELLOW (NEUTRAL)** - No clear signal or ranging

**System Confidence Calculation:**
```
Confidence = Weighted Average of All Indicators

Weighting (Institutional Importance):
- SMC: 25%
- VWAP: 20%
- Bollinger: 15%
- MACD: 15%
- RSI: 10%
- Supertrend: 15%

Output: XX% [STRONG BUY / BUY / NEUTRAL / SELL / STRONG SELL]
```

---

## 🔐 SECURITY BEST PRACTICES

### ✅ DO
- Store credentials in `.env` file
- Add `.env` to `.gitignore`
- Use environment variables in all apps
- Regenerate MT5 password after sharing
- Use cent/micro accounts for testing
- Enable 2FA on MT5 account

### ❌ DON'T
- Hardcode credentials in Python files
- Commit `.env` to Git
- Share passwords via email/chat
- Use demo/live accounts interchangeably
- Leave console open on shared machines
- Enable unnecessary MT5 permissions

---

## 📡 API ENDPOINTS

### **Live Analysis**
```
GET /api/analyze/<SYMBOL>
Response: JSON with all indicators calculated
```

Example:
```bash
curl http://127.0.0.1:9000/api/analyze/XAUUSD
```

### **System Status**
```
GET /api/status
Response: { status, account_info }
```

### **Multi-Symbol Analysis**
```
GET /api/watchlist
Response: JSON analysis for all 4 symbols
```

---

## 🛠️ TROUBLESHOOTING

### **"MT5 Init Failed" Error**
```python
# Check connection
1. Verify account number is correct
2. Confirm password is not expired
3. Check broker server name
4. Ensure MT5 terminal is running (if required)
5. Test with MetaTrader5 directly first
```

### **"No data for SYMBOL" Warning**
```python
# Data fetch issue
1. Verify symbol exists on broker
2. Check market hours (some pairs trade specific hours)
3. Try alternate symbols (EURUSD, GBPUSD)
4. Increase OHLCV bars parameter
5. Check broker data stream status
```

### **Dashboard Shows "N/A" for Indicators**
```python
# Calculation error
1. Check logs: look for exception messages
2. Verify minimum candle count (need 50+ bars)
3. Ensure data has no gaps
4. Try different timeframe
5. Check Python syntax in core_engine.py
```

### **Slow Refresh Rate**
```python
# Optimize performance
1. Reduce refresh interval in HTML (change refreshInterval variable)
2. Use fewer indicators
3. Reduce OHLCV bars count
4. Move to faster server
5. Implement caching layer
```

---

## 📊 DASHBOARD SECTIONS EXPLAINED

### **Left Sidebar - Watchlist**
- Click symbol buttons to switch analysis
- Shows current live account status
- Real-time connection indicator

### **Center Grid - Performance Deck**
- **Current Price Box**: Live quote and timestamp
- **Account Metrics**: Equity, Balance, Spread (broker cost)
- **System Confidence**: Overall signal strength (75%+ = Strong, <25% = Weak)
- **Volume/Trend/Volatility/Momentum**: Individual indicator boxes
- **Trading Signals**: Entry prices, SL, and 3 Take-Profit targets
- **Expansion Slots**: Reserved for future charting modules

### **Right Sidebar - Confluence Board**
- Real-time indicator voting matrix
- Each indicator shows BUY/SELL/NEUTRAL
- Live news feed (simulated market events)
- Color-coded signal display

---

## 🎓 EDUCATIONAL NOTES

**Why Backend Calculations?**
- Prevents $0.00 freezing issues
- Eliminates floating-point errors
- Ensures consistent precision across all clients
- Reduces network bandwidth
- Improves page responsiveness

**Why No Trading Buttons?**
- This is a **pure analytics** tool
- Separates analysis from execution
- Prevents accidental order placement
- Maintains institutional compliance
- Encourages manual decision-making

**Indicator Weighting**
- Institutional traders prioritize SMC > VWAP > Price Action
- Oscillators (RSI, Stochastic) are confirmatory, not primary
- Volume analysis reveals institutional money movement
- Multiple timeframe alignment = stronger signals

---

## 📞 SUPPORT & UPDATES

For issues or enhancements:
1. Check troubleshooting section above
2. Review logs in terminal
3. Verify all dependencies installed
4. Test with different symbols
5. Report bugs with full error message and symbol

---

## 📝 VERSION HISTORY

**V14 - SUPREME INFRASTRUCTURE**
- 21 technical indicators
- Multi-timeframe signals
- Confluence voting system
- Cyberpunk dark theme
- Backend-only calculations
- Zero cache freezing

---

**Built with institutional-grade architecture for serious traders.**
