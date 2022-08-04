from sqlalchemy import Column, Integer, String, JSON, ForeignKey, TIMESTAMP, MetaData
from core.models.database import Base

metadata = MetaData()


class Employers(Base):
    """
    Структура БД:
    <код запроса>
    <имя сохраненного файла>
    <дата / время регистрации>
    """
    __tablename__ = 'employers'
    id_emp = Column(Integer, primary_key=True, autoincrement=True)
    role_emp = Column(String(5), nullable=False)
    resume_emp = Column(JSON)


class AdminToken(Base):
    """
    Структура БД:
    <код запроса>
    <имя сохраненного файла>
    <дата / время регистрации>
    """
    __tablename__ = 'tokens'
    # admin_id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey("employers.id_emp", ondelete='CASCADE'),
                      primary_key=True, autoincrement=False)
    admin_token = Column(String(255), nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
