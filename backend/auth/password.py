import bcrypt
from pydantic import SecretStr


def resolve_secret(value: str | SecretStr) -> str:
    return value.get_secret_value() if isinstance(value, SecretStr) else value


def hash_password(password: str | SecretStr) -> str:
    plain = resolve_secret(password)
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str | SecretStr) -> bool:
    resolved_hashed = resolve_secret(hashed)
    return bcrypt.checkpw(plain.encode("utf-8"), resolved_hashed.encode("utf-8"))
