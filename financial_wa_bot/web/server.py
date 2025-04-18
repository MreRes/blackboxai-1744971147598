from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from database.db_manager import db_manager
from features.financial_processor import financial_processor
from .websocket import WebSocketManager

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Financial Planner Dashboard")

# Mount static files
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="dashboard/templates")

# Initialize WebSocket manager
websocket_manager = WebSocketManager()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render dashboard homepage"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, user_id: int):
    """Render user dashboard"""
    try:
        # Get user data
        user = await db_manager.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get financial data
        balance = await financial_processor.get_balance(user_id)
        budget_status = await self.check_budget_status(user_id)
        insights = await financial_processor.get_financial_insights(user_id)
        
        return templates.TemplateResponse(
            "dashboard/main.html",
            {
                "request": request,
                "user": user,
                "balance": balance,
                "budget_status": budget_status,
                "insights": insights
            }
        )
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time updates"""
    try:
        await websocket_manager.connect(websocket, user_id)
        while True:
            try:
                # Wait for messages (can be used for user interactions)
                data = await websocket.receive_text()
                
                # Process any websocket messages here
                # For now, we'll just echo back
                await websocket_manager.send_personal_message(
                    f"Message received: {data}",
                    websocket
                )
            except WebSocketDisconnect:
                websocket_manager.disconnect(websocket, user_id)
                break
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in websocket_manager.active_connections:
            websocket_manager.disconnect(websocket, user_id)

# API Routes

@app.get("/api/transactions/{user_id}")
async def get_transactions(
    user_id: int,
    limit: Optional[int] = 10
) -> List[Dict[str, Any]]:
    """Get user transactions"""
    try:
        transactions = await db_manager.get_user_transactions(user_id, limit)
        return [
            {
                "id": t.id,
                "type": t.type.value,
                "amount": t.amount,
                "category": t.category,
                "description": t.description,
                "date": t.date.isoformat()
            }
            for t in transactions
        ]
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/balance/{user_id}")
async def get_balance(user_id: int) -> Dict[str, float]:
    """Get user balance"""
    try:
        return await financial_processor.get_balance(user_id)
    except Exception as e:
        logger.error(f"Error getting balance: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/budget/{user_id}")
async def get_budget_status(user_id: int) -> Dict[str, Any]:
    """Get user budget status"""
    try:
        return await financial_processor.check_budget_status(user_id)
    except Exception as e:
        logger.error(f"Error getting budget status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/report/{user_id}")
async def get_report(
    user_id: int,
    period: str = "monthly"
) -> Dict[str, Any]:
    """Get financial report"""
    try:
        return await financial_processor.generate_report(user_id, period)
    except Exception as e:
        logger.error(f"Error getting report: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/insights/{user_id}")
async def get_insights(user_id: int) -> List[Dict[str, Any]]:
    """Get financial insights"""
    try:
        return await financial_processor.get_financial_insights(user_id)
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/notifications/{user_id}")
async def get_notifications(
    user_id: int,
    unread_only: bool = False
) -> List[Dict[str, Any]]:
    """Get user notifications"""
    try:
        notifications = await db_manager.get_user_notifications(user_id, unread_only)
        return [
            {
                "id": n.id,
                "type": n.type,
                "message": n.message,
                "is_read": bool(n.is_read),
                "created_at": n.created_at.isoformat()
            }
            for n in notifications
        ]
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
