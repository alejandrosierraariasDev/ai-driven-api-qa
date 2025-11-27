from datetime import datetime, timedelta
import json
import pytest
import requests

# Importar required libraries

# Configurar variables para la URL base y credenciales (en este caso, no se proporcionan)
url_base = 'http://localhost:8080'
base_url = None
api_client = None

# Estructura de los tests
@pytest.mark.parametrize("endpoint, expected_params", [
    # Verificación de Contrato
    ('/v1/customers', {'firstName': 'Juan', 'lastName': 'Diaz'}),  # Crear un cliente nuevo
    ('/v1/customers/{id}', {'firstName': 'Juan', 'lastName': 'Diaz'}),  # Obtener un cliente por ID
    ('/v1/customers/{id}/update', {'firstName': 'Juan', 'lastName': 'Diaz'}),  # Actualizar un cliente
    
    # Lógica de Negocio - cada caso de prueba debe ser una tupla separada
    ('/api/customers', [{'firstName': 'Juan', 'lastName': 'Diaz'}]),  # Crear un nuevo cliente
    ('/api/customers', [{'firstName': 'Juan', 'lastName': 'Diaz'}, {'lastName': 'Garcia'}]),  # Obtener clientes
    ('/api/customers', [{'firstName': 'Juan', 'lastName': 'Diaz'}, {'lastName': 'Garcia'}])
])



def test_get_all_users(base_url, api_client):
    response = requests.get(f'{base_url}/v1/customers')
    assert response.status_code == 200
    content = response.json()
    expected_results = [
        {'id': 'a2b3c4d5e6f7g8h9i0j1k', 'firstName': 'Juan', 'lastName': 'Diaz'},
        {'id': 'm1n2o3p4q5r6s7t8u9v10w11x12y13z14'},  # Crear varios clientes
    ]
    assert content == expected_results

def test_create_user_success(base_url, api_client):
    response = requests.post(f'{base_url}/v1/customers', json={'firstName': 'Juan', 'lastName': 'Diaz'})
    assert response.status_code == 201
    content = response.json()
    assert len(content) > 0
    expected_result = {'id': 'a2b3c4d5e6f7g8h9i0j1k'}
    assert expected_result in content

def test_create_user_invalid_data(base_url, api_client):
    response = requests.post(f'{base_url}/v1/customers', json={'firstName': '', 'lastName': ''})
    assert response.status_code == 400
    content = response.json()
    assert not any(item['email'] for item in content)

def test_get_user_by_id(base_url, api_client):
    response = requests.get(f'{base_url}/v1/customers/{api_client["id"]}')
    assert response.status_code == 200
    content = response.json()
    expected_result = {'id': 'a2b3c4d5e6f7g8h9i0j1k'}
    assert expected_result in content

def test_update_user(base_url, api_client):
    response = requests.put(f'{base_url}/v1/customers/{api_client["id"]}', json={'firstName': 'Juan', 'lastName': 'Diaz'})
    assert response.status_code == 200
    content = response.json()
    expected_result = {'id': 'a2b3c4d5e6f7g8h9i0j1k'}
    assert expected_result in content

def test_delete_user(base_url, api_client):
    response = requests.delete(f'{base_url}/v1/customers/{api_client["id"]}')
    assert response.status_code == 204