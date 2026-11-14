"""Creates the platform Super Admin (no tenant). Run once:  python -m app.scripts.create_super_admin"""
import getpass
import sys

from pydantic import TypeAdapter, ValidationError
from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models import tenant as _tenant_models  # noqa: F401
from app.models.user import Role, User
from app.schemas.user import FullName, LowerEmail, Password


def main() -> None:
    try:
        email = TypeAdapter(LowerEmail).validate_python(input("Super admin email: "))
        full_name = TypeAdapter(FullName).validate_python(input("Full name: ").strip())
        password = TypeAdapter(Password).validate_python(getpass.getpass("Password: "))
    except ValidationError as e:
        sys.exit(f"Invalid input: {e.errors()[0]['msg']}")

    with SessionLocal() as db:
        if db.scalar(select(User.id).where(User.email == email)):
            sys.exit("A user with that email already exists.")
        db.add(
            User(
                tenant_id=None,
                full_name=full_name,
                email=email,
                hashed_password=get_password_hash(password),
                role=Role.SUPER_ADMIN,
            )
        )
        db.commit()
    print(f"Super admin created: {email}")


if __name__ == "__main__":
    main()