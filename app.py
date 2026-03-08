import streamlit as st
import ccxt
import pandas as pd
import pandas_ta as ta

# Page configuration
st.set_page_config(page_title="Prime Vortex Dashboard", layout="wide")

st.title("🌐 Prime Vortex Crypto Scanner")
st.write("Real-time market analysis for top assets.")

# List of main symbols
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT']

def fetch_data(symbol):
    try:
        exchange = ccxt.kucoin()
        # Fetch 100 hourly candles
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        
        # Indicators
        df['RSI'] = ta.rsi(df['close'], length=14)
        
        return {
            "Symbol": symbol,
            "Price": df['close'].iloc[-1],
            "RSI": round(df['RSI'].iloc[-1], 2),
            "Status": "Oversold" if df['RSI'].iloc[-1] < 35 else "Normal"
        }
    except Exception as e:
        return None

# Refresh Button
if st.button('🔄 Update Prices'):
    results = []
    for s in SYMBOLS:
        data = fetch_data(s)
        if data:
            results.append(data)
    
    if results:
        st.table(pd.DataFrame(results))
    else:
        st.error("Could not fetch data. Please check your connection.")
else:
    st.info("Click the button above to load market data.")
