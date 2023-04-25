import structlog
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from repos.database import get_db
from repos.users import create_user
from schema.jwt_auth import Token
from schema.responses import DefaultResponse, TokenResponse
from schema.user import UserModel
from sqlalchemy.orm import Session
from utils import jwt_auth
from utils import verification as verif
from utils.validation import validate_password

log = structlog.get_logger(module=__name__)
router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")


@router.post(
    "/login", responses={200: {"model": TokenResponse}, 401: {"model": DefaultResponse}}
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    is_verified, msg = verif.verify_user(db, user)
    status_code = 200 if is_verified else 401
    log.info(f"[LOGIN | GETTING TOKEN] {status_code} {msg}")
    # create response
    response_content = {"details": msg}
    if status_code == 200:
        user_token = Token(
            access_token=jwt_auth.create_access_token(user.email),
            token_type="bearer",
        )
        response_content.update(token=user_token.json())
    return JSONResponse(content=response_content, status_code=status_code)


@router.post(
    "/sign_up",
    responses={201: {"model": TokenResponse}, 400: {"model": DefaultResponse}},
)
def sign_up(user: UserModel, db: Session = Depends(get_db)) -> JSONResponse:
    is_verified = verif.verify_new_user(db, user)
    is_validated = validate_password(user.password)
    sign_up_flag = all([is_verified[0], is_validated[0]])

    if sign_up_flag:
        create_user(db, user)

    msgs = "".join(
        [msg[1] + ". " for msg in [is_verified, is_validated] if msg[0] == sign_up_flag]
    ).strip()
    status_code = 201 if sign_up_flag else 400
    log.info(f"[SIGN UP] {status_code} {msgs}")
    # create response
    response_content = {"details": msgs}
    if status_code == 201:
        user_token = Token(
            access_token=jwt_auth.create_access_token(user.email),
            token_type="bearer",
        )
        response_content.update(token=user_token.json())
    return JSONResponse(content=response_content, status_code=status_code)
