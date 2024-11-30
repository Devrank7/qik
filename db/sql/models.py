import datetime

from sqlalchemy import Column, Integer, DateTime, BigInteger

from db.sql.connect import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, unique=True, index=True, nullable=False)
    expired_date = Column(DateTime, nullable=False, default=datetime.datetime.now())
