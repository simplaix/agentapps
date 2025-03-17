from __future__ import annotations

from models.google_api_scope import GoogleApiScope
from utils.utils import (
    build_resource_service,
    get_gmail_credentials,
    has_valid_token,
)


def login(scopes: list[GoogleApiScope] = None):
    """Login to Google for the given scopes.

    Args:
        scopes: The scopes to login to.
    """
    build_gmail_service(scopes=scopes)
    return {
        "status": f"OK, logged in successfully with the given scopes {scopes}"
    }


def logout():
    pass


def check_gmail_token_file() -> bool:
    """Check if a valid token file exists locally."""
    return has_valid_token()


def build_gmail_service(scopes: list[GoogleApiScope] = None):
    """Get Gmail credentials."""
    token_file = get_gmail_credentials(scopes=scopes)
    return build_resource_service(token_file)
