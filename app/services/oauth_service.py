from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from app.models.user import User
from app.core.security import create_access_token

flow_store = {}


class OAuthService:
    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/gmail.readonly",
    ]

    REDIRECT_URI = "http://localhost:8000/auth/google/callback"

    def get_flow(self):
        return Flow.from_client_secrets_file(
            "credentials.json",
            scopes=self.SCOPES,
            redirect_uri=self.REDIRECT_URI,
        )

    def get_authorization_url(self):
        flow = self.get_flow()
        auth_url, state = flow.authorization_url(
            access_type="offline",
            prompt="consent",
        )
        flow_store[state] = flow
        return auth_url, state

    def handle_google_callback(self, code: str, state: str, db):
        flow = flow_store.get(state)
        if not flow:
            raise Exception("Invalid OAuth state")

        flow.fetch_token(code=code)
        credentials = flow.credentials

        gmail = build("gmail", "v1", credentials=credentials)
        profile = gmail.users().getProfile(userId="me").execute()

        email = profile.get("emailAddress")
        if not email:
            raise Exception("Email not found")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(email=email)
            db.add(user)

        user.access_token = credentials.token
        user.refresh_token = credentials.refresh_token
        user.token_expiry = credentials.expiry

        db.commit()
        db.refresh(user)

        token = create_access_token({"sub": user.email})

        flow_store.pop(state, None)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
            }
        }