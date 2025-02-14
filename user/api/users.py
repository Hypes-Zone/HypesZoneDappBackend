from fastapi import APIRouter, status
from fastapi import Depends

from sqlalchemy.orm import Session

from db.connector import get_db

from user.services import user_services

user_routers = APIRouter()


@user_routers.post("/users/", tags=["users"], status_code=status.HTTP_200_OK)
async def upsert_user(data: dict[str, str], db: Session = Depends(get_db)):
    public_key = data["public_key"]
    if not user_services.get_user_if_exists(public_key=public_key, db=db):
        user_services.create_user(public_key=public_key, db=db)

    return
