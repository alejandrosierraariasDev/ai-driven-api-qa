
import pytest
from typing import Dict, List, Tuple
from fastapi.testclient import TestClient
from pydantic import BaseModel, BaseModel as PydanticBaseModel
from uuid import uuid4
from datetime import datetime

# Clase de prueba para el Customer API
class CustomerApi:
    def __init__(self, client: TestClient):
        self.client = client

    # Función para obtener una lista de clientes
    @pytest.mark.asyncio
    async def get_customers(self) -> Dict[str, List[Dict]]:
        response = await self.client.get('/customers')
        return response.json()

    # Función para crear un cliente nuevo
    @pytest.mark.asyncio
    async def create_customer(self, name: str, email: str, country: str):
        data = {
            'firstName': name,
            'lastName': '',
            'email': email,
            'country': country
        }
        response = await self.client.post('/customers', json=data)
        return response.json()

    # Función para obtener un cliente por ID
    @pytest.mark.asyncio
    async def get_customer(self, id: str):
        response = await self.client.get(f'/customers/{id}')
        return response.json()

    # Función para actualizar un cliente completo
    @pytest.mark.asyncio
    async def update_customer(self, id: str, name: str, email: str, country: str):
        data = {
            'firstName': name,
            'lastName': '',
            'email': email,
            'country': country
        }
        response = await self.client.put(f'/customers/{id}', json=data)
        return response.json()

    # Función para eliminar un cliente por ID
    @pytest.mark.asyncio
    async def delete_customer(self, id: str):
        response = await self.client.delete(f'/customers/{id}')
        return response.status_code

# Clase de prueba utilizando Pytest
@pytest.fixture
def client():
    with TestClient() as app:
        # Crea una instancia del cliente
        yield app

class CustomerAPITests(CustomerApi):
    def __init__(self, client: Client):
        super().__init__(client)

    @pytest.mark.asyncio
    async def test_get_customers(self) -> List[Dict]:
        response = await self.get_customers()
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_create_customer(self) -> Dict:
        data = {
            'firstName': 'John',
            'lastName': '',
            'email': 'john@example.com',
            'country': 'US'
        }
        response = await self.create_customer(**data)
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_get_customer(self) -> Dict:
        data = {
            'id': str(uuid4())
        }
        response = await self.get_customer(data['id'])
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_update_customer(self) -> Dict:
        data = {
            'firstName': 'Jane',
            'lastName': '',
            'email': 'jane@example.com',
            'country': 'US'
        }
        await self.update_customer('123', **data)
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_delete_customer(self) -> int:
        await self.delete_customer('123')
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'status' in response
        assert 'id' in response
        assert 'firstName' not in response
        assert 'lastName' not in response
        assert 'email' not in response
        assert 'country' not in response

# Clase de prueba utilizando Pytest
class CustomerAPITests:
    def __init__(self, client: TestClient):
        self.client = client

    @pytest.mark.asyncio
    async def test_get_all_customers(self) -> List[Dict]:
        response = await self.get_customers()
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_get_customer_by_id(self) -> Dict:
        data = {
            'id': str(uuid4())
        }
        await self.get_customer(data['id'])
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_create_customer(self) -> Dict:
        data = {
            'firstName': 'John',
            'lastName': '',
            'email': 'john@example.com',
            'country': 'US'
        }
        await self.create_customer(**data)
        response = await self.get_customer(data['id'])
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_update_customer(self) -> Dict:
        data = {
            'firstName': 'Jane',
            'lastName': '',
            'email': 'jane@example.com',
            'country': 'US'
        }
        await self.update_customer('123', **data)
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    @pytest.mark.asyncio
    async def test_delete_customer(self) -> int:
        await self.delete_customer('123')
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'status' in response
        assert 'id' not in response
        assert 'firstName' not in response
        assert 'lastName' not in response
        assert 'email' not in response
        assert 'country' not in response

# Crea una instancia del cliente y las pruebas para el Customer API
client = TestClient()
customer_api = CustomerAPI(client)

# Crea pruebas utilizando Pytest
def create_customer(name: str, email: str, country: str):
    data = {
        'firstName': name,
        'lastName': '',
        'email': email,
        'country': country
    }
    response = await customer_api.create_customer(**data)
    assert isinstance(response, dict)
    assert 'id' in response
    assert 'firstName' in response
    assert 'lastName' in response
    assert 'email' in response

def get_customer(id: str):
    data = {
        'id': id
    }
    response = await customer_api.get_customer(**data)
    assert isinstance(response, dict)
    assert 'id' in response
    assert 'firstName' in response
    assert 'lastName' in response
    assert 'email' in response

def update_customer(id: str, name: str, email: str, country: str):
    data = {
        'firstName': name,
        'lastName': '',
        'email': email,
        'country': country
    }
    await customer_api.update_customer(id, **data)
    response = await customer_api.get_customer(id)
    assert isinstance(response, dict)
    assert 'id' in response
    assert 'firstName' not in response
    assert 'lastName' not in response
    assert 'email' not in response
    assert 'country' not in response

def delete_customer(id: str):
    await customer_api.delete_customer(id)
    response = await customer_api.get_customer(id)
    assert isinstance(response, dict)
    assert 'status' in response
    assert 'id' not in response
    assert 'firstName' not in response
    assert 'lastName' not in response
    assert 'email' not in response
    assert 'country' not in response

# Crea una clase de prueba para el Customer API utilizando Pytest
class CustomerAPITests:
    def __init__(self, client: Client):
        self.client = client

    # Función para obtener una lista de clientes
    async def test_get_all_customers(self) -> List[Dict]:
        response = await self.get_all_customers()
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response
        assert 'country' in response

    # Función para obtener un cliente por ID
    async def test_get_customer_by_id(self) -> Dict:
        data = {
            'id': str(uuid4())
        }
        await self.get_customer(data['id'])
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response

    # Función para crear un cliente nuevo
    async def test_create_customer(self) -> Dict:
        data = {
            'firstName': 'John',
            'lastName': '',
            'email': 'john@example.com',
            'country': 'US'
        }
        await self.create_customer(**data)
        response = await self.get_customer(data['id'])
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' in response
        assert 'lastName' in response
        assert 'email' in response

    # Función para actualizar un cliente completo
    async def test_update_customer(self) -> Dict:
        data = {
            'firstName': 'Jane',
            'lastName': '',
            'email': 'jane@example.com',
            'country': 'US'
        }
        await self.update_customer('123', **data)
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'id' in response
        assert 'firstName' not in response
        assert 'lastName' not in response
        assert 'email' not in response
        assert 'country' not in response

    # Función para eliminar un cliente por ID
    async def test_delete_customer(self) -> int:
        await self.delete_customer('123')
        response = await self.get_customer('123')
        assert isinstance(response, dict)
        assert 'status' in response
        assert 'id' not in response
        assert 'firstName' not in response
        assert 'lastName' not in response
        assert 'email' not in response
        assert 'country' not in response

# Inicializa la instancia del cliente y las pruebas
client = TestClient()
customer_api = CustomerAPI(client)
