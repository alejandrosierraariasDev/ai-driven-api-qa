```python
import pytest
from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import json

# Configuración de pruebas ( fixtures )
@pytest.fixture
def client():
    app = FastAPI()
    with app.test_client() as test_client:
        yield test_client

# Modelo Pydantic para el modelo de cliente
class CustomerBase(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    country: str
    status: str
    subscribedNewsletter: bool
    createdAt: str
    updatedAt: str

class Customer(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    phone: str
    birthDate: str
    country: str
    status: str
    subscribedNewsletter: bool

# Clase de interacción (API)
class API:
    def __init__(self, client):
        self.client = client

    async def get_customer(self, id):
        response = await self.client.get(f"/customers/{id}")
        return Customer(response.json())

    async def create_customer(self, customer: CustomerCreate):
        response = await self.client.post("/customers", json=customer.dict())
        return Customer(response.json())

    async def get_customer(self, id):
        return await self.client.get(f"/customers/{id}")

    async def update_customer(self, id, customer: CustomerUpdate):
        response = await self.client.put(f"/customers/{id}", json=customer.dict())
        return Customer(response.json())

    async def delete_customer(self, id):
        response = await self.client.delete(f"/customers/{id}")
        return {"message": "Cliente eliminado correctamente"}

# Clase de prueba (TestFlows)
@pytest.mark.asyncio
async def test_create_customer(client):
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juan.perez@example.com",
        country="Spain"
    )
    response = await client.post("/customers", json=customer.dict())
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_customer(client):
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juan.perez@example.com",
        country="Spain"
    )
    response = await client.get(f"/customers/{uuid.uuid4()}")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_customer(client):
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juan.perez@example.com",
        country="Spain"
    )
    response = await client.put(f"/customers/{uuid.uuid4()}", json=customer.dict())
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_customer(client):
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juan.perez@example.com",
        country="Spain"
    )
    response = await client.delete(f"/customers/{uuid.uuid4()}")
    assert response.status_code == 204

# Configuración de la aplicación para el test
app = FastAPI()

# Función principal (main) que ejecuta los tests
async def main():
    try:
        # Crear un cliente nuevo
        api = API(app)
        customer_create_response = await api.create_customer(customer_create={"firstName": "Juan", "lastName": "Pérez", "email": "juan.perez@example.com"})
        assert customer_create_response.status_code == 201

        # Obtener el cliente creado
        response = await api.get_customer(uuid.uuid4())
        assert response.status_code == 200

        # Actualizar al cliente
        customer_update_response = await api.update_customer(
            uuid.uuid4(), 
            customer_update={"firstName": "Juan", "lastName": "Pérez", "email": "juan.perez@example.com"}
        )
        assert customer_update_response.status_code == 200

        # Eliminar el cliente
        response = await api.delete_customer(uuid.uuid4())
        assert response.status_code == 204
    except Exception as e:
        pytest.fail(f"Error: {e}")

# Ejecución del main en la aplicación (con pytest)
if __name__ == "__main__":
    from pydantic import validator
    # Validator para asegurar que el ID tenga un formato válido
    @validator("id")
    def id_is_valid(cls, v):
        if not isinstance(v, str):
            raise ValueError("Id debe ser un string")
        return uuid.uuid4()
    app.add_argument("id", type=str)
```

Esta es la implementación completa del script Python que proporciona tests para una API REST. La función `main` define el flujo de prueba y ejecuta las pruebas en función del cliente creado, utilizando el FastAPI como backend. Se utilizan funciones asincrónicas (asynchronous) y aserciones directas (`assert`) para garantizar la veracidad de los datos de respuesta.