import bcrypt


def get_hashed_password(pwd: str) -> str:
    """
    Hash a password with auto-generated salt using bcrypt
    """
    bytes_password = pwd.encode("utf-8")
    return bcrypt.hashpw(bytes_password, bcrypt.gensalt()).decode("utf-8")


def check_password(pwd: str, hashed_pwd: str) -> bool:
    """
    Check hashed password using bcrypt
    """
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd.encode("utf-8"))
