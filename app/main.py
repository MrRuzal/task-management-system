from contextlib import asynccontextmanager

from app.container import Container

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse

from app.entrypoints.api.routes.users import router as users_router
from app.entrypoints.api.routes.tasks import router as tasks_router
from app.entrypoints.api.routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    container.wire(
        modules=[
            "app.entrypoints.api.routes.users",
            "app.entrypoints.api.routes.tasks",
            "app.entrypoints.api.routes.auth",
        ]
    )
    app.container = container
    yield


app = FastAPI(
    title="Task Management System",
    lifespan=lifespan,
)

app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_validation_exception_handler(_: Request, exc: HTTPException):
    content = {"detail": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=content)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return RedirectResponse(url="/docs")
