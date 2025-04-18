
Built by https://www.blackbox.ai

---

```markdown
# WhatsApp Financial Planner Bot

## Project Overview
WhatsApp Financial Planner Bot is a self-hosted solution built with Python that enables users to manage their financial activities through an unofficial WhatsApp gateway. The bot supports both formal and informal Indonesian language, allowing users to interactively record their expenses, income, and budget planning via simple commands. It also features a real-time web dashboard for comprehensive financial monitoring.

## Installation
To set up the project, follow these instructions:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/financial_wa_bot.git
   cd financial_wa_bot
   ```

2. **Set Up a Virtual Environment:**
   Make sure you have Python 3.8+ installed, and create a virtual environment.
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   Install the required packages using the following command:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure WhatsApp Gateway:**
   Modify the `config/settings.py` file to set up your WhatsApp gateway settings including credentials.

5. **Run the Bot:**
   Start the bot by executing:
   ```bash
   python main.py
   ```

## Usage
Once the bot is running, you can interact with it using the following commands via WhatsApp:

- Record an expense: `Catat pengeluaran 50000 untuk makan`
- Record an income: `Catat pemasukan 1000000 gaji`
- Check balance: `Cek saldo`
- View report: `Laporan bulanan`
- Set budget: `Atur budget 2000000 per bulan`
- Get tips: `Tips keuangan`
- Access dashboard: `Buka dashboard`

## Features
- **WhatsApp Integration:** Send and receive messages through WhatsApp.
- **Financial Management:** Record expenses and income, set budgets, and generate financial reports.
- **Natural Language Processing:** Supports conversational Indonesian for command recognition.
- **Real-Time Dashboard:** Interactive charts and graphs for monitoring financial status.
- **Budget Tracking:** Visual aids for budgets with alert notifications.
- **Report Generation:** PDF reports and financial insights.

## Dependencies
This project requires the following Python packages, which are included in `requirements.txt`:

- Python 3.8+
- `wa-automate-python`
- `SQLAlchemy`
- `python-dotenv`
- `nltk` (for language processing)
- `pandas` (for financial analysis)
- `pytest` (for testing)
- `FastAPI` (for web server)
- `uvicorn` (ASGI server)
- `websockets` (for real-time updates)
- `Jinja2` (for templating)
- `Chart.js` (for dashboard visualizations)
- `TailwindCSS` (for dashboard styling)

## Project Structure
The project is organized into several key directories:

```
financial_wa_bot/
├── config/               # Configuration settings.
│   ├── __init__.py
│   └── settings.py
├── core/                 # Core bot functionalities.
│   ├── __init__.py
│   ├── bot.py
│   ├── message_handler.py
│   └── whatsapp_client.py
├── features/             # Financial processing features.
│   ├── __init__.py
│   ├── financial_processor.py
│   ├── budget_manager.py
│   └── report_generator.py
├── database/             # Database models and managers.
│   ├── __init__.py
│   ├── models.py
│   └── db_manager.py
├── web/                  # Web server and API.
│   ├── __init__.py
│   ├── server.py
│   ├── websocket.py
│   └── api/
│       ├── __init__.py
│       └── routes.py
├── dashboard/            # Dashboards for visualization.
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/
│       ├── index.html
│       ├── components/
│       └── layouts/
├── utils/                # Utility functions for the bot.
│   ├── __init__.py
│   ├── language_processor.py
│   └── helpers.py
├── tests/                # Automated tests for the project.
│   └── __init__.py
├── requirements.txt      # Project dependencies.
├── README.md             # Project overview and documentation.
└── main.py               # Entry point for the bot.
```

## Next Steps
For further development, consider implementing advanced features, conducting testing, and optimizing the user interaction flow. 

Feel free to contribute or provide feedback! 
```