from sqlalchemy import create_engine
from app.database.connection import Base, engine
from app.database.models import Workflow, Document, Component, ChatSession, ChatMessage

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")






