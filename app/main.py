from fastapi import FastAPI

app = FastAPI(title="SICEDU API")


@app.get("/")
def read_root():
    return {"status": "ok"}
