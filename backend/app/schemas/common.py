from typing import Annotated

from pydantic import AfterValidator, EmailStr, HttpUrl, TypeAdapter

_http_url = TypeAdapter(HttpUrl)


def _normalize_email(v: str) -> str:
    return v.strip().lower()


def _clean_website(v: str | None) -> str | None:
    """'' -> None; 'acme.com' -> 'https://acme.com/'; only http(s) accepted."""
    if v is None:
        return None
    v = v.strip()
    if not v:
        return None
    if "://" not in v:
        v = "https://" + v
    try:
        url = str(_http_url.validate_python(v))
    except ValueError:
        raise ValueError("Enter a valid website URL (http or https)") from None
    if len(url) > 500:
        raise ValueError("Website URL is too long")
    return url


LowerEmail = Annotated[EmailStr, AfterValidator(_normalize_email)]
WebsiteUrl = Annotated[str | None, AfterValidator(_clean_website)]