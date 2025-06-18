import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.features import router

app = FastAPI(title="Task Manager")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app=app)
