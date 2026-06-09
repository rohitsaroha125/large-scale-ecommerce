from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import text
import os
from dotenv import load_dotenv
from auth import create_access_token, hash_password, verify_password
from schemas import UserRegister, UserLogin
from models import Users

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

print(create_access_token({"name": "John Doe", "email": ""}))

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def startup():
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.post("/user/register")
async def register_user(user: UserRegister, session: SessionDep):
    findUser = session.exec(select(Users).where(Users.email == user.email)).first()
    if findUser:
        raise HTTPException(status_code=400, detail="User already exists")
    db_user = Users(name=user.name, email=user.email, password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"id": db_user.id, "email": db_user.email, "name": db_user.name}
        

@app.post("/user/login")
async def login_user(user: UserLogin, session: SessionDep):
    findUser = session.exec(select(Users).where(Users.email == user.email)).first()
    if not findUser or not verify_password(user.password, findUser.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_access_token({"name": findUser.name, "email": findUser.email})
    return {"access_token": token, "token_type": "bearer", "user": {"id": findUser.id, "email": findUser.email, "name": findUser.name}}