from fastapi import FastAPI
import uvicorn

from config import settings
from api.routers import search, items, recommend, kanbans, inference

app = FastAPI(title=settings.APP_NAME)

app.include_router(search.router)
app.include_router(items.router)
app.include_router(kanbans.router)
app.include_router(recommend.router)
app.include_router(inference.router)


@app.get("/")
def root():
    return {"HWF": "Search Engine"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, host="0.0.0.0", reload=True)
