import uvicorn

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from db.connector import Base, engine  # noqa

from authentication.api.authentication import authentication_routers  # noqa
from user.api.users import user_routers  # noqa

origins = [
    "*"
]

app = FastAPI(
    title="Hypes Zone Backend",
    description="API Backend chat Hypes.zone",
    version="1.0.0",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )
    ]
)

Base.metadata.create_all(bind=engine)

app.include_router(authentication_routers)
app.include_router(user_routers)

@app.get("/")
async def get():
    return "Go away!"


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
