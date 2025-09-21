from http import HTTPStatus

from src.app.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/ola/mundo')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_create_user_deve_criar_usuario(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'teste@email.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'teste@email.com',
    }


def test_read_users(client, auth_headers):
    user_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'teste@email.com',
    }

    post_response = client.post('/users/', json=user_data)
    assert post_response.status_code == HTTPStatus.CREATED
    created_user = post_response.json()

    response = client.get('/users/', headers=auth_headers)
    assert response.status_code == HTTPStatus.OK
    expected_users = [
        {
            'id': created_user['id'],
            'username': user_data['username'],
            'email': user_data['email'],
        }
    ]
    assert response.json() == {'users': expected_users}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client):
    client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'teste@email.com',
        },
    )

    login_response = client.post(
        '/token',
        data={
            'username': 'teste@email.com',
            'password': 'testpassword',
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    assert login_response.status_code == HTTPStatus.OK
    assert 'access_token' in login_response.json()
    token = login_response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        '/users/1',
        headers=headers,
        json={
            'username': 'teste_2',
            'password': 'testpassword',
            'email': 'teste2@email.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'teste_2'
    assert response.json()['email'] == 'teste2@email.com'


# def test_delete_user(client, auth_headers): precisa corrigir
#     user_data = {
#         'username': 'user_to_delete',
#         'password': 'password123',
#         'email': 'delete@example.com',
#     }

#     create_response = client.post('/users/', json=user_data)
#     assert create_response.status_code == HTTPStatus.CREATED
#     created_user_id = create_response.json()['id']
#     response = client.delete(f'/users/{created_user_id}',
# headers=auth_headers)
#     assert response.status_code == HTTPStatus.OK


# def test_delete_nonexistent_user(client, auth_headers): # precisa corrigir
#     response = client.delete('/users/999', headers=auth_headers)
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json()['detail'] == 'User not found'


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'Bearer'
    assert len(token['access_token']) > 0
