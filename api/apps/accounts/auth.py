from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User

ALGORITHM = "HS256"


def _encode(payload, lifetime):
    now = datetime.now(timezone.utc)
    payload = {**payload, "iat": now, "exp": now + lifetime}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def issue_tokens(user):
    return {
        "access": _encode(
            {"sub": str(user.id), "type": "access", "email": user.email},
            timedelta(minutes=settings.JWT_ACCESS_MINUTES),
        ),
        "refresh": _encode(
            {"sub": str(user.id), "type": "refresh"},
            timedelta(days=settings.JWT_REFRESH_DAYS),
        ),
        "expires_in": settings.JWT_ACCESS_MINUTES * 60,
    }


def decode(token, expected_type="access"):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token.")
    if payload.get("type") != expected_type:
        raise AuthenticationFailed("Wrong token type.")
    return payload


class JWTAuthentication(BaseAuthentication):
    keyword = "Bearer"

    def authenticate(self, request):
        header = request.headers.get("Authorization", "")
        if not header.startswith(f"{self.keyword} "):
            return None
        payload = decode(header.split(" ", 1)[1].strip())
        user = User.objects(id=payload["sub"], is_active=True).first()
        if not user:
            raise AuthenticationFailed("User not found.")
        return (user, None)

    def authenticate_header(self, request):
        return self.keyword
