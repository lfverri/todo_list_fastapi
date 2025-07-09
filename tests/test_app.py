from http import HTTPStatus

from src.app.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):
    response = client.get('/ola/mundo')  # Act (agir)
    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {'message': 'Olá, mundo!'}


def test_create_user_deve_criar_usuario(client):
    response = client.post(  # UserSchema (entrada)
        '/users/',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'teste@email.com',
        },
    )
    #  Validação : UserPublic (saída)
    assert response.status_code == HTTPStatus.CREATED  # se voltar 201
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'teste@email.com',
    }


def test_read_users(client):
    # Dados do usuário que será criado
    user_data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'teste@email.com',
    }

    # 1. Cria um usuário
    post_response = client.post(
        '/users/',
        json=user_data,
    )
    assert post_response.status_code == HTTPStatus.CREATED
    created_user = post_response.json()
    response = client.get('/users/')
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
    # Primeiro, crie o usuário para que ele exista no 'banco de dados'
    client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'teste@email.com',
        },
    )

    response = client.put(
        '/users/1',
        json={
            'username': 'teste_2',
            'password': 'testpassword',  # Adicione a senha aqui
            'email': 'teste2@email.com',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'teste_2',
        'email': 'teste2@email.com',
        # A senha não deve ser retornada se response_model for UserPublic
        # então o assert response.json() precisaria ser ajustado ou o model.
    }


def test_update_nonexistent_user(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'any',
            'password': 'any',
            'email': 'any@email.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_delete_user(client):
    user_data = {
        'username': 'user_to_delete',
        'password': 'password123',
        'email': 'delete@example.com',
    }
    create_response = client.post('/users/', json=user_data)
    assert create_response.status_code == HTTPStatus.CREATED
    created_user_id = create_response.json()['id']
    response = client.delete(f'/users/{created_user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}

    get_deleted_user_response = client.get(f'/users/{created_user_id}')

    assert get_deleted_user_response.status_code == HTTPStatus.NOT_FOUND
    assert get_deleted_user_response.json() == {'detail': 'User not found'}


def test_delete_nonexistent_user(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'
