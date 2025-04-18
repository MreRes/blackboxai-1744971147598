from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# WhatsApp Bot Configuration
WHATSAPP_CONFIG: Dict[str, Any] = {
    "headless": True,
    "qr_timeout": 60,
    "authentication_timeout": 60,
}

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/database/financial_bot.db")

# Web Server Configuration
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "True").lower() == "true"

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Language Processing Configuration
LANGUAGE_MODEL = os.getenv("LANGUAGE_MODEL", "indonesian")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Dashboard Configuration
DASHBOARD_THEME = {
    "primary_color": "#1a56db",
    "secondary_color": "#7e3af2",
    "success_color": "#0e9f6e",
    "danger_color": "#dc2626",
    "warning_color": "#ff5a1f",
    "info_color": "#3f83f8",
}

# Financial Categories
EXPENSE_CATEGORIES = [
    "Makanan & Minuman",
    "Transportasi",
    "Belanja",
    "Hiburan",
    "Kesehatan",
    "Pendidikan",
    "Tagihan",
    "Lainnya",
]

INCOME_CATEGORIES = [
    "Gaji",
    "Bonus",
    "Investasi",
    "Bisnis",
    "Lainnya",
]

# Command Prefixes
COMMAND_PREFIXES = {
    "expense": ["catat pengeluaran", "tambah pengeluaran", "keluar"],
    "income": ["catat pemasukan", "tambah pemasukan", "masuk"],
    "balance": ["cek saldo", "saldo", "balance"],
    "report": ["laporan", "report"],
    "budget": ["atur budget", "set budget"],
    "help": ["bantuan", "help", "tolong"],
    "dashboard": ["buka dashboard", "dashboard"],
}

# API Configuration
API_V1_PREFIX = "/api/v1"
API_TITLE = "Financial Planner Bot API"
API_DESCRIPTION = "API for WhatsApp Financial Planner Bot"
API_VERSION = "1.0.0"
