from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db, DATABASE_URL
from sqlalchemy import create_engine
from models import Base
from routes.user_routes import router as user_router
from routes.ai_response_routes import router as ai_response_router
from routes.email_routes import router as email_router
from routes.history_routes import router as history_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; refine for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)
app.include_router(ai_response_router)
app.include_router(email_router)
app.include_router(history_router)

# Create database tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/dashboard")

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "user": request.cookies.get("user"), "is_auth": True})

@app.post("/signup")
async def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"User Registered: {username}, {email}")
    return RedirectResponse(url="/signin", status_code=303)

@app.get("/signin", response_class=HTMLResponse)
async def signin_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "user": request.cookies.get("user"), "is_auth": True})

@app.post("/signin")
async def signin(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"User Sign In Attempt: {email}")
    # Simple simulated session for UI demonstration
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user", value=email)
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse(url="/signin")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "is_auth": False})

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/signin")
    response.delete_cookie("user")
    return response

@app.get("/projects", response_class=HTMLResponse)
async def projects_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": request.cookies.get("user") or "Guest", "is_auth": False})

@app.get("/messages", response_class=HTMLResponse)
async def messages_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": request.cookies.get("user") or "Guest", "is_auth": False})

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": request.cookies.get("user") or "Guest", "is_auth": False})

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": request.cookies.get("user") or "Guest", "is_auth": False})

# Redundant routes removed to use user_routes.py instead


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
