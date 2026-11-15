import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.tenant import TenantStatus
from app.schemas.common import LowerEmail, WebsiteUrl

Description = Annotated[str | None, Field(max_length=1000)]


class TenantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_name: str
    business_email: EmailStr
    industry: str
    description: str | None
    website_url: str | None
    status: TenantStatus
    created_at: datetime


class TenantUpdate(BaseModel):
    """Business Admin edits their own business profile. Status/id are not editable here."""

    model_config = ConfigDict(extra="forbid")

    business_name: Annotated[str | None, Field(min_length=2, max_length=200)] = None
    business_email: LowerEmail | None = None
    industry: Annotated[str | None, Field(min_length=2, max_length=100)] = None
    description: Description = None
    website_url: WebsiteUrl = None


class TenantStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: TenantStatus