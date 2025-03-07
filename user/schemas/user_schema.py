from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    public_key: str
    created_at: str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    updated_at: str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")


class UserSession(BaseModel):
    public_key: str
    jwt: str
    signed_message: UUID
    csrf_token: str
    created_at: str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    updated_at: str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
