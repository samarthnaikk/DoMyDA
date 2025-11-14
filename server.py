from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
import asyncio
from solver.quiz_solver import solve_quiz

SECRET = "supersecret123"

app = FastAPI()


class Input(BaseModel):
    email: EmailStr
    secret: str
    url: str


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Invalid JSON or missing fields"})


@app.post("/")
async def root(payload: Input):
    if payload.secret != SECRET:
        raise HTTPException(status_code=403, detail="Invalid secret")
    asyncio.create_task(solve_quiz(payload.email, payload.secret, payload.url))
    return {"status": "received", "message": "Solver running"}
