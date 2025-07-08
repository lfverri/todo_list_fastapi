from sqlalchemy import select

from src.app.models import User


def test_create_user(session):
    user = User(username='lucas', email='teste@email.com', password='senha')
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.username == 'lucas'))

    assert result.username == 'lucas'
