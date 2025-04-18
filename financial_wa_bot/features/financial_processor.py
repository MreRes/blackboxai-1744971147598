from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import pandas as pd
from sqlalchemy import func

from database.db_manager import db_manager
from database.models import Transaction, Budget, TransactionType
from config.settings import EXPENSE_CATEGORIES, INCOME_CATEGORIES

logger = logging.getLogger(__name__)

class FinancialProcessor:
    async def process_transaction(self, user_id: int, transaction_data: Dict[str, Any]) -> Transaction:
        """Process and record a new transaction"""
        try:
            # Create transaction
            transaction = await db_manager.create_transaction(user_id, transaction_data)
            
            # Check budget alerts
            if transaction.type == TransactionType.EXPENSE:
                await self._check_budget_alerts(user_id, transaction)
            
            return transaction
        except Exception as e:
            logger.error(f"Error processing transaction: {e}")
            raise

    async def get_balance(self, user_id: int) -> Dict[str, float]:
        """Calculate user's current balance"""
        try:
            db = db_manager.get_db()
            
            # Calculate total income
            total_income = db.query(func.sum(Transaction.amount))\
                .filter(Transaction.user_id == user_id,
                       Transaction.type == TransactionType.INCOME)\
                .scalar() or 0.0

            # Calculate total expenses
            total_expenses = db.query(func.sum(Transaction.amount))\
                .filter(Transaction.user_id == user_id,
                       Transaction.type == TransactionType.EXPENSE)\
                .scalar() or 0.0

            return {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "current_balance": total_income - total_expenses
            }
        except Exception as e:
            logger.error(f"Error calculating balance: {e}")
            raise

    async def generate_report(self, user_id: int, period: str = "monthly") -> Dict[str, Any]:
        """Generate financial report for specified period"""
        try:
            # Get date range based on period
            start_date = self._get_period_start_date(period)
            
            # Get transactions for the period
            transactions = await db_manager.get_user_transactions(user_id)
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame([{
                'amount': t.amount,
                'type': t.type.value,
                'category': t.category,
                'date': t.date
            } for t in transactions])

            if df.empty:
                return self._generate_empty_report()

            # Filter by date
            df = df[df['date'] >= start_date]

            # Calculate summaries
            summary = {
                "period": period,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": datetime.now().strftime("%Y-%m-%d"),
                "total_income": float(df[df['type'] == 'income']['amount'].sum()),
                "total_expenses": float(df[df['type'] == 'expense']['amount'].sum()),
                "categories": {
                    "income": self._calculate_category_summary(df, 'income'),
                    "expense": self._calculate_category_summary(df, 'expense')
                },
                "daily_summary": self._calculate_daily_summary(df)
            }

            return summary
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise

    async def set_budget(self, user_id: int, budget_data: Dict[str, Any]) -> Budget:
        """Set or update budget"""
        try:
            # Calculate period dates
            period = budget_data.get('period', 'monthly')
            start_date = datetime.now()
            end_date = self._calculate_period_end_date(start_date, period)

            budget_info = {
                "user_id": user_id,
                "amount": budget_data['amount'],
                "period_start": start_date,
                "period_end": end_date,
                "category": budget_data.get('category', 'all')
            }

            return await db_manager.create_budget(budget_info)
        except Exception as e:
            logger.error(f"Error setting budget: {e}")
            raise

    async def check_budget_status(self, user_id: int) -> Dict[str, Any]:
        """Check current budget status"""
        try:
            # Get active budgets
            budgets = await db_manager.get_user_budgets(user_id)
            
            status = []
            for budget in budgets:
                # Calculate spent amount
                spent = await self._calculate_spent_amount(
                    user_id, 
                    budget.category,
                    budget.period_start,
                    budget.period_end
                )
                
                remaining = budget.amount - spent
                percentage_used = (spent / budget.amount) * 100 if budget.amount > 0 else 0

                status.append({
                    "category": budget.category,
                    "budget_amount": budget.amount,
                    "spent_amount": spent,
                    "remaining_amount": remaining,
                    "percentage_used": percentage_used,
                    "period_start": budget.period_start.strftime("%Y-%m-%d"),
                    "period_end": budget.period_end.strftime("%Y-%m-%d")
                })

            return {"budget_status": status}
        except Exception as e:
            logger.error(f"Error checking budget status: {e}")
            raise

    async def get_financial_insights(self, user_id: int) -> List[Dict[str, Any]]:
        """Generate financial insights based on user's data"""
        try:
            insights = []
            
            # Get user's financial data
            balance = await self.get_balance(user_id)
            budget_status = await self.check_budget_status(user_id)
            
            # Generate insights based on the data
            if balance["current_balance"] < 0:
                insights.append({
                    "type": "warning",
                    "message": "Saldo Anda negatif. Pertimbangkan untuk mengurangi pengeluaran."
                })

            for status in budget_status["budget_status"]:
                if status["percentage_used"] > 80:
                    insights.append({
                        "type": "alert",
                        "message": f"Budget untuk {status['category']} sudah terpakai {status['percentage_used']:.1f}%"
                    })

            # Add general financial tips
            insights.append({
                "type": "tip",
                "message": "Simpan minimal 20% dari pendapatan Anda untuk dana darurat."
            })

            return insights
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            raise

    def _get_period_start_date(self, period: str) -> datetime:
        """Get start date based on period"""
        now = datetime.now()
        if period == "daily":
            return now - timedelta(days=1)
        elif period == "weekly":
            return now - timedelta(weeks=1)
        elif period == "monthly":
            return now - timedelta(days=30)
        elif period == "yearly":
            return now - timedelta(days=365)
        else:
            return now - timedelta(days=30)  # Default to monthly

    def _calculate_period_end_date(self, start_date: datetime, period: str) -> datetime:
        """Calculate end date based on period"""
        if period == "daily":
            return start_date + timedelta(days=1)
        elif period == "weekly":
            return start_date + timedelta(weeks=1)
        elif period == "monthly":
            return start_date + timedelta(days=30)
        elif period == "yearly":
            return start_date + timedelta(days=365)
        else:
            return start_date + timedelta(days=30)  # Default to monthly

    def _calculate_category_summary(self, df: pd.DataFrame, trans_type: str) -> Dict[str, float]:
        """Calculate summary by category for given transaction type"""
        type_df = df[df['type'] == trans_type]
        return type_df.groupby('category')['amount'].sum().to_dict()

    def _calculate_daily_summary(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Calculate daily transaction summary"""
        daily = df.groupby(['date', 'type'])['amount'].sum().unstack(fill_value=0)
        return [
            {
                "date": date.strftime("%Y-%m-%d"),
                "income": float(row.get('income', 0)),
                "expense": float(row.get('expense', 0))
            }
            for date, row in daily.iterrows()
        ]

    def _generate_empty_report(self) -> Dict[str, Any]:
        """Generate empty report structure"""
        return {
            "period": "monthly",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
            "total_income": 0.0,
            "total_expenses": 0.0,
            "categories": {
                "income": {},
                "expense": {}
            },
            "daily_summary": []
        }

    async def _calculate_spent_amount(
        self, 
        user_id: int, 
        category: str,
        start_date: datetime,
        end_date: datetime
    ) -> float:
        """Calculate amount spent for a specific category and period"""
        try:
            db = db_manager.get_db()
            query = db.query(func.sum(Transaction.amount))\
                .filter(
                    Transaction.user_id == user_id,
                    Transaction.type == TransactionType.EXPENSE,
                    Transaction.date.between(start_date, end_date)
                )
            
            if category != 'all':
                query = query.filter(Transaction.category == category)
            
            return query.scalar() or 0.0
        except Exception as e:
            logger.error(f"Error calculating spent amount: {e}")
            raise

    async def _check_budget_alerts(self, user_id: int, transaction: Transaction) -> None:
        """Check if transaction triggers any budget alerts"""
        try:
            # Get active budgets
            budgets = await db_manager.get_user_budgets(user_id)
            
            for budget in budgets:
                if budget.category in ['all', transaction.category]:
                    spent = await self._calculate_spent_amount(
                        user_id,
                        budget.category,
                        budget.period_start,
                        budget.period_end
                    )
                    
                    # Create alert if over 80% of budget
                    if spent >= (budget.amount * 0.8):
                        await db_manager.create_notification({
                            "user_id": user_id,
                            "type": "budget_alert",
                            "message": f"Anda telah menggunakan {(spent/budget.amount)*100:.1f}% "
                                     f"dari budget {budget.category}"
                        })
        except Exception as e:
            logger.error(f"Error checking budget alerts: {e}")
            # Don't raise the error to prevent transaction failure
            pass

# Create global financial processor instance
financial_processor = FinancialProcessor()
