from typing import Optional, List, Any, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from config.settings import DATABASE_URL
from .models import Base, User, Transaction, Budget, Notification, FinancialGoal, FinancialTip

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def init_db(self) -> None:
        """Initialize the database, creating all tables."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database initialized successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def get_db(self) -> Session:
        """Get database session."""
        db = self.SessionLocal()
        try:
            return db
        except:
            db.close()
            raise

    async def create_user(self, phone_number: str, name: Optional[str] = None) -> User:
        """Create a new user."""
        db = self.get_db()
        try:
            user = User(phone_number=phone_number, name=name)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating user: {e}")
            raise
        finally:
            db.close()

    async def get_user_by_phone(self, phone_number: str) -> Optional[User]:
        """Get user by phone number."""
        db = self.get_db()
        try:
            return db.query(User).filter(User.phone_number == phone_number).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting user: {e}")
            raise
        finally:
            db.close()

    async def create_transaction(self, user_id: int, transaction_data: Dict[str, Any]) -> Transaction:
        """Create a new transaction."""
        db = self.get_db()
        try:
            transaction = Transaction(user_id=user_id, **transaction_data)
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            return transaction
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating transaction: {e}")
            raise
        finally:
            db.close()

    async def get_user_transactions(self, user_id: int, limit: int = 10) -> List[Transaction]:
        """Get user's transactions."""
        db = self.get_db()
        try:
            return db.query(Transaction)\
                    .filter(Transaction.user_id == user_id)\
                    .order_by(Transaction.date.desc())\
                    .limit(limit)\
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting transactions: {e}")
            raise
        finally:
            db.close()

    async def create_budget(self, budget_data: Dict[str, Any]) -> Budget:
        """Create a new budget."""
        db = self.get_db()
        try:
            budget = Budget(**budget_data)
            db.add(budget)
            db.commit()
            db.refresh(budget)
            return budget
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating budget: {e}")
            raise
        finally:
            db.close()

    async def get_user_budgets(self, user_id: int) -> List[Budget]:
        """Get user's budgets."""
        db = self.get_db()
        try:
            return db.query(Budget)\
                    .filter(Budget.user_id == user_id)\
                    .all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting budgets: {e}")
            raise
        finally:
            db.close()

    async def create_notification(self, notification_data: Dict[str, Any]) -> Notification:
        """Create a new notification."""
        db = self.get_db()
        try:
            notification = Notification(**notification_data)
            db.add(notification)
            db.commit()
            db.refresh(notification)
            return notification
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating notification: {e}")
            raise
        finally:
            db.close()

    async def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Notification]:
        """Get user's notifications."""
        db = self.get_db()
        try:
            query = db.query(Notification)\
                     .filter(Notification.user_id == user_id)
            if unread_only:
                query = query.filter(Notification.is_read == 0)
            return query.order_by(Notification.created_at.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting notifications: {e}")
            raise
        finally:
            db.close()

    async def create_financial_goal(self, goal_data: Dict[str, Any]) -> FinancialGoal:
        """Create a new financial goal."""
        db = self.get_db()
        try:
            goal = FinancialGoal(**goal_data)
            db.add(goal)
            db.commit()
            db.refresh(goal)
            return goal
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error creating financial goal: {e}")
            raise
        finally:
            db.close()

    async def get_financial_tips(self, category: Optional[str] = None) -> List[FinancialTip]:
        """Get financial tips, optionally filtered by category."""
        db = self.get_db()
        try:
            query = db.query(FinancialTip)
            if category:
                query = query.filter(FinancialTip.category == category)
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting financial tips: {e}")
            raise
        finally:
            db.close()

# Create global database manager instance
db_manager = DatabaseManager()
