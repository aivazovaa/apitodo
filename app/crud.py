from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()
    
def update_task(db: Session, task_id: int, task_data: schemas.TaskCreate, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task or task.owner_id != user_id:
        return None
    for field, value in task_data.dict().items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task or task.owner_id != user_id:
        return False
    db.delete(task)
    db.commit()
    return True

def grant_permission(db: Session, task_id: int, target_user_id: int, can_read: bool=False, can_update: bool=False):
    perm = db.query(models.TaskPermission).filter_by(task_id=task_id, user_id=target_user_id).first()
    if not perm:
        perm = models.TaskPermission(task_id=task_id, user_id=target_user_id,
                                     can_read=can_read, can_update=can_update)
        db.add(perm)
    else:
        perm.can_read = can_read or perm.can_read
        perm.can_update = can_update or perm.can_update
    db.commit()
    return perm

def revoke_permission(db: Session, task_id: int, target_user_id: int):
    perm = db.query(models.TaskPermission).filter_by(task_id=task_id, user_id=target_user_id).first()
    if not perm:
        return False
    db.delete(perm)
    db.commit()
    return True

