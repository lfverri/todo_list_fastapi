from http import HTTPStatus

from fastapi.testclient import TestClient

from app.app import app


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)  # Arreange (organizar)
    response = client.get('/ola/mundo')  # Act (agir)
    assert response.status_code == HTTPStatus.OK  # Assert (afirmar)
    assert response.json() == {'message': 'Olá, mundo!'}
