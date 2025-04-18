import re
from typing import Dict, Any, Tuple, Optional
import logging
from datetime import datetime

from config.settings import EXPENSE_CATEGORIES, INCOME_CATEGORIES, COMMAND_PREFIXES

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self):
        # Compile regex patterns for better performance
        self.amount_pattern = re.compile(r'(\d+(?:\.\d+)?)')
        self.category_pattern = re.compile(r'untuk|dari\s+(\w+(?:\s+\w+)*)')

    def parse_message(self, text: str) -> Tuple[str, Optional[Dict[str, Any]]]:
        """
        Parse message text and identify command type and parameters
        Returns: (command_type, parameters)
        """
        text = text.lower().strip()

        # Identify command type
        command_type = self._identify_command_type(text)
        if not command_type:
            return "unknown", None

        # Parse parameters based on command type
        try:
            if command_type == "expense":
                return "expense", self._parse_expense(text)
            elif command_type == "income":
                return "income", self._parse_income(text)
            elif command_type == "budget":
                return "budget", self._parse_budget(text)
            elif command_type in ["balance", "report", "help", "dashboard"]:
                return command_type, {}
            else:
                return "unknown", None
        except Exception as e:
            logger.error(f"Error parsing message: {e}")
            return "error", None

    def _identify_command_type(self, text: str) -> Optional[str]:
        """Identify the type of command from the message"""
        for command, prefixes in COMMAND_PREFIXES.items():
            if any(text.startswith(prefix) for prefix in prefixes):
                return command
        return None

    def _parse_expense(self, text: str) -> Dict[str, Any]:
        """Parse expense command text"""
        # Example: "catat pengeluaran 50000 untuk makan"
        try:
            # Extract amount
            amount_match = self.amount_pattern.search(text)
            if not amount_match:
                raise ValueError("Jumlah pengeluaran tidak ditemukan")
            amount = float(amount_match.group(1))

            # Extract category
            category_match = self.category_pattern.search(text)
            if not category_match:
                raise ValueError("Kategori pengeluaran tidak ditemukan")
            category = category_match.group(1).strip()

            # Validate category
            if category not in EXPENSE_CATEGORIES:
                category = "Lainnya"

            return {
                "type": "expense",
                "amount": amount,
                "category": category,
                "date": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error parsing expense: {e}")
            raise ValueError("Format pengeluaran tidak valid. Contoh: catat pengeluaran 50000 untuk makan")

    def _parse_income(self, text: str) -> Dict[str, Any]:
        """Parse income command text"""
        # Example: "catat pemasukan 1000000 dari gaji"
        try:
            # Extract amount
            amount_match = self.amount_pattern.search(text)
            if not amount_match:
                raise ValueError("Jumlah pemasukan tidak ditemukan")
            amount = float(amount_match.group(1))

            # Extract category
            category_match = self.category_pattern.search(text)
            if not category_match:
                raise ValueError("Kategori pemasukan tidak ditemukan")
            category = category_match.group(1).strip()

            # Validate category
            if category not in INCOME_CATEGORIES:
                category = "Lainnya"

            return {
                "type": "income",
                "amount": amount,
                "category": category,
                "date": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error parsing income: {e}")
            raise ValueError("Format pemasukan tidak valid. Contoh: catat pemasukan 1000000 dari gaji")

    def _parse_budget(self, text: str) -> Dict[str, Any]:
        """Parse budget command text"""
        # Example: "atur budget 2000000 per bulan"
        try:
            # Extract amount
            amount_match = self.amount_pattern.search(text)
            if not amount_match:
                raise ValueError("Jumlah budget tidak ditemukan")
            amount = float(amount_match.group(1))

            # Extract period
            period_pattern = re.compile(r'per\s+(hari|minggu|bulan|tahun)')
            period_match = period_pattern.search(text)
            if not period_match:
                raise ValueError("Periode budget tidak ditemukan")
            period = period_match.group(1)

            return {
                "amount": amount,
                "period": period,
                "start_date": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error parsing budget: {e}")
            raise ValueError("Format budget tidak valid. Contoh: atur budget 2000000 per bulan")

    def format_currency(self, amount: float) -> str:
        """Format amount as Indonesian Rupiah"""
        try:
            return f"Rp {amount:,.0f}".replace(",", ".")
        except Exception as e:
            logger.error(f"Error formatting currency: {e}")
            return str(amount)

    def format_response(self, command_type: str, data: Dict[str, Any]) -> str:
        """Format response message based on command type and data"""
        try:
            if command_type == "expense":
                return (f"✅ Pengeluaran sebesar {self.format_currency(data['amount'])} "
                       f"untuk {data['category']} telah dicatat.")
            
            elif command_type == "income":
                return (f"✅ Pemasukan sebesar {self.format_currency(data['amount'])} "
                       f"dari {data['category']} telah dicatat.")
            
            elif command_type == "budget":
                return (f"✅ Budget sebesar {self.format_currency(data['amount'])} "
                       f"per {data['period']} telah diatur.")
            
            elif command_type == "error":
                return "❌ Maaf, terjadi kesalahan. Silakan coba lagi."
            
            else:
                return "❓ Perintah tidak dikenali. Ketik 'bantuan' untuk melihat daftar perintah."
                
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "Maaf, terjadi kesalahan dalam memformat respons."

    def parse_informal_indonesian(self, text: str) -> str:
        """Convert informal Indonesian to formal command format"""
        # Dictionary of informal to formal word mappings
        informal_dict = {
            "catet": "catat",
            "duit": "uang",
            "keluar": "pengeluaran",
            "masuk": "pemasukan",
            "buat": "untuk",
            "dr": "dari",
            "utk": "untuk",
            "rb": "ribu",
            "jt": "juta",
            "bln": "bulan",
            "mgg": "minggu",
            "thn": "tahun"
        }

        # Convert numbers with k/m suffix
        text = re.sub(r'(\d+)k\b', lambda m: str(int(m.group(1)) * 1000), text)
        text = re.sub(r'(\d+)m\b', lambda m: str(int(m.group(1)) * 1000000), text)

        # Replace informal words with formal ones
        for informal, formal in informal_dict.items():
            text = re.sub(r'\b' + informal + r'\b', formal, text)

        return text

# Create global message handler instance
message_handler = MessageHandler()
