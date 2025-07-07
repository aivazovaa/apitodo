from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user

def get_db_session():
    return next(get_db())

def get_active_user(current_user=Depends(get_current_user)):
    return current_user
