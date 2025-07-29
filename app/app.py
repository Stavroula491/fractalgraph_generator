from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import julia

app = FastAPI()

# Mount the router
app.include_router(julia.router)

# Jinja templates setup (used in julia.py)
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name = "static")
