import logging
from fastapi import FastAPI
from .routers import auth, users

passlib_logger = logging.getLogger("passlib")
#set to ignore lofs below ERROR: used to fix the error "(trapped) error reading bcrypt version"
passlib_logger.setLevel(logging.ERROR)

app = FastAPI(
    title="Secure Ingestion Module API",
    description="The backend service for securely ingesting and managing data.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Secure Ingestion API!"}