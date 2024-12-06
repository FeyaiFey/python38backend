from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from database.init_db import create_db_and_tables
from api import mo,auth,users,files,bi,test
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="upload/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},  # 传递具体的错误信息
    )

# Include routers

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(mo.router, prefix="/mo", tags=["mo"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(test.router, prefix="/test", tags=["test"])
app.include_router(bi.router, prefix="/bi", tags=["bi"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# For testing purposes
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}