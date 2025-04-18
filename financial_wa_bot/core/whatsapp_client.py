from typing import Optional, Dict, Any
import logging
from wa_automate_python import WhatsApp
from datetime import datetime

from config.settings import WHATSAPP_CONFIG, COMMAND_PREFIXES
from database.db_manager import db_manager

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self):
        self.client: Optional[WhatsApp] = None
        self.is_ready: bool = False

    async def initialize(self) -> None:
        """Initialize WhatsApp client"""
        try:
            # Initialize WhatsApp client with configuration
            self.client = WhatsApp(**WHATSAPP_CONFIG)
            self.is_ready = True
            logger.info("WhatsApp client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WhatsApp client: {e}")
            raise

    async def process_message(self, message: Dict[str, Any]) -> None:
        """Process incoming WhatsApp message"""
        try:
            if not message or 'text' not in message:
                return

            # Extract message details
            phone_number = message.get('from', '')
            text = message.get('text', '').lower().strip()
            
            # Get or create user
            user = await db_manager.get_user_by_phone(phone_number)
            if not user:
                user = await db_manager.create_user(phone_number)

            # Process commands
            if any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['expense']):
                await self._handle_expense(user, text)
            elif any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['income']):
                await self._handle_income(user, text)
            elif any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['balance']):
                await self._handle_balance(user)
            elif any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['report']):
                await self._handle_report(user)
            elif any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['budget']):
                await self._handle_budget(user, text)
            elif any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['help']):
                await self._handle_help(user)
            elif any(text.startswith(prefix) for prefix in COMMAND_PREFIXES['dashboard']):
                await self._handle_dashboard(user)
            else:
                await self._handle_unknown_command(user)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await self.send_message(phone_number, "Maaf, terjadi kesalahan. Silakan coba lagi.")

    async def send_message(self, to: str, message: str) -> None:
        """Send WhatsApp message"""
        try:
            if not self.is_ready or not self.client:
                raise Exception("WhatsApp client not initialized")
            
            await self.client.send_message(to, message)
            logger.info(f"Message sent to {to}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    async def _handle_expense(self, user: Any, text: str) -> None:
        """Handle expense recording command"""
        try:
            # TODO: Implement expense handling logic
            # Format: "catat pengeluaran <amount> untuk <category>"
            await self.send_message(user.phone_number, "Fitur pencatatan pengeluaran akan segera tersedia.")
        except Exception as e:
            logger.error(f"Error handling expense: {e}")
            raise

    async def _handle_income(self, user: Any, text: str) -> None:
        """Handle income recording command"""
        try:
            # TODO: Implement income handling logic
            # Format: "catat pemasukan <amount> dari <category>"
            await self.send_message(user.phone_number, "Fitur pencatatan pemasukan akan segera tersedia.")
        except Exception as e:
            logger.error(f"Error handling income: {e}")
            raise

    async def _handle_balance(self, user: Any) -> None:
        """Handle balance check command"""
        try:
            # TODO: Implement balance checking logic
            await self.send_message(user.phone_number, "Fitur cek saldo akan segera tersedia.")
        except Exception as e:
            logger.error(f"Error handling balance check: {e}")
            raise

    async def _handle_report(self, user: Any) -> None:
        """Handle report generation command"""
        try:
            # TODO: Implement report generation logic
            await self.send_message(user.phone_number, "Fitur laporan keuangan akan segera tersedia.")
        except Exception as e:
            logger.error(f"Error handling report: {e}")
            raise

    async def _handle_budget(self, user: Any, text: str) -> None:
        """Handle budget setting command"""
        try:
            # TODO: Implement budget setting logic
            # Format: "atur budget <amount> per <period>"
            await self.send_message(user.phone_number, "Fitur pengaturan budget akan segera tersedia.")
        except Exception as e:
            logger.error(f"Error handling budget: {e}")
            raise

    async def _handle_help(self, user: Any) -> None:
        """Handle help command"""
        help_message = """
*Financial Planner Bot - Bantuan*

Perintah yang tersedia:
1. Catat pengeluaran: "catat pengeluaran <jumlah> untuk <kategori>"
2. Catat pemasukan: "catat pemasukan <jumlah> dari <kategori>"
3. Cek saldo: "cek saldo"
4. Laporan: "laporan"
5. Atur budget: "atur budget <jumlah> per <periode>"
6. Buka dashboard: "buka dashboard"

Contoh:
- catat pengeluaran 50000 untuk makan
- catat pemasukan 1000000 dari gaji
- cek saldo
- laporan bulanan
- atur budget 2000000 per bulan
"""
        try:
            await self.send_message(user.phone_number, help_message)
        except Exception as e:
            logger.error(f"Error handling help: {e}")
            raise

    async def _handle_dashboard(self, user: Any) -> None:
        """Handle dashboard access command"""
        try:
            # TODO: Implement dashboard access logic
            dashboard_url = f"http://localhost:8000/dashboard?user={user.id}"
            message = f"Silakan akses dashboard Anda di:\n{dashboard_url}"
            await self.send_message(user.phone_number, message)
        except Exception as e:
            logger.error(f"Error handling dashboard: {e}")
            raise

    async def _handle_unknown_command(self, user: Any) -> None:
        """Handle unknown command"""
        message = "Maaf, perintah tidak dikenali. Ketik 'bantuan' untuk melihat daftar perintah yang tersedia."
        try:
            await self.send_message(user.phone_number, message)
        except Exception as e:
            logger.error(f"Error handling unknown command: {e}")
            raise

# Create global WhatsApp client instance
wa_client = WhatsAppClient()
