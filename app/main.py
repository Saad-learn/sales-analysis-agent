from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user, email, analysis
from app.api.routes import auth, gmail, analysis, user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Sales Email Analyzer")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(gmail.router, prefix="/gmail", tags=["Gmail"])
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "AI Sales Email Analyzer is running"}