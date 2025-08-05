from fastapi import FastAPI

app = FastAPI(title="FERJEE Student System")

@app.get("/")
async def root():
    return {"message": "Welcome to FERJEE Student System API"}