from datetime import datetime, timedelta

class TokenService:
    def is_token_expired(self, expiry_time: datetime):
        if not expiry_time:
            return True
        return datetime.utcnow() >= expiry_time

    def calculate_expiry(self, expires_in: int):
        return datetime.utcnow() + timedelta(seconds=expires_in)