import requests
import pandas as pd
import pandas_ta as ta
import telegram
import time
from datetime import datetime

# === CONFIGURAÇÕES ===
TOKEN = "7454567397:AAEbFH2XY1BXmQprKoyyU_0IuWVddtiZmMQ"
CHAT_ID = "6877756288"
INTERVAL = 900  # 15 minutos = 900 segundos

# === LISTA DE MOEDAS ===
MOEDAS = {
    "BTCUSDT": "Bitcoin",
    "ETHUSDT": "Ethereum",
    "SOLUSDT": "Solana",
    "BNBUSDT": "BNB",
    "AVAXUSDT": "Avalanche",
    "MATICUSDT": "Polygon",
    "ADAUSDT": "Cardano",
    "DOGEUSDT": "Dogecoin",
    "XRPUSDT": "XRP",
    "INJUSDT": "Injective",
    "OPUSDT": "Optimism",
    "ARBUSDT": "Arbitrum",
    "PYTHUSDT": "Pyth Network",
    "JUPUSDT": "Jupiter",
    "TIAUSDT": "Celestia"
}

bot = telegram.Bot(token=TOKEN)

# === FUNÇÕES ===

def get_klines(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=15m&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=range(12))
    df['close'] = pd.to_numeric(df[4])
    return df

def analyze(symbol, name):
    df = get_klines(symbol)
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['ema9'] = ta.ema(df['close'], length=9)
    df['ema21'] = ta.ema(df['close'], length=21)

    price = df['close'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    ema9 = df['ema9'].iloc[-1]
    ema21 = df['ema21'].iloc[-1]

    high = df['close'][-5:].max() * 1.01  # alvo = última alta +1%
    low = df['close'][-5:].min() * 0.995  # stop = última baixa -0.5%

    if ema9 > ema21 and rsi < 70:
        tendencia = "📈 Alta"
    elif ema9 < ema21 and rsi > 30:
        tendencia = "📉 Baixa"
    else:
        tendencia = "🔄 Consolidação"

    msg = (
        f"{name} ({symbol})\n"
        f"💰 Entrada: {price:.2f}\n"
        f"🎯 Alvo (High): {high:.2f}\n"
        f"🛑 Stop (Low): {low:.2f}\n"
        f"📊 RSI: {rsi:.1f} | EMA9: {ema9:.1f} / EMA21: {ema21:.1f}\n"
        f"🔎 Tendência: {tendencia}\n"
    )
    return msg

def send_calls():
    now = datetime.now().strftime("%d/%m %H:%M")
    mensagem = f"📊 CALL DE MERCADO — {now}\n\n"

    for symbol, name in MOEDAS.items():
        try:
            mensagem += analyze(symbol, name) + "\n"
        except Exception as e:
            mensagem += f"⚠️ Erro com {name}: {e}\n"

    bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode=telegram.ParseMode.MARKDOWN)

# === LOOP INFINITO ===
if __name__ == "_main_":
    while True:
        send_calls()
        time.sleep(INTERVAL)
