import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel, Schema as PydanticSchema
from datetime import date, timedelta

# Configuración de Pruebas (Fixture)
@pytest.fixture
def client():
    # Crear un client FastAPI
    test_client = TestClient(fastapi_app="app")
    
    return test_client


# Clase de Interacción (API)
class API:
    def __init__(self, app):
        self.app = app
    
    async def create_customer(self, customer: PydanticSchema):
        # Crear un cliente nuevo
        response = await self.app.post("/customers", json=customer.dict())
        
        return response.json()

    async def get_customer_by_id(self, id: str):
        # Obtener cliente por ID
        response = await self.app.get(f"/customers/{id}")
        
        return response.json()

    async def update_customer(self, customer_id: str, customer: PydanticSchema):
        # Actualizar cliente completo
        body = customer.dict()
        response = await self.app.put(f"/customers/{customer_id}", json=body)

        return response.json()


# Clase de Tests Pytest (TestFlows)
@pytest.mark.asyncio
async def test_create_customer():
    # Crear un cliente nuevo
    api = API(app)
    customer = PydanticSchema(title="Customer")
    
    expected_response = {"id": str(date()), "firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "country": "US", "status": "ACTIVE"}
    
    response = await api.create_customer(customer)
    
    assert response["id"] == expected_response["id"]
    assert response["firstName"] == expected_response["firstName"]
    assert response["lastName"] == expected_response["lastName"]
    assert response["email"] == expected_response["email"]
    assert response["country"] == expected_response["country"]
    assert response["status"] == expected_response["status"]

    # Verificar el cuerpo de la respuesta
    assert isinstance(response, dict)
    assert "id" in response
    assert "firstName" in response
    assert "lastName" in response
    assert "email" in response
    assert "country" in response
    assert "status" in response


@pytest.mark.asyncio
async def test_get_customer_by_id():
    # Obtener cliente por ID
    api = API(app)
    
    customer = PydanticSchema(title="Customer")
    customer = customer.replace(email="johndoe@example.com", phone=None, birthDate=date(1990, 1, 1), country="US").dict()
    
    expected_response = {"id": str(date()), "firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "country": "US", "status": "ACTIVE"}
    
    response = await api.get_customer_by_id("12345")
    
    assert response["id"] == expected_response["id"]
    assert response["firstName"] == expected_response["firstName"]
    assert response["lastName"] == expected_response["lastName"]
    assert response["email"] == expected_response["email"]
    assert response["country"] == expected_response["country"]
    assert response["status"] == expected_response["status"]

    # Verificar el cuerpo de la respuesta
    assert isinstance(response, dict)
    assert "id" in response
    assert "firstName" in response
    assert "lastName" in response
    assert "email" in response
    assert "country" in response
    assert "status" in response


@pytest.mark.asyncio
async def test_update_customer():
    # Actualizar cliente completo
    api = API(app)
    
    customer = PydanticSchema(title="Customer")
    customer = customer.replace(id=str(date()), firstName="John", lastName="Doe", email="johndoe@example.com", country="US", status="ACTIVE").dict()
    
    expected_response = {"id": str(date()), "firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "country": "US", "status": "ACTIVE"}
    
    response = await api.update_customer("12345", customer)

    assert response["id"] == expected_response["id"]
    assert response["firstName"] == expected_response["firstName"]
    assert response["lastName"] == expected_response["lastName"]
    assert response["email"] == expected_response["email"]
    assert response["country"] == expected_response["country"]
    assert response["status"] == expected_response["status"]

    # Verificar el cuerpo de la respuesta
    assert isinstance(response, dict)
    assert "id" in response
    assert "firstName" in response
    assert "lastName" in response
    assert "email" in response
    assert "country" in response
    assert "status" in response


# Configuración de Pruebas (Fixture final)
@pytest.fixture
def app():
    # Crear un cliente FastAPI
    from fastapi import FastAPI
    class Customer:
        def __init__(self):
            self.id = str(date())
            self.firstName = "John"
            self.lastName = "Doe"
            self.email = "johndoe@example.com"
            self.country = "US"
            self.status = "ACTIVE"

    app = FastAPI()
    from . import api

    # Configurar el servidor
    app.add_api_route("/customers", api)
    
    return app


# Finalización de la configuración de pruebas
def main():
    # Crear un client FastAPI
    test_client = TestClient(fastapi_app=app)

    # Pruebas unitarias
    # ...

if __name__ == "__main__":
    main()
