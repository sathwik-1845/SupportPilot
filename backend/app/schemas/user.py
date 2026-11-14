import re
import uuid
from datetime import datetime
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, Field

from app.models.user import Role
from app.schemas.tenant import TenantOut


def _normalize_email(v: str) -> str:
    return v.strip().lower()


def _check_password(v: str) -> str:
    if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
        raise ValueError("Password must contain at least one letter and one digit")
    return v


LowerEmail = Annotated[EmailStr, AfterValidator(_normalize_email)]
Password = Annotated[str, Field(min_length=8, max_length=128), AfterValidator(_check_password)]
FullName = Annotated[str, Field(min_length=2, max_length=120)]


class BusinessRegister(BaseModel):
    """Public sign-up: creates a tenant plus its first Business Admin."""

    model_config = ConfigDict(extra="forbid")

    business_name: Annotated[str, Field(min_length=2, max_length=200)]
    business_email: LowerEmail
    industry: Annotated[str, Field(min_length=2, max_length=100)]
    admin_full_name: FullName
    admin_email: LowerEmail
    password: Password


class UserCreate(BaseModel):
    """Business Admin adds a teammate. tenant_id is NOT accepted: it always comes from the caller."""

    model_config = ConfigDict(extra="forbid")

    full_name: FullName
    email: LowerEmail
    password: Password
    role: Literal[Role.BUSINESS_ADMIN, Role.SUPPORT_AGENT] = Role.SUPPORT_AGENT


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID | None
    full_name: str
    email: EmailStr
    role: Role
    created_at: datetime


class BusinessRegisterOut(BaseModel):
    tenant: TenantOut
    user: UserOut


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int