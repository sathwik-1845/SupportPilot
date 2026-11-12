from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# This imports the router.py file you just edited
from app.api.v1 import router as api_v1_router 

app = FastAPI(title="SupportPilot API")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add this in main.py
@app.get("/")
def root():
    return {"message": "Welcome to the SupportPilot API"}

# This now successfully finds the 'router' variable from router.py
app.include_router(api_v1_router.router, prefix="/api/v1")