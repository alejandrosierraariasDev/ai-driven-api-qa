from datetime import datetime
from urllib.parse import urljoin, parse_qsl
import os
import pytest
import requests


# Fixture base_url
@pytest.fixture(scope="session")
def base_url():
    return os.getenv("API_BASE_URL", "http://localhost:8080")

# Fixture auth_headers
@pytest.fixture(scope="session")
def auth_headers():
    token = os.getenv("API_TOKEN")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# Estructura de los datos de prueba
@pytest.fixture(scope="function", autouse=True)
def data_providers():
    # Obtenemos la lista de clientes desde la API OpenAPI
    response = requests.get(base_url + "/customers")
    if response.status_code != 200:
        raise Exception("Error al obtener la lista de clientes")

    # Obtenemos los datos de cliente por ID
    for data in parse_qsl(response.text, skip_empty_strings=False):
        yield {
            "id": data["id"],
            "firstName": data.get("firstName"),
            "lastName": data.get("lastName"),
            "email": data.get("email"),
            "country": data.get("country")
        }

# Tests de Contrato
def test_contrato_validacion_get_customer_list():
    response = requests.get(base_url + "/customers")
    assert response.status_code == 200

def test_contrato_validacion_post_create_customer():
    response = requests.post(base_url + "/customers", json={"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == response.json()["id"]

def test_contrato_validacion_get_customer_by_id():
    # Simulamos un error de contexto (debe ser un 404)
    response = requests.get(base_url + "/customers/12345")
    assert response.status_code == 404

# Tests de Lógica de Negocio
def test_lnf_creatorule_lecturar_update_Eliminar():
    #Simulamos un estado de creación (DEBEN ser 200)
    response = requests.post(base_url + "/customers", json={"firstName": "John", "lastName": "Doe"})
    assert response.status_code == 201

    # Luego, simula la lógica de negocio para lectura, actualización y eliminación
    response_lecturar = requests.get(base_url + "/customers/12345")
    response_actualizar = requests.put(base_url + "/customers/12345", json={"firstName": "Jane"})
    response_eliminar = requests.delete(base_url + "/customers/12345")

    # Verificar que los respuestas sean correctas
    assert response_lecturar.status_code == 200
    assert response_actualizar.status_code == 200
    assert response_eliminar.status_code == 204

# Tests de Negocio
def test_negocio_validacion_post_entrada_completa():
    # Simulamos un estado de entrada correcto (DEBEN ser 201)
    response = requests.post(base_url + "/customers", json={"firstName": "John", "lastName": "Doe"})
    assert response.status_code == 201

def test_negocio_validacion_put_entrada_incomplete():
    # Simulamos un estado de entrada incompleta (DEBEN ser 400)
    response = requests.put(base_url + "/customers/12345")
    assert response.status_code == 400

# Tests de Errores
def test_negocio_problema_validacion_errorHTTP_405_methodNotAllowed():
    # Simulamos un estado de error para el método GET
    response = requests.get(base_url + "/customers")
    assert response.status_code == 405

def test_negocio_problema_validacion_error_http_403_forbidden():
    # Simulamos un estado de error para la petición GET
    response = requests.get("http://localhost:8080/customers")
    assert response.status_code == 403