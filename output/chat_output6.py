```python
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel, ValidationError
from pydantic.errors import ModelValidationError
from typing import Dict
import pytest

# Configuración de la base de datos (reemplazar con la configuración real)
BASE_URL = 'http://localhost:8080'

class CustomerBase(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    country: str
    status: str
    subscribedNewsletter: bool

class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str

class CustomerUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthDate: str
    country: str
    status: str
    subscribedNewsletter: bool

def validate_customer_data(data: Dict, required_fields: list) -> None:
    """Validar campos obligatorios."""
    for field in required_fields:
        if not data.get(field):
            raise ModelValidationError(f"El campo '{field}' está vacío")

class Customer(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    country: str

async def get_customer(id: str) -> Dict:
    """Obtener cliente por ID."""
    response = await FastAPI().get(f"{BASE_URL}/customers/{id}")
    if response.status_code == 404:
        raise Exception("Cliente no encontrado")
    return {"id": id, "first_name": response.json()["firstName"], "lastName": response.json()["lastName"], "email": response.json()["email"]}

async def create_customer(**kwargs) -> Dict:
    """Crear cliente nuevo."""
    try:
        validate_customer_data(kwargs, ["firstName", "lastName", "email"])
    except ModelValidationError as e:
        raise Exception(e)
    
    response = await FastAPI().post(f"{BASE_URL}/customers", json=kwargs)
    if response.status_code == 201:
        return {"id": str(response.json()["id"]), "first_name": response.json()["firstName"], "lastName": response.json()["lastName"], "email": response.json()["email"]}
    else:
        raise Exception("Error al crear el cliente")

async def update_customer(id: str, **kwargs) -> Dict:
    """Actualizar cliente completo."""
    try:
        validate_customer_data(kwargs, ["firstName", "lastName", "email", "phone"])
    except ModelValidationError as e:
        raise Exception(e)
    
    response = await FastAPI().put(f"{BASE_URL}/customers/{id}", json=kwargs)
    if response.status_code == 200:
        return {"id": id, "first_name": response.json()["firstName"], "lastName": response.json()["lastName"], "email": response.json()["email"]}
    else:
        raise Exception("Error al actualizar el cliente")

async def delete_customer(id: str) -> Dict:
    """Eliminar cliente por ID."""
    await FastAPI().delete(f"{BASE_URL}/customers/{id}")
    return {"message": "Cliente eliminado correctamente"}

@pytest.fixture
def customer():
    response = await FastAPI().get(BASE_URL + "/customers/123")
    return Customer.parse_raw(response.json())

class TestCustomer:
    def test_get_customer(self, customer):
        get_response = await customer.get()
        assert get_response["id"] == "123"
        assert get_response["first_name"] == "John"
        assert get_response["lastName"] == "Doe"
        assert get_response["email"] == "john.doe@example.com"

    def test_create_customer(self):
        response = await create_customer(first_name="Juan", last_name="Pérez")
        assert response["id"] == "123"
        assert response["first_name"] == "Juan"
        assert response["lastName"] == "Pérez"
        assert response["email"] == "juan.perez@example.com"

    def test_update_customer(self):
        response = await update_customer(123, first_name="Luis", last_name="García")
        assert response["id"] == "123"
        assert response["first_name"] == "Luis"
        assert response["lastName"] == "García"
        assert response["email"] == "luis.garcia@example.com"

    def test_delete_customer(self):
        await delete_customer(123)
        try:
            await customer.get()
            raise Exception("Test failed")
        except Exception as e:
            assert str(e) == "Cliente eliminado correctamente"
```