import asyncio
import logging
from typing import Optional
from datetime import datetime
from typing import List, Dict, Any
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from config.settings import (
    WEB_HOST,
    WEB_PORT,
    DEBUG_MODE,
    LOG_LEVEL,
    LOG_FORMAT,
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_V1_PREFIX,
)

# Configure logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    debug=DEBUG_MODE,
)

# Mount static files
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Initialize templates with custom context
templates = Jinja2Templates(directory="dashboard/templates")
templates.env.globals["now"] = datetime.now

# Initialize WhatsApp client and WebSocket manager
wa_client: Optional[object] = None

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

async def init_whatsapp():
    """Initialize WhatsApp client"""
    try:
        # TODO: Implement WhatsApp client initialization
        logger.info("Initializing WhatsApp client...")
        pass
    except Exception as e:
        logger.error(f"Failed to initialize WhatsApp client: {e}")
        raise

async def init_websocket():
    """Initialize WebSocket server"""
    try:
        # TODO: Implement WebSocket server initialization
        logger.info("Initializing WebSocket server...")
        pass
    except Exception as e:
        logger.error(f"Failed to initialize WebSocket server: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Initialize WhatsApp client
        await init_whatsapp()
        
        # Initialize WebSocket server
        await init_websocket()
        
        logger.info("All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        # TODO: Implement cleanup logic
        logger.info("Shutting down services...")
        if wa_client:
            # Close WhatsApp client
            pass
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Mock data for financial goals
MOCK_GOALS = [
    {
        "id": 1,
        "name": "Dana Darurat",
        "target_amount": 50000000,
        "current_amount": 30000000,
        "deadline": "2024-12-31"
    },
    {
        "id": 2,
        "name": "Liburan",
        "target_amount": 15000000,
        "current_amount": 5000000,
        "deadline": "2024-06-30"
    }
]

@app.get("/api/goals/{user_id}")
async def get_financial_goals(user_id: str):
    """Get financial goals for a user"""
    return JSONResponse(content=MOCK_GOALS)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back the received message
            await manager.send_personal_message(data, client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# Route handlers for different pages
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render dashboard homepage"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": {"id": 1},  # Mock user for demo
            "balance": {
                "current_balance": 1000000,
                "total_income": 2000000,
                "total_expenses": 1000000
            },
            "transactions": [],
            "budget_status": {
                "budget_status": []
            },
            "expense_categories": [],
            "expense_amounts": [],
            "trend_dates": [],
            "income_trend": [],
            "expense_trend": []
        }
    )

@app.get("/transactions", response_class=HTMLResponse)
async def transactions(request: Request):
    """Render transactions page"""
    return templates.TemplateResponse(
        "transactions.html",
        {
            "request": request,
            "user": {"id": 1},
            "transactions": [
                {
                    "date": datetime.now(),
                    "category": "Makanan",
                    "description": "Makan Siang",
                    "amount": 50000,
                    "type": "expense"
                },
                {
                    "date": datetime.now(),
                    "category": "Gaji",
                    "description": "Gaji Bulanan",
                    "amount": 5000000,
                    "type": "income"
                }
            ]
        }
    )

@app.get("/budget", response_class=HTMLResponse)
async def budget(request: Request):
    """Render budget page"""
    return templates.TemplateResponse(
        "budget.html",
        {
            "request": request,
            "user": {"id": 1},
            "budgets": [
                {
                    "category": "Makanan",
                    "allocated": 2000000,
                    "spent": 1500000,
                    "remaining": 500000
                },
                {
                    "category": "Transport",
                    "allocated": 1000000,
                    "spent": 800000,
                    "remaining": 200000
                }
            ]
        }
    )

@app.get("/reports", response_class=HTMLResponse)
async def reports(request: Request):
    """Render reports page"""
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "user": {"id": 1},
            "monthly_summary": {
                "income": 5000000,
                "expenses": 3000000,
                "savings": 2000000
            },
            "expense_breakdown": [
                {"category": "Makanan", "amount": 1500000},
                {"category": "Transport", "amount": 800000},
                {"category": "Hiburan", "amount": 700000}
            ]
        }
    )

@app.get("/goals", response_class=HTMLResponse)
async def goals(request: Request):
    """Render financial goals page"""
    return templates.TemplateResponse(
        "goals.html",
        {
            "request": request,
            "user": {"id": 1},
            "goals": MOCK_GOALS
        }
    )

def run():
    """Run the application"""
    try:
        uvicorn.run(
            "main:app",
            host=WEB_HOST,
            port=WEB_PORT,
            reload=DEBUG_MODE,
            log_level=LOG_LEVEL.lower(),
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

if __name__ == "__main__":
    run()
