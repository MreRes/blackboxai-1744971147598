# WhatsApp Financial Planner Bot

A WhatsApp bot integrated with a web dashboard for personal financial management.

## Features

- 💬 WhatsApp Integration for financial tracking
- 📊 Interactive Web Dashboard
- 💰 Transaction Management
- 📈 Budget Tracking
- 📋 Financial Reports
- 🎯 Financial Goals
- 🔄 Real-time Updates via WebSocket

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- SQLite3
- WhatsApp account

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/financial-wa-bot.git
cd financial-wa-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```env
# Web Server Configuration
WEB_HOST=0.0.0.0
WEB_PORT=8000
DEBUG_MODE=True

# Database Configuration
DATABASE_URL=sqlite:///database/financial_bot.db

# Security Configuration
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Language Configuration
LANGUAGE_MODEL=indonesian

# Logging Configuration
LOG_LEVEL=INFO
```

## Running the Application

1. Initialize the database:
```bash
python -m financial_wa_bot.database.db_manager
```

2. Start the server:
```bash
cd financial_wa_bot
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

3. Access the dashboard at `http://localhost:8000`

## WhatsApp Bot Commands

The bot responds to the following commands:

### Expense Tracking
- "catat pengeluaran [jumlah] [kategori] [deskripsi]"
- "tambah pengeluaran [jumlah] [kategori] [deskripsi]"
- "keluar [jumlah] [kategori] [deskripsi]"

### Income Tracking
- "catat pemasukan [jumlah] [kategori] [deskripsi]"
- "tambah pemasukan [jumlah] [kategori] [deskripsi]"
- "masuk [jumlah] [kategori] [deskripsi]"

### Balance Check
- "cek saldo"
- "saldo"
- "balance"

### Reports
- "laporan"
- "report"

### Budget Management
- "atur budget [kategori] [jumlah]"
- "set budget [kategori] [jumlah]"

### Help
- "bantuan"
- "help"
- "tolong"

### Dashboard Access
- "buka dashboard"
- "dashboard"

## Project Structure

```
financial_wa_bot/
├── config/                 # Configuration files
├── core/                   # Core functionality
├── dashboard/             # Web dashboard
│   ├── static/           # Static files
│   └── templates/        # HTML templates
├── database/             # Database models and manager
├── features/             # Feature implementations
├── web/                  # Web server and API
└── main.py              # Application entry point
```

## Development

To contribute to the project:

1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Submit a pull request

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Security Considerations

1. Keep your `.env` file secure and never commit it to version control
2. Regularly update dependencies
3. Use strong passwords and secret keys
4. Monitor server logs for suspicious activity

## Troubleshooting

Common issues and solutions:

1. **Database Connection Error**
   - Check if SQLite is installed
   - Verify database path in `.env`
   - Ensure proper permissions

2. **WhatsApp Connection Issues**
   - Check internet connection
   - Verify WhatsApp account status
   - Ensure proper session management

3. **Server Won't Start**
   - Check if port 8000 is available
   - Verify Python version compatibility
   - Check log files for errors

## Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## License

This project is licensed under the MIT License - see the LICENSE file for details.
