from fastapi import FastAPI

from config import settings
from api.routers import search, items, recommend, kanbans

app = FastAPI(title=settings.APP_NAME)

app.include_router(search.router)
app.include_router(items.router)
app.include_router(kanbans.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


# uvicorn main:app --reload