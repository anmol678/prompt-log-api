# app/main.py

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.errors.handlers import http_exception_handler
from app.api import api_router as router

app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(router, prefix="/api")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
