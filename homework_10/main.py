from fastapi import FastAPI, Depends
import uvicorn

from contextlib import asynccontextmanager

from api.routers import default_router, users_router, quizes_router, questions_router
from models.database import DataRepository as dr


@asynccontextmanager
async def lifespan(app: FastAPI):
    await dr.delete_table()
    await dr.create_table()
    await dr.add_test_data()
    print("------Bases build-------------")

    yield
    await dr.delete_table()
    print("-------------Bases drooped------------")


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(users_router)
app.include_router(quizes_router)
app.include_router(questions_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
