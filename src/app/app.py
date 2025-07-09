from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from src.app.database import get_session
from src.app.models import User
from src.app.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/ola/mundo', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            or_(User.username == user.username, User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    statement = select(User).limit(limit).offset(offset)
    users = session.scalars(statement).all()
    if not users:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='No users found',
        )
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )

    return user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.get(User, user_id)
    # db_user = session.scalar(select(User).where(User.id == user_id
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    if user.username != db_user.username:
        existing_user = session.scalar(
            select(User).where(User.username == user.username)
        )
        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
    if user.email != db_user.email:
        existing_email = session.scalar(
            select(User).where(User.email == user.email)
        )
        if existing_email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    db_user.updated_at = datetime.now()
    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    # poderia usar : db_user = session.get(User, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found',
        )
    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted successfully'}
