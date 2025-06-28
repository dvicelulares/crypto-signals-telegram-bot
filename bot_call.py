import requests, pandas as pd, pandas_ta as ta
import telegram, time
from datetime import datetime

TOKEN = "7454567397:AAEbFH2XY1BXmQprKoyyU_0IuWVddtiZmMQ"
CHAT_ID = "6877756288"
bot = telegram.Bot(token=TOKEN)

INTERVAL = 3600  # 1 hora

def get_klines(sym):
    url = f"https://api.binance.com/api/v3/klines?symbol={sym}&interval=1h&limit=100"
    df = pd.DataFrame(requests.get(url).json(), columns=list(range(12)))
    df['close'] = pd.to_numeric(df[4])
    return df

def analyze(sym, name):
    df = get_klines(sym)
    df['rsi'] = ta.rsi(df['close'], 14)
    df['ema9'] = ta.ema(df['close'], 9)
    df['ema21'] = ta.ema(df['close'], 21)
    price = df['close'].iloc[-1]
    rsi = df['rsi'].iloc[-1]
    e9, e21 = df['ema9'].iloc[-1], df['ema21'].iloc[-1]

    trend = "🔄 Consolidação"
    if e9 > e21 and rsi < 70: trend = "📈 ALTA"
    elif e9 < e21 and rsi > 30: trend = "📉 BAIXA"

    return f"{name} ${price:.2f} | RSI {rsi:.1f} | EMA9 {e9:.1f} / EMA21 {e21:.1f} — {trend}"

def send_signal():
    now = datetime.now().strftime("%d/%m %H:%M")
    msg = f"📊 CALL — {now}\n"
    msg += analyze("BTCUSDT", "Bitcoin") + "\n"
    msg += analyze("ETHUSDT", "Ethereum") + "\n"
    msg += analyze("SOLUSDT", "Solana") + "\n"
    bot.send_message(CHAT_ID, msg, parse_mode=telegram.ParseMode.MARKDOWN)

if _name_ == "_main_":
    while True:
        send_signal()
        time.sleep(INTERVAL)
