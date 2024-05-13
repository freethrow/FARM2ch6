from fastapi import FastAPI
from motor import motor_asyncio

from config import BaseConfig
from fastapi.middleware.cors import CORSMiddleware

from routers.cars import router as cars_router

settings = BaseConfig()

# define origins
origins = ["*"]


async def lifespan(app: FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]

    try:
        app.client.admin.command("ping")
        print("Pinged your deployment. You have successfully connected to MongoDB!")
        print("Mongo address:", settings.DB_URL)
    except Exception as e:
        print(e)
    yield
    app.client.close()


app = FastAPI(lifespan=lifespan)


# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cars_router, prefix="/cars", tags=["cars"])


@app.get("/")
async def get_root():
    return {"Message": "Root working!"}
