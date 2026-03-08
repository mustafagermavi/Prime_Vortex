import streamlit as st
import ccxt
import pandas as pd
import pandas_ta as ta

st.set_page_config(page_title="Prime Vortex Dashboard", layout="wide")

st.title("🌐 Prime Vortex Crypto Scanner")
st.write("Real-time RSI & Trend analysis for top 50 Global Assets.")

# List of Symbols
SYMBOLS = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 
    'AVAX/USDT', 'DOT/USDT', 'LINK/USDT', 'MATIC/USDT'
]

def fetch_data(symbol):
    try:
        exchange = ccxt.kucoin()
        bars = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=100)
        df = pd.DataFrame(bars, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
        df['RSI'] = ta.rsi(df['close'], length=14)
        df['EMA_50'] = ta.ema(df['close'], length=50)
        return {
            "Symbol": symbol,
            "Price": df['close'].iloc[-1],
            "RSI": round(df['RSI'].iloc[-1], 2),
            "Trend": "Bullish" if df['close'].iloc[-1] > df['EMA_50'].iloc[-1] else "Bearish"
        }
    except:
        return None

if st.button('🔄 Refresh Market Data'):
    data_list = []
    with st.spinner('Scanning market...'):
        for s in SYMBOLS:
            res = fetch_data(s)
            if res:
                data_list.append(res)
    
    df_display = pd.DataFrame(data_list)
    
    # Styling
    st.table(df_display)
