from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class AvailableGoogleApiScope(Enum):
    """Available Google API scopes."""

    GMAIL = "https://mail.google.com/"
    CALENDAR = "https://www.googleapis.com/auth/calendar"
    CALENDAR_EVENTS = "https://www.googleapis.com/auth/calendar.events"


class GoogleApiScope(BaseModel):
    """Google API scope."""

    scope: AvailableGoogleApiScope = Field(
        ..., description="The scope of the API"
    )
