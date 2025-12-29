# config.py
import os
from dotenv import load_dotenv

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(BASE_PATH, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    ZABBIX_API_URL = os.getenv("ZABBIX_API_URL", "")
