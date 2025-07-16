from http import HTTPStatus
from http.client import HTTPException

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerifyMismatchError

ph = PasswordHasher()


SECRET_KEY = 'your_secret_key_here'
ALGORITHM = 'HS256'
ACESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> None:
    try:
        ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect password',
        )
    except InvalidHash:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid password hash',
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='An error occurred while verifying the password',
        )

def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)
    
    decoded = decode(token, SECRET_KEY)
    
    assert decoded['test'] == 'test'
    assert 'exp' in decoded
    