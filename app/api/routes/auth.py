from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.oauth_service import OAuthService
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.oauth_service import OAuthService

router = APIRouter()
oauth_service = OAuthService()

@router.get("/google/login")
def google_login():
    auth_url, state = oauth_service.get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/google/callback")
def google_callback(code: str, state: str, db: Session = Depends(get_db)):
    return oauth_service.handle_google_callback(code, state, db)