from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class Employers(BaseModel):
    id_emp: int
    role_emp: str
    resume_emp: Dict

    class Config:
        orm_mode = True


class AdminToken(BaseModel):
    admin_id: int
    admin_token: str
    updated_at: datetime

    class Config:
        orm_mode = True
