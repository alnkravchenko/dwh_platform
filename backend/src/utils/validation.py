from string import ascii_letters, digits
from typing import Tuple

from pydantic import SecretStr


def validate_password(value: SecretStr) -> Tuple[bool, str]:
    pwd = value.get_secret_value()
    msgs = []
    if len(pwd) < 8:
        msgs.append("be at least 8 characters long")
    if any(char.isspace() for char in pwd):
        msgs.append("not contain spaces")
    if not any(char.isupper() for char in pwd):
        msgs.append("contain an uppercase letter")
    if not any(char.isdecimal() for char in pwd):
        msgs.append("contain a number")
    if set(pwd).difference(ascii_letters + digits):
        msgs.append("not contain any special characters (!@#$%^&*()-+?_=,<>/)")

    if msgs:
        return False, f"Password must: {', '.join(msgs)}"
    return True, "Password is valid"
