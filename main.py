"""
╔══════════════════╗
              TEAMDEV
╚══════════════════╝

[ PROJECT   ]  TeamDev AIO (All-In-One Downloader)
[ DEVELOPER ]  @MR_ARMAN_08

────────────────────

[ SUPPORT   ]  https://t.me/Team_X_Og
[ UPDATES   ]  https://t.me/TeamDevXBots
[ ABOUT US  ]  https://TeamDev.sbs

────────────────────

[ DONATE    ]  https://Pay.TeamDev.sbs

────────────────────
      FAST • POWERFUL • ALL-IN-ONE
      
"""

# Read @License Don't Copy This File This Code Made Only For This Project Do Not Try To Use This Script.

from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import time

from app.core.database import init_db
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.ban import BanMiddleware
from app.middleware.logger import RequestLoggerMiddleware
from app.routes import download, admin, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="TeamDev AIO API",
    version="2.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)

templates = Jinja2Templates(directory="templates")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RequestLoggerMiddleware)
app.add_middleware(BanMiddleware)
app.add_middleware(RateLimitMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(download.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/admin")
app.include_router(auth.router, prefix="/auth")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico", media_type="image/x-icon")

@app.get("/robots.txt", include_in_schema=False)
async def robots():
    return FileResponse("robots.txt", media_type="text/plain")

@app.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    return FileResponse("sitemap.xml", media_type="application/xml")

@app.get("/TeamDev-Logo.jpg", include_in_schema=False)
async def logo():
    return FileResponse("TeamDev-Logo.jpg", media_type="image/jpeg")

@app.get("/health")
async def health():
    return {"status": "ok", "ts": int(time.time())}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
