from fastapi import FastAPI
from app.routers import users, tasks
import app.database

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
