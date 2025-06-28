import requests
import pandas as pd
import pandas_ta as ta
import telegram
from datetime import datetime
import time

# === CONFIG ===
TOKEN = "7454567397:AAEbFH2XY1BXmQprKoyyU_0IuWVddtiZmMQ"
CHAT_ID = "6877756288"
INTERVAL = 900  # 15 minutos

bot = telegram.Bot(token=TOKEN)

def test_send():
    try:
        now = datetime.now().strftime("%H:%M:%S")
        bot.send_message(chat_id=CHAT_ID, text=f"✅ Bot funcionando! Mensagem de teste enviada às {now}")
        print(f"[{now}] Mensagem de teste enviada com sucesso.")
    except Exception as e:
        print(f"[ERRO ao enviar mensagem de teste] {e}")

if __name__ == "_main_":
    test_send()
    time.sleep(60)  # Espera 1 minuto antes de encerrar (pro ver se a mensagem chega no Telegram)
