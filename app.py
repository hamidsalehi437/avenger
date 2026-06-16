"""
QUANT MATRIX CONSOLE V14 - Flask Gateway Server
Real-time multi-asset financial analytics dashboard
"""

from flask import Flask, render_template, jsonify
from core_engine import QuantMatrixEngine
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

# Initialize engine
ENGINE = None

def init_engine():
    """Initialize the analysis engine"""
    global ENGINE
    try:
        account = os.getenv("MT5_ACCOUNT", "50035319")
        password = os.getenv("MT5_PASSWORD", "Haji\"2020")
        server = os.getenv("MT5_SERVER", "LiteFinance-MT5-Live")
        
        ENGINE = QuantMatrixEngine(int(account), password, server)
        return ENGINE.connected
    except Exception as e:
        logger.error(f"Engine init failed: {e}")
        return False


def analyze_symbol(symbol):
    """Comprehensive analysis for a symbol across all indicators"""
    try:
        if ENGINE is None:
            return {"error": "Engine not connected"}
        
        # Get data for primary analysis (H1 timeframe)
        df = ENGINE.get_ohlcv(symbol, "H1", 300)
        if df is None:
            return {"error": f"Could not fetch data for {symbol}"}
        
        current_price = str(round(df['close'].iloc[-1], 4))
        
        # ==================== CALCULATE ALL INDICATORS ====================
        
        # Volume Indicators
        vwap = ENGINE.calculate_vwap(df)
        obv = ENGINE.calculate_obv(df)
        mfi = ENGINE.calculate_mfi(df)
        volume_profile = ENGINE.calculate_volume_profile(df)
        chaikin = ENGINE.calculate_chaikin(df)
        
        # Trend Indicators
        sma20 = ENGINE.calculate_sma(df, 20)
        sma50 = ENGINE.calculate_sma(df, 50)
        ema12 = ENGINE.calculate_ema(df, 12)
        ema26 = ENGINE.calculate_ema(df, 26)
        ichimoku = ENGINE.calculate_ichimoku(df)
        supertrend = ENGINE.calculate_supertrend(df)
        parabolic_sar = ENGINE.calculate_parabolic_sar(df)
        
        # Volatility Indicators
        atr = ENGINE.calculate_atr(df, 14)
        bollinger = ENGINE.calculate_bollinger_bands(df)
        fibonacci = ENGINE.calculate_fibonacci(df)
        
        # Momentum Indicators
        rsi = ENGINE.calculate_rsi(df)
        macd = ENGINE.calculate_macd(df)
        stochastic = ENGINE.calculate_stochastic(df)
        cci = ENGINE.calculate_cci(df)
        adx = ENGINE.calculate_adx(df)
        
        # Smart Money & Structure
        smc = ENGINE.calculate_smc(df)
        
        # Pivot Points
        pivot_points = ENGINE.calculate_pivot_points(df)
        
        # Multi-timeframe signals
        scalping_signal = ENGINE.generate_scalping_signal(symbol, current_price)
        swing_signal = ENGINE.generate_swing_signal(symbol, current_price)
        longterm_signal = ENGINE.generate_longterm_signal(symbol, current_price)
        
        # Confidence Score
        confidence = ENGINE.calculate_confluence_score(df)
        
        # Account info
        account_info = ENGINE.get_account_info()
        
        return {
            "symbol": symbol,
            "timestamp": datetime.now().isoformat(),
            "current_price": current_price,
            "account": account_info,
            
            # Volume Section
            "volume": {
                "vwap": vwap,
                "obv": obv,
                "mfi": mfi,
                "volume_profile_poc": volume_profile,
                "chaikin_mf": chaikin
            },
            
            # Trend Section
            "trend": {
                "sma_20": sma20,
                "sma_50": sma50,
                "ema_12": ema12,
                "ema_26": ema26,
                "ichimoku": ichimoku,
                "supertrend": supertrend,
                "parabolic_sar": parabolic_sar
            },
            
            # Volatility Section
            "volatility": {
                "atr_14": atr,
                "bollinger_bands": bollinger,
                "fibonacci_levels": fibonacci
            },
            
            # Momentum Section
            "momentum": {
                "rsi_14": rsi,
                "macd": macd,
                "stochastic": stochastic,
                "cci_20": cci,
                "adx_14": adx
            },
            
            # Structure & Smart Money
            "smart_money": {
                "structure": smc["structure"],
                "signal": smc["signal"],
                "level": smc["level"]
            },
            
            # Support & Resistance
            "pivot_points": pivot_points,
            
            # Trading Signals - Multi-timeframe
            "trading_signals": {
                "scalping": scalping_signal,
                "swing": swing_signal,
                "long_term": longterm_signal
            },
            
            # System Confidence
            "system_confidence": confidence
        }
    
    except Exception as e:
        logger.error(f"Analysis error for {symbol}: {e}")
        return {"error": str(e), "symbol": symbol}


@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


@app.route('/api/analyze/<symbol>')
def api_analyze(symbol):
    """API endpoint for live analysis"""
    result = analyze_symbol(symbol)
    return jsonify(result)


@app.route('/api/watchlist')
def api_watchlist():
    """Analyze all watchlist symbols"""
    symbols = ["XAUUSD", "EURUSD", "GBPUSD", "BTCUSD"]
    results = {}
    
    for symbol in symbols:
        results[symbol] = analyze_symbol(symbol)
    
    return jsonify(results)


@app.route('/api/status')
def api_status():
    """Check system status"""
    return jsonify({
        "status": "connected" if ENGINE and ENGINE.connected else "disconnected",
        "account": ENGINE.get_account_info() if ENGINE else {}
    })


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500


if __name__ == '__main__':
    # Initialize engine on startup
    if init_engine():
        logger.info("✓ Engine initialized successfully")
        app.run(
            host=os.getenv("FLASK_HOST", "127.0.0.1"),
            port=int(os.getenv("FLASK_PORT", 9000)),
            debug=False,
            threaded=True
        )
    else:
        logger.error("✗ Failed to initialize engine")
