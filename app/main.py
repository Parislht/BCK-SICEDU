from fastapi import FastAPI

from app.routers import auth

app = FastAPI(title="SICEDU API")

app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"status": "ok"}
