"""Gmail tool utils."""

from __future__ import annotations

import logging
import os
from typing import List, Optional, Tuple

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource
from googleapiclient.discovery import build as build_resource
from models.google_api_scope import GoogleApiScope

logger = logging.getLogger(__name__)


def import_google() -> Tuple[Request, Credentials]:
    """Import google libraries.

    Returns:
        Tuple[Request, Credentials]: Request and Credentials classes.
    """
    # google-auth-httplib2
    try:
        from google.auth.transport.requests import Request  # noqa: F401
        from google.oauth2.credentials import Credentials  # noqa: F401
    except ImportError:
        raise ImportError(
            "You need to install google-auth-httplib2 to use this toolkit. "
            "Try running pip install --upgrade google-auth-httplib2"
        )
    return Request, Credentials


def import_installed_app_flow() -> InstalledAppFlow:
    """Import InstalledAppFlow class.

    Returns:
        InstalledAppFlow: InstalledAppFlow class.
    """
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ImportError(
            "You need to install google-auth-oauthlib to use this toolkit. "
            "Try running pip install --upgrade google-auth-oauthlib"
        )
    return InstalledAppFlow


def import_googleapiclient_resource_builder() -> build_resource:
    """Import googleapiclient.discovery.build function.

    Returns:
        build_resource: googleapiclient.discovery.build function.
    """
    try:
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "You need to install googleapiclient to use this toolkit. "
            "Try running pip install --upgrade google-api-python-client"
        )
    return build


DEFAULT_SCOPES = ["https://mail.google.com/"]
DEFAULT_CREDS_TOKEN_FILE = "token.json"  # TODO： read from db
DEFAULT_CLIENT_SECRETS_FILE = "credentials.json"  # TODO： read from db


def get_gmail_credentials(
    token_file: Optional[str] = None,
    client_secrets_file: Optional[str] = None,
    scopes: Optional[List[GoogleApiScope]] = None,
) -> Credentials:
    """Get credentials."""
    # From https://developers.google.com/gmail/api/quickstart/python
    Request, Credentials = import_google()
    InstalledAppFlow = (
        import_installed_app_flow()
    )  # TODO： change to web app flow
    creds = None
    scopes = [scope.scope.value for scope in scopes] or DEFAULT_SCOPES
    token_file = token_file or DEFAULT_CREDS_TOKEN_FILE
    client_secrets_file = client_secrets_file or DEFAULT_CLIENT_SECRETS_FILE
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Token expired. Refreshing...")
            creds.refresh(Request())
            logger.info("Token refreshed successfully")
        else:
            logger.info("No valid credentials found. Starting auth flow...")
            # https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application # noqa
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes
            )
            # Use redirect_uri=http://localhost without specifying a port
            # This will work with the authorized redirect
            # URI in credentials.json
            try:
                creds = flow.run_local_server(
                    redirect_uri_trailing_slash=False
                )
                logger.info("Authentication flow completed successfully")
            except Exception as e:
                logger.error(f"Error during authentication flow: {e}")
                raise
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            logger.info(f"Credentials saved to {token_file}")
    return creds


def build_resource_service(
    credentials: Credentials,
    service_name: str = "gmail",
    service_version: str = "v1",
) -> Resource:
    """Build a Gmail service."""
    builder = import_googleapiclient_resource_builder()
    return builder(service_name, service_version, credentials=credentials)


def clean_email_body(body: str) -> str:
    """Clean email body."""
    try:
        from bs4 import BeautifulSoup

        try:
            soup = BeautifulSoup(str(body), "html.parser")
            body = soup.get_text()
            return str(body)
        except Exception as e:
            logger.error(e)
            return str(body)
    except ImportError:
        logger.warning("BeautifulSoup not installed. Skipping cleaning.")
        return str(body)


def has_valid_token(token_file: Optional[str] = None) -> bool:
    """Check if a valid token file exists locally.

    Args:
        token_file (Optional[str]): Path to token file. Defaults to
        DEFAULT_CREDS_TOKEN_FILE.

    Returns:
        bool: True if token file exists, False otherwise.
    """
    token_file = token_file or DEFAULT_CREDS_TOKEN_FILE
    return os.path.exists(token_file)
