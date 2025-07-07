from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.deps import get_active_user, get_db_session

router = APIRouter()

@router.post("/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db_session), user=Depends(get_active_user)):
    return crud.create_task(db, task, user.id)

@router.get("/", response_model=List[schemas.TaskOut])
def read_tasks(db: Session = Depends(get_db_session), user=Depends(get_active_user)):
    return crud.get_tasks(db, user.id)

@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db_session), user=Depends(get_active_user)):
    db_task = crud.get_task(db, task_id)
    if not db_task or db_task.owner_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int,
                task: schemas.TaskUpdate,
                db: Session = Depends(get_db_session),
                user=Depends(get_active_user)):
    updated = crud.update_task(db, task_id, task, user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or no rights")
    return updated

@router.delete("/{task_id}")
def delete_task(task_id: int,
                db: Session = Depends(get_db_session),
                user=Depends(get_active_user)):
    success = crud.delete_task(db, task_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found or no rights")
    return {"detail": "Task deleted"}

@router.post("/{task_id}/permissions")
def grant_task_permission(task_id: int,
                          perm_in: schemas.PermissionIn,
                          db: Session = Depends(get_db_session),
                          user=Depends(get_active_user)):
    # только создатель может выдавать
    task = crud.get_task(db, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not task owner")
    perm = crud.grant_permission(db, task_id, perm_in.user_id,
                                 can_read=perm_in.can_read,
                                 can_update=perm_in.can_update)
    return {"detail": "Permission granted", "permission": perm}

@router.delete("/{task_id}/permissions/{target_user_id}")
def revoke_task_permission(task_id: int,
                           target_user_id: int,
                           db: Session = Depends(get_db_session),
                           user=Depends(get_active_user)):
    task = crud.get_task(db, task_id)
    if not task or task.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not task owner")
    success = crud.revoke_permission(db, task_id, target_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"detail": "Permission revoked"}
