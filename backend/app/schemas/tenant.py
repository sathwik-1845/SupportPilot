import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.tenant import TenantStatus


class TenantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    business_name: str
    business_email: EmailStr
    industry: str
    status: TenantStatus
    created_at: datetime


class TenantStatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: TenantStatus