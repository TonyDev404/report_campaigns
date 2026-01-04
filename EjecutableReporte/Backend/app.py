from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.campaigns import router as campaigns_router

app = FastAPI(title="Campaign Export API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(campaigns_router)