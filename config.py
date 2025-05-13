import os
from dotenv import load_dotenv

load_dotenv()

# 🔐 Llave secreta para sesiones y flashes
SECRET_KEY = os.getenv("SECRET_KEY", "clave-secreta-soygeek")

# 🔑 Otras APIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
