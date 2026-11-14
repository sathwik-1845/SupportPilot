import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(str, enum.Enum):
    SUPER_ADMIN = "super_admin"        # platform owner (you). Belongs to NO tenant.
    BUSINESS_ADMIN = "business_admin"  # manages one tenant
    SUPPORT_AGENT = "support_agent"    # works inside one tenant


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        # Super admins have no tenant; everyone else must have one. Enforced by the database.
        CheckConstraint(
            "(role = 'super_admin') = (tenant_id IS NULL)", name="ck_users_role_matches_tenant"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("tenants.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(
        SAEnum(Role, native_enum=False, length=20, values_callable=lambda e: [m.value for m in e]),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    tenant = relationship("Tenant", back_populates="users")


class RevokedToken(Base):
    """Logout denylist. Rows are safe to delete once expires_at has passed."""

    __tablename__ = "revoked_tokens"

    jti: Mapped[str] = mapped_column(String(32), primary_key=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)