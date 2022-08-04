# import uvicorn
from fastapi import FastAPI, status, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from core.models import database, model
from enum import Enum
from datetime import datetime
from secrets import token_hex
import json


app = FastAPI()


class AccessUsers(str, Enum):
    user = "user"
    admin = "admin"


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/add/', status_code=status.HTTP_200_OK)
async def add_account(access_right: AccessUsers, data: UploadFile, db: Session = Depends(get_db)):
    content = await data.read()
    content = content.decode("utf-8")
    content = json.loads(content)
    new_employer = model.Employers(
        role_emp=access_right,
        resume_emp=content
    )
    db.add(new_employer)
    db.commit()
    if access_right == "admin":
        admin_id = db.query(model.Employers).order_by(model.Employers.id_emp.desc()).first().id_emp
        new_admin_token = model.AdminToken(
            admin_id=admin_id,
            admin_token=token_hex(16),
            updated_at=datetime.now()
        )
        db.add(new_admin_token)
        db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": "Successfully uploaded"}


@app.put('/update-token/{id_in}', status_code=status.HTTP_200_OK)
async def update_token(id_in: int, db: Session = Depends(get_db)):
    role_request = db.query(model.Employers).filter(model.Employers.id_emp == id_in).one().role_emp
    if role_request == 'admin':
        db.query(model.AdminToken).filter(model.AdminToken.admin_id == id_in).update({"admin_token": token_hex(16)})
        db.commit()
    return {"status_code": status.HTTP_200_OK}


@app.get('/show-employers/', status_code=status.HTTP_200_OK)
async def show_employers(db: Session = Depends(get_db)):
    out = db.query(*[c for c in model.Employers.__table__.c if c.name != 'resume_emp'])
    return out


@app.get('/show-resume/{id_in}', status_code=status.HTTP_200_OK)
async def show_resume(id_in: int, db: Session = Depends(get_db)):
    out = db.query(model.Employers).filter(model.Employers.id_emp == id_in).one().resume_emp
    return out


@app.get('/show-token/{id_in}', status_code=status.HTTP_200_OK)
async def show_token(id_in: int, db: Session = Depends(get_db)):
    role_request = db.query(model.Employers).filter(model.Employers.id_emp == id_in).one().role_emp
    if role_request == 'admin':
        out = db.query(model.AdminToken).filter(model.AdminToken.admin_id == id_in).one().admin_token
        return out
    return "Fuck yourself"


@app.delete('/remove/{id_in}', status_code=status.HTTP_200_OK)
async def remove_account(id_in: int, db: Session = Depends(get_db)):
    role_request = db.query(model.Employers).filter(model.Employers.id_emp == id_in).one().role_emp
    if role_request == 'admin':
        admin_delete = db.query(model.AdminToken).filter(model.AdminToken.admin_id == id_in).delete()
        if not admin_delete:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="resource not found")
    employer_delete = db.query(model.Employers).filter(model.Employers.id_emp == id_in).delete()
    if not employer_delete:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="resource not found")
    db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": "Successfully deleted"}
