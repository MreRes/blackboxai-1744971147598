from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from datetime import datetime

from database.db_manager import db_manager
from features.financial_processor import financial_processor

router = APIRouter(prefix="/api/v1")

@router.get("/transactions/{user_id}")
async def get_transactions(
    user_id: int,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """Get user transactions with pagination"""
    try:
        transactions = await db_manager.get_user_transactions(user_id, limit)
        total = await db_manager.get_transaction_count(user_id)
        
        return {
            "total": total,
            "transactions": [
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
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/balance/{user_id}")
async def get_balance(user_id: int) -> Dict[str, float]:
    """Get user's current balance"""
    try:
        return await financial_processor.get_balance(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/budget/{user_id}")
async def get_budget_status(user_id: int) -> Dict[str, Any]:
    """Get user's budget status"""
    try:
        return await financial_processor.check_budget_status(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{user_id}")
async def get_financial_report(
    user_id: int,
    period: str = "monthly"
) -> Dict[str, Any]:
    """Get financial report for specified period"""
    try:
        return await financial_processor.generate_report(user_id, period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights/{user_id}")
async def get_financial_insights(user_id: int) -> List[Dict[str, Any]]:
    """Get financial insights and recommendations"""
    try:
        return await financial_processor.get_financial_insights(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/notifications/{user_id}")
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
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/notifications/{notification_id}/read")
async def mark_notification_read(notification_id: int) -> Dict[str, str]:
    """Mark notification as read"""
    try:
        await db_manager.mark_notification_read(notification_id)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_categories() -> Dict[str, List[str]]:
    """Get available transaction categories"""
    from config.settings import EXPENSE_CATEGORIES, INCOME_CATEGORIES
    return {
        "expense": EXPENSE_CATEGORIES,
        "income": INCOME_CATEGORIES
    }

@router.get("/stats/{user_id}")
async def get_statistics(
    user_id: int,
    period: str = "monthly"
) -> Dict[str, Any]:
    """Get financial statistics"""
    try:
        report = await financial_processor.generate_report(user_id, period)
        budget = await financial_processor.check_budget_status(user_id)
        balance = await financial_processor.get_balance(user_id)
        
        return {
            "report": report,
            "budget": budget,
            "balance": balance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
