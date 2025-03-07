from uuid import uuid4

from datetime import datetime

from db.connector import Base
from sqlalchemy import Column, String


class UserModel(Base):
    __tablename__ = "users"

    public_key = Column(String, primary_key=True, nullable=False)
    created_at = Column(String, server_default=datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
    updated_at = Column(String, server_default=datetime.now().strftime("%m-%d-%Y %H:%M:%S"), onupdate=datetime.now().strftime("%m-%d-%Y %H:%M:%S"))


class UserSessionModel(Base):
    __tablename__ = "users_sessions"

    public_key = Column(String, primary_key=True, nullable=False)
    jwt = Column(String, nullable=True)
    jwt_secret = Column(String, nullable=True)

    signed_message = Column(String, nullable=True)

    csrf_token = Column(String, nullable=False, default=str(uuid4()))

    created_at = Column(String, server_default=datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
    updated_at = Column(String, server_default=datetime.now().strftime("%m-%d-%Y %H:%M:%S"), onupdate=datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
