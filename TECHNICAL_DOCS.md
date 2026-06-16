# TECHNICAL DOCUMENTATION - QUANT MATRIX CONSOLE V14

## 📑 TABLE OF CONTENTS

1. [System Architecture](#system-architecture)
2. [Component Breakdown](#component-breakdown)
3. [Indicator Calculations](#indicator-calculations)
4. [Signal Generation](#signal-generation)
5. [Data Flow](#data-flow)
6. [Configuration Guide](#configuration-guide)

---

## 🏗️ SYSTEM ARCHITECTURE

### Three-Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND LAYER                            │
│              (Cyberpunk Dashboard - index.html)             │
│  - Dark theme UI with matrix green (#00ff66)               │
│  - Real-time DOM updates via innerText                     │
│  - No client-side calculations (prevents freezing)         │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/JSON
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVER LAYER                              │
│               (Flask Gateway - app.py)                      │
│  - Runs on 127.0.0.1:9000                                  │
│  - Orchestrates all analysis requests                      │
│  - Returns pre-formatted JSON with string values           │
└────────────────────┬────────────────────────────────────────┘
                     │ Method calls
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  ENGINE LAYER                               │
│          (Analysis Engine - core_engine.py)                │
│  - QuantMatrixEngine class with 21 indicators              │
│  - MT5 connection & data streaming                         │
│  - All calculations return pre-formatted strings           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 COMPONENT BREAKDOWN

### 1. **FRONTEND LAYER** (`templates/index.html`)

#### Purpose
- Display real-time market data with professional UI
- Provide symbol watchlist navigation
- Show confluence indicator voting board
- Display multi-timeframe trading signals

#### Key Sections

**Left Sidebar (Watchlist)**
```html
<!-- Symbol buttons for XAUUSD, EURUSD, GBPUSD, BTCUSD -->
<button class="symbol-btn" data-symbol="XAUUSD">XAUUSD</button>

<!-- Auto-switches data stream to selected symbol -->
<!-- Updates all center boxes with new analysis -->
```

**Center Grid (Performance Deck)**
```html
<!-- 14 information boxes displaying: -->
1. Current Market Price (Live quote)
2. Account Metrics (Equity, Balance, Spread)
3. System Confidence (Overall consensus score)
4. Smart Money Concepts (Structure analysis)
5. Volume Analysis (VWAP, OBV, MFI, POC)
6. Trend Indicators (SMA, EMA, Supertrend)
7. Bollinger Bands (Upper, Middle, Lower)
8. Fibonacci Levels (6 retracement levels)
9. Momentum Indicators (RSI, Stochastic, CCI)
10. MACD (MACD, Signal, Histogram)
11. ATR & ADX (Volatility & Direction)
12. Pivot Points (R2, R1, Pivot, S1, S2)
13. Trading Signals - Scalping (M5)
14. Trading Signals - Swing (H4)
15. Trading Signals - Long-term (D1)
16. Expansion Slots (Reserved)
```

**Right Sidebar (Confluence Board)**
```html
<!-- Indicator voting matrix showing: -->
- SMC (BUY/SELL/NEUTRAL)
- VWAP (BUY/SELL/NEUTRAL)
- Bollinger Bands (BUY/SELL/NEUTRAL)
- MACD (BUY/SELL/NEUTRAL)
- RSI (BUY/SELL/NEUTRAL)
- Supertrend (BUY/SELL/NEUTRAL)
- Stochastic (BUY/SELL/NEUTRAL)
- ADX (BUY/SELL/NEUTRAL)
- Ichimoku (BUY/SELL/NEUTRAL)
- CCI (BUY/SELL/NEUTRAL)

<!-- Live news feed (simulated market events) -->
```

#### JavaScript Auto-Refresh
```javascript
// Fetches data every 2 seconds
setInterval(updateDashboard, 2000);

// Fetches: GET /api/analyze/XAUUSD
// Displays all values as plain text (no calculations)
```

---

### 2. **SERVER LAYER** (`app.py`)

#### Purpose
- Receive HTTP requests for symbol analysis
- Orchestrate engine calculations
- Format all data as strings before JSON serialization
- Serve static HTML/CSS

#### Routes

**Route: GET `http://127.0.0.1:9000/`**
```
Serves: templates/index.html (main dashboard)
```

**Route: GET `http://127.0.0.1:9000/api/analyze/<symbol>`**
```python
# Example: GET /api/analyze/XAUUSD

# Returns JSON:
{
  "symbol": "XAUUSD",
  "timestamp": "2025-06-16T14:30:00",
  "current_price": "2450.5234",  # ← STRING, not number!
  "account": {
    "equity": "$5,234.56",
    "balance": "$5,000.00",
    "spread": "15 pts"
  },
  "volume": {
    "vwap": "2450.1234",
    "obv": "125432100",
    "mfi": "65.43",
    "volume_profile_poc": "2450.5000",
    "chaikin_mf": "0.3456"
  },
  "trend": { ... },
  "volatility": { ... },
  "momentum": { ... },
  "smart_money": {
    "structure": "HH",
    "signal": "BUY",
    "level": "2450.5234"
  },
  "trading_signals": {
    "scalping": {
      "entry": "2450.5234",
      "sl": "2448.9234",
      "tp1": "2451.1234",
      "tp2": "2451.7234",
      "tp3": "2452.3234",
      "signal": "BUY"
    },
    ...
  },
  "system_confidence": "75% BUY"
}
```

**Route: GET `http://127.0.0.1:9000/api/watchlist`**
```
Returns analysis for all 4 symbols:
{
  "XAUUSD": { full analysis... },
  "EURUSD": { full analysis... },
  "GBPUSD": { full analysis... },
  "BTCUSD": { full analysis... }
}
```

**Route: GET `http://127.0.0.1:9000/api/status`**
```
Returns:
{
  "status": "connected",
  "account": {
    "equity": "$5,234.56",
    "balance": "$5,000.00",
    "spread": "15 pts"
  }
}
```

---

### 3. **ENGINE LAYER** (`core_engine.py`)

#### Purpose
- Calculate all 21 technical indicators
- Fetch OHLCV data from MT5
- Generate multi-timeframe trading signals
- Calculate confluence scoring

#### Core Class: `QuantMatrixEngine`

```python
class QuantMatrixEngine:
    def __init__(self, account, password, server)
    def init_mt5()
    def get_account_info()
    def get_ohlcv(symbol, timeframe, bars)
```

#### Data Input Flow
```
MT5 Terminal (Live Market Data)
        ↓
get_ohlcv(symbol, "H1", 300)
        ↓
pandas DataFrame with 300 hourly candles
        ↓
[open, high, low, close, volume]
        ↓
All 21 Indicators Calculate
        ↓
Return pre-formatted STRINGS
```

---

## 📊 INDICATOR CALCULATIONS

### VOLUME INDICATORS (5 indicators)

#### 1. **VWAP (Volume Weighted Average Price)**
```python
TP = (High + Low + Close) / 3
VWAP = Σ(TP × Volume) / Σ(Volume)  # Rolling 20 bars
```
- **Signal**: Price > VWAP = Bullish, Price < VWAP = Bearish
- **Weight in Confluence**: 20%

#### 2. **OBV (On-Balance Volume)**
```python
If Close > Close[-1]:
    OBV = OBV[-1] + Volume
Else if Close < Close[-1]:
    OBV = OBV[-1] - Volume
Else:
    OBV = OBV[-1]
```
- **Signal**: Rising OBV = Buying pressure, Falling OBV = Selling pressure
- **Weight in Confluence**: Part of volume analysis

#### 3. **MFI (Money Flow Index)**
```python
TP = (High + Low + Close) / 3
MF = TP × Volume
Positive MF = Sum when TP > TP[-1]
Negative MF = Sum when TP < TP[-1]
MFI = 100 - (100 / (1 + (Positive MF / Negative MF)))
```
- **Signal**: MFI > 80 = Overbought (SELL), MFI < 20 = Oversold (BUY)
- **Range**: 0-100 (like RSI)

#### 4. **Volume Profile POC (Point of Control)**
```python
# Find price level with highest volume
Price_Range / 20 bins
For each bin: Sum(Volume)
POC = Price level with maximum volume
```
- **Signal**: Price above POC = Bullish, Price below POC = Bearish
- **Use Case**: Institutional support/resistance

#### 5. **Chaikin Money Flow**
```python
MFV = ((Close - Low) - (High - Close)) / (High - Low) × Volume
CMF = Sum(MFV) / Sum(Volume)  # 20-period
```
- **Signal**: CMF > 0 = Accumulation (BUY), CMF < 0 = Distribution (SELL)

---

### TREND INDICATORS (7 indicators)

#### 1. **SMA (Simple Moving Average)**
```python
SMA = Sum(Close) / Period
# Typically: SMA20 & SMA50
```
- **Signal**: Price > SMA = Uptrend, Price < SMA = Downtrend
- **Crossover**: SMA20 > SMA50 = Golden Cross (BUY)

#### 2. **EMA (Exponential Moving Average)**
```python
EMA = Close × Multiplier + EMA[-1] × (1 - Multiplier)
Multiplier = 2 / (Period + 1)
# Typically: EMA12 & EMA26
```
- **Signal**: Same as SMA but more responsive to recent prices
- **Use**: MACD calculation uses EMA12 & EMA26

#### 3. **Ichimoku Cloud**
```python
Tenkan-sen = (9-period High + 9-period Low) / 2
Kijun-sen = (26-period High + 26-period Low) / 2
Senkou Span A = (Tenkan + Kijun) / 2
Senkou Span B = (52-period High + 52-period Low) / 2
```
- **Signal**: Price above cloud = BUY, Price below cloud = SELL
- **Weight**: 15% in confluence

#### 4. **Supertrend**
```python
HL2 = (High + Low) / 2
Basic Upper Band = HL2 + (Multiplier × ATR)
Basic Lower Band = HL2 - (Multiplier × ATR)
Final Upper Band = min(Basic UB, Final UB[-1])
Final Lower Band = max(Basic LB, Final LB[-1])
```
- **Signal**: Clear BUY/SELL levels
- **Advantage**: No repainting, real-time reversal detection
- **Weight**: 15% in confluence

#### 5. **Parabolic SAR (Stop and Reverse)**
```python
SAR = Prior SAR + AF × (Prior EP - Prior SAR)
AF = Acceleration Factor (starts at 0.02, max 0.2)
EP = Extreme Point
```
- **Signal**: SAR below price = BUY, SAR above price = SELL
- **Use**: Trailing stop levels

#### 6. **Pivot Points**
```python
Pivot = (High + Low + Close) / 3
R1 = (2 × Pivot) - Low
S1 = (2 × Pivot) - High
R2 = Pivot + (High - Low)
S2 = Pivot - (High - Low)
```
- **Signal**: Support (S1, S2) and Resistance (R1, R2) levels
- **Calculated**: Daily (recalculates at 00:00 UTC)

#### 7. **Smart Money Concepts (SMC)**
```python
If Current Price > Recent High:
    Signal = "BUY" (Higher High - HH)
Else if Current Price < Recent Low:
    Signal = "SELL" (Lower Low - LL)
Else if Price > Previous Resistance:
    Signal = "BUY" (Break of Structure - BOS)
Else:
    Signal = "NEUTRAL"
```
- **Weight**: 25% in confluence (highest institutional weight)

---

### VOLATILITY INDICATORS (3 indicators)

#### 1. **ATR (Average True Range)**
```python
True Range = max(High - Low, |High - Close[-1]|, |Low - Close[-1]|)
ATR = Average(True Range)  # 14-period
```
- **Signal**: High ATR = High volatility, Low ATR = Low volatility
- **Use**: Position sizing, stop-loss placement
- **Formula**: SL = Entry - (ATR × 1.5) for scalping

#### 2. **Bollinger Bands**
```python
Middle Band = SMA(20)
Upper Band = Middle + (2 × StdDev)
Lower Band = Middle - (2 × StdDev)
```
- **Signal**: Price > Upper = Overbought (SELL), Price < Lower = Oversold (BUY)
- **Weight**: 15% in confluence

#### 3. **Fibonacci Retracement Levels**
```python
High = Max Price in lookback period
Low = Min Price in lookback period
Range = High - Low

Level 0% = High
Level 23.6% = High - (Range × 0.236)
Level 38.2% = High - (Range × 0.382)
Level 50% = High - (Range × 0.5)
Level 61.8% = High - (Range × 0.618)
Level 100% = Low
```
- **Signal**: Key support/resistance levels
- **Use**: Entry, exit, profit-taking zones

---

### MOMENTUM INDICATORS (5 indicators)

#### 1. **RSI (Relative Strength Index)**
```python
Gain = Average of positive closes
Loss = Average of negative closes
RS = Gain / Loss
RSI = 100 - (100 / (1 + RS))  # 14-period
```
- **Range**: 0-100
- **Signal**: RSI > 70 = Overbought (SELL), RSI < 30 = Oversold (BUY)
- **Weight**: 10% in confluence

#### 2. **MACD (Moving Average Convergence Divergence)**
```python
MACD = EMA12 - EMA26
Signal Line = EMA9(MACD)
Histogram = MACD - Signal Line
```
- **Signal**: MACD > Signal = BUY, MACD < Signal = SELL
- **Divergence**: Hidden divergence = trend continuation
- **Weight**: 15% in confluence

#### 3. **Stochastic Oscillator**
```python
K% = ((Close - Low14) / (High14 - Low14)) × 100
D% = EMA3(K%)

Range: 0-100
Overbought: K > 80
Oversold: K < 20
```
- **Signal**: K crosses above D = BUY, K crosses below D = SELL
- **Use**: Momentum confirmation

#### 4. **CCI (Commodity Channel Index)**
```python
TP = (High + Low + Close) / 3
CCI = (TP - SMA(TP)) / (0.015 × Mean Absolute Deviation)
```
- **Signal**: CCI > 100 = Overbought (SELL), CCI < -100 = Oversold (BUY)
- **Range**: -100 to +100 (can extend beyond)

#### 5. **ADX (Average Directional Index)**
```python
Plus DM = High - High[-1] (if positive)
Minus DM = Low[-1] - Low (if positive)
Plus DI = 100 × (Plus DM / ATR)
Minus DI = 100 × (Minus DM / ATR)
ADX = Average(|Plus DI - Minus DI| / (Plus DI + Minus DI))
```
- **Signal**: ADX > 25 = Strong trend, ADX < 25 = Ranging market
- **Use**: Filter for trend-following vs range-trading strategies

---

## 🚀 SIGNAL GENERATION

### Multi-Timeframe Architecture

The system generates **3 independent trading signals** based on different timeframes:

#### 1. **SCALPING SIGNAL (M5 Timeframe)**
```
Purpose: Ultra-short term (5-minute) trades
Risk/Reward: 1:1.5
Duration: 5-30 minutes

Calculation:
Entry = Current Price
ATR = Average True Range(14)

Stop Loss = Entry - (ATR × 1.5)
Take Profit 1 = Entry + (ATR × 0.5)    [First target]
Take Profit 2 = Entry + (ATR × 1.0)    [Second target]
Take Profit 3 = Entry + (ATR × 1.5)    [Max profit]

Example (XAUUSD):
Entry: 2450.50
ATR: 3.20
SL: 2450.50 - 4.80 = 2445.70
TP1: 2450.50 + 1.60 = 2452.10
TP2: 2450.50 + 3.20 = 2453.70
TP3: 2450.50 + 4.80 = 2455.30
```

#### 2. **SWING SIGNAL (H4 Timeframe)**
```
Purpose: Medium-term (4-hour candles) trades
Risk/Reward: 1:2.5
Duration: 4 hours to 2 days

Calculation:
Entry = Current Price
ATR = Average True Range(14)

Stop Loss = Entry - (ATR × 2.0)
Take Profit 1 = Entry + (ATR × 1.0)
Take Profit 2 = Entry + (ATR × 2.0)
Take Profit 3 = Entry + (ATR × 3.0)

Example (XAUUSD):
Entry: 2450.50
ATR: 5.40
SL: 2450.50 - 10.80 = 2439.70
TP1: 2450.50 + 5.40 = 2455.90
TP2: 2450.50 + 10.80 = 2461.30
TP3: 2450.50 + 16.20 = 2466.70
```

#### 3. **LONG-TERM SIGNAL (D1 Timeframe)**
```
Purpose: Long-term (daily candles) trades
Risk/Reward: 1:4.0
Duration: 2 weeks to 2 months

Calculation:
Entry = Current Price
ATR = Average True Range(14)

Stop Loss = Entry - (ATR × 3.0)
Take Profit 1 = Entry + (ATR × 2.0)
Take Profit 2 = Entry + (ATR × 4.0)
Take Profit 3 = Entry + (ATR × 6.0)

Example (XAUUSD):
Entry: 2450.50
ATR: 8.60
SL: 2450.50 - 25.80 = 2424.70
TP1: 2450.50 + 17.20 = 2467.70
TP2: 2450.50 + 34.40 = 2484.90
TP3: 2450.50 + 51.60 = 2502.10
```

---

## 🎯 CONFLUENCE SCORING SYSTEM

### Weighted Indicator Agreement

Each indicator "votes" for BUY/SELL/NEUTRAL. The system calculates a **System Confidence Score**:

```python
WEIGHTING (Institutional Priority):
├─ Smart Money Concepts (SMC): 25%    [Highest institutional weight]
├─ VWAP: 20%                          [Volume-based
]
├─ Bollinger Bands: 15%
├─ MACD: 15%
├─ Supertrend: 15%
└─ RSI: 10%

CALCULATION:
Score = (SMC_weight × SMC_vote +
         VWAP_weight × VWAP_vote +
         BB_weight × BB_vote +
         MACD_weight × MACD_vote +
         ST_weight × ST_vote +
         RSI_weight × RSI_vote) / 100

OUTPUT RANGES:
75-100% = STRONG BUY  (Green)
60-74%  = BUY         (Light Green)
40-59%  = NEUTRAL     (Yellow)
25-39%  = SELL        (Light Red)
0-24%   = STRONG SELL (Red)

EXAMPLE:
SMC = BUY (25%)
VWAP = BUY (20%)
BB = SELL (7.5%)
MACD = BUY (15%)
ST = BUY (15%)
RSI = NEUTRAL (5%)

Total = 82.5% STRONG BUY
```

---

## 📡 DATA FLOW SEQUENCE

```
1. USER LOADS DASHBOARD
   ↓
2. index.html loaded, JavaScript initialized
   ↓
3. setInterval(updateDashboard, 2000)  // Every 2 seconds
   ↓
4. JavaScript sends: GET /api/analyze/XAUUSD
   ↓
5. Flask route receives request (app.py)
   ↓
6. analyze_symbol("XAUUSD") called
   ↓
7. ENGINE.get_ohlcv("XAUUSD", "H1", 300) → MT5
   ↓
8. Receives 300 hourly candles from MT5
   ↓
9. ALL 21 INDICATORS CALCULATED (core_engine.py)
   ├─ Volume: VWAP, OBV, MFI, POC, Chaikin
   ├─ Trend: SMA, EMA, Ichimoku, Supertrend, SAR
   ├─ Volatility: ATR, Bollinger, Fibonacci
   ├─ Momentum: RSI, MACD, Stochastic, CCI, ADX
   ├─ Structure: SMC
   └─ Signals: Scalping, Swing, Long-term
   ↓
10. ALL VALUES FORMATTED AS STRINGS
    ├─ "2450.5234"
    ├─ "$5,234.56"
    └─ "75% STRONG BUY"
    ↓
11. JSON RESPONSE:
    {
      "current_price": "2450.5234",
      "volume": { "vwap": "2450.1234", ... },
      "trend": { "sma_20": "2448.2134", ... },
      ...
    }
    ↓
12. SENT TO FRONTEND
    ↓
13. JavaScript receives JSON
    ↓
14. DOM UPDATE (using innerText only):
    document.getElementById('current-price').innerText = "2450.5234"
    ↓
15. DASHBOARD DISPLAYS LIVE DATA
    ↓
16. CONFLUENCE BOARD UPDATED
    (Shows BUY/SELL votes from each indicator)
    ↓
17. WAIT 2 SECONDS
    ↓
18. REPEAT (Back to step 4)
```

---

## ⚙️ CONFIGURATION GUIDE

### Environment Variables (.env)

```ini
# MT5 Connection
MT5_ACCOUNT=50035319
MT5_PASSWORD=your_actual_password
MT5_SERVER=LiteFinance-MT5-Live

# Flask Server
FLASK_HOST=127.0.0.1
FLASK_PORT=9000
FLASK_ENV=production
```

### Modifiable Parameters

**In `core_engine.py`:**

```python
# Bollinger Bands
calculate_bollinger_bands(df, period=20, std_dev=2)

# Fibonacci
calculate_fibonacci(df)  # Fixed at 0%, 23.6%, 38.2%, 50%, 61.8%, 100%

# RSI
calculate_rsi(df, period=14)

# MACD
calculate_macd(df, fast=12, slow=26, signal=9)

# Stochastic
calculate_stochastic(df, period=14, smooth_k=3, smooth_d=3)

# CCI
calculate_cci(df, period=20)

# ADX
calculate_adx(df, period=14)

# Supertrend
calculate_supertrend(df, period=10, multiplier=3)
```

---

## 🔒 SECURITY BEST PRACTICES

### ✅ IMPLEMENTED
- ✓ All credentials in `.env` (not committed)
- ✓ `.env` in `.gitignore`
- ✓ No API keys in HTML
- ✓ No trading execution buttons
- ✓ Local server only (127.0.0.1)
- ✓ Read-only analysis mode

### ⚠️ BEFORE PRODUCTION
- [ ] Regenerate MT5 password
- [ ] Use environment variable manager
- [ ] Enable HTTPS if external access needed
- [ ] Implement rate limiting
- [ ] Add request authentication
- [ ] Use secrets manager (AWS Secrets, HashiCorp Vault)

---

## 📋 QUICK REFERENCE TABLE

| Indicator | Period | Range | Signal | Weight |
|-----------|--------|-------|--------|--------|
| VWAP | 20 | Any | Price > VWAP = BUY | 20% |
| OBV | Cumulative | Any | Rising = BUY | Part of Volume |
| MFI | 14 | 0-100 | < 20 = BUY, > 80 = SELL | Part of Volume |
| SMA | 20/50 | Any | Price > SMA = BUY | Trend |
| EMA | 12/26 | Any | EMA12 > EMA26 = BUY | Trend |
| RSI | 14 | 0-100 | < 30 = BUY, > 70 = SELL | 10% |
| MACD | 12/26/9 | Any | MACD > Signal = BUY | 15% |
| Stochastic | 14 | 0-100 | K > 80 = SELL, K < 20 = BUY | Momentum |
| CCI | 20 | ±100 | > 100 = SELL, < -100 = BUY | Momentum |
| ADX | 14 | 0-100 | > 25 = Trending, < 25 = Ranging | Direction |
| ATR | 14 | Any | High = Volatile, Low = Stable | Position Sizing |
| Bollinger | 20/2 | Any | Price > Upper = SELL, < Lower = BUY | 15% |
| Fibonacci | N/A | 0-100% | Key levels for S/R | Volatility |
| Supertrend | 10/3 | Any | Clear BUY/SELL | 15% |
| SMC | Recent | N/A | Structure analysis | 25% |
| Ichimoku | 9/26/52 | Any | Price > Cloud = BUY | Trend |
| Pivot Points | Daily | N/A | R1/R2 = Resistance, S1/S2 = Support | Structure |

---

## 🎓 EDUCATIONAL NOTES

### Why Backend String Formatting?
1. **Prevents $0.00 Freezing**: Calculations happen once, not on every JS update
2. **Eliminates Floating-Point Errors**: Consistent precision across all browsers
3. **Reduces Bandwidth**: One JSON per request (vs. raw data)
4. **Improves Performance**: Dashboard responsive, no DOM redraws for calculations

### Why No Trading Buttons?
1. **Pure Analysis Tool**: Separates decision-making from execution
2. **Reduces Accidents**: No accidental order placement
3. **Institutional Compliance**: Analysis-only mode for institutional use
4. **Manual Decision-Making**: Encourages thoughtful trade selection

### Indicator Weighting Philosophy
- **SMC (25%)**: Smart Money moves markets—highest priority
- **VWAP (20%)**: Volume shows institutional accumulation/distribution
- **Bollinger (15%)**: Volatility context for breakouts
- **MACD (15%)**: Momentum confirmation
- **Supertrend (15%)**: Trend direction confirmation
- **RSI (10%)**: Overbought/oversold extremes (confirmatory)

### Why Multiple Timeframes?
- **Scalping (M5)**: Quick profit, tight stops (1:1.5 RR)
- **Swing (H4)**: Medium risk/reward (1:2.5 RR)
- **Long-term (D1)**: High potential, longer duration (1:4 RR)
- **Decision Rule**: Wait for alignment across timeframes for strongest signals

---

## 📞 TROUBLESHOOTING

### "MT5 Init Failed"
```
1. Verify account number matches broker account
2. Check password is correct (case-sensitive)
3. Confirm broker server name matches
4. Ensure MT5 terminal is running (if broker requires it)
5. Test login directly in MetaTrader 5
```

### "No data for SYMBOL"
```
1. Verify symbol exists on broker (e.g., XAUUSD vs GOLD)
2. Check if market is open for that symbol
3. Try different symbols: EURUSD, GBPUSD
4. Check if data stream is paused
5. Increase bars parameter: bars=500 → bars=1000
```

### Dashboard Shows "N/A"
```
1. Check Python console for exceptions
2. Verify at least 50 candles loaded
3. Ensure no data gaps
4. Check file permissions
5. Verify numpy/pandas installed correctly
```

### Slow Refresh Rate
```
1. Increase refresh interval: 2000ms → 5000ms
2. Reduce bar count: 300 → 100
3. Move to faster network
4. Check CPU usage
5. Consider caching indicator results
```

---

**Built for serious traders and institutional analysis. Pure analytical power—no execution distractions.**
