from http import HTTPStatus


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


def test_read_users_deve_retornar_lista_de_usuarios(client):
    client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'teste@email.com',
        },
    )

    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'testuser', 'email': 'teste@email.com'},
            {'id': 2, 'username': 'testuser', 'email': 'teste@email.com'},
        ]
    }


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
    response = client.delete('/users/1')
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_nonexistent_user(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'
