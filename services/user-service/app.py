from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000", "localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. DATABASE CONFIGURATION
# ==========================================
# Replace with your actual PostgreSQL connection string
DATABASE_URL = os.getenv("DATABASE_URL")

# The engine handles connection pools and executes raw SQL queries under the hood
engine = create_engine(DATABASE_URL, echo=True)

@app.on_event("startup")
def startup():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

@app.get("/users")
async def get_users():
    return [
        {"id": 1, "name": "John Doe", "email": "john.doe@example.com"},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@example.com"},
    ]