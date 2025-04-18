# Setting Up WhatsApp Financial Planner Bot

## Quick Start Guide

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
Create `.env` file with:
```env
# Web Server
WEB_HOST=0.0.0.0
WEB_PORT=8000
DEBUG_MODE=True

# Database
DATABASE_URL=sqlite:///database/financial_bot.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# WhatsApp
WHATSAPP_CONFIG_HEADLESS=true
WHATSAPP_CONFIG_QR_TIMEOUT=60
WHATSAPP_CONFIG_AUTH_TIMEOUT=60
```

3. **Install Chrome/Chromium**
```bash
# Ubuntu/Debian
sudo apt-get install -y chromium-browser chromium-chromedriver

# CentOS/RHEL
sudo yum install -y chromium chromium-headless chromedriver

# macOS
brew install --cask chromium
```

4. **Start the Server**
```bash
cd financial_wa_bot
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

5. **Connect WhatsApp**
- Run the server
- Scan QR code with WhatsApp mobile app
- Wait for connection confirmation

## Available Commands

### Expense Recording
```
catat pengeluaran 50000 untuk makan
tambah pengeluaran 30000 transportasi
keluar 100000 belanja
```

### Income Recording
```
catat pemasukan 5000000 dari gaji
tambah pemasukan 1000000 bonus
masuk 500000 freelance
```

### Other Commands
- Check balance: `cek saldo`
- View report: `laporan`
- Set budget: `atur budget makan 2000000`
- Get help: `bantuan`
- Open dashboard: `buka dashboard`

## Troubleshooting

1. **WhatsApp Connection Issues**
- Clear WhatsApp Web session
- Restart Chrome/Chromium
- Check internet connection
- Verify mobile WhatsApp is online

2. **Server Issues**
- Check port 8000 availability
- Verify all dependencies installed
- Check log files for errors

For more details, see the full README.md
