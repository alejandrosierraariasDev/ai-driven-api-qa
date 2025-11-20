import pytest
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class CustomerCreate(BaseModel):
    """Customer create model"""
    firstName: str
    lastName: str
    email: str
    country: str

class Customer(BaseModel):
    """Customer model"""
    id: str
    firstName: str
    lastName: str
    email: str
    country: str
    status: str
    subscribedNewsletter: bool
    createdAt: str
    updatedAt: str

# Crear un modelo de respuesta base
class CustomerBase(BaseModel):
    """CustomerBase model"""
    id: str
    firstName: str
    lastName: str
    email: str
    country: str
    status: str
    subscribedNewsletter: bool
    createdAt: str
    updatedAt: str

# Crear un modelo de respuesta para eliminar un cliente
class CustomerDelete(BaseModel):
    """CustomerDelete model"""
    id: str

# Funciones de interacción
async def get_customer(id: str) -> Dict:
    """Obtener cliente por ID"""
    response = await app.get(f"/customers/{id}")
    return {
        "id": response.id,
        "firstName": response.firstName,
        "lastName": response.lastName,
        "email": response.email,
        "country": response.country
    }

async def create_customer(firstName: str, lastName: str, email: str, country: str) -> Dict:
    """Crear un nuevo cliente"""
    customer = CustomerCreate(**locals())
    await app.post("/customers", json=customer)
    return {
        "id": customer.id,
        "firstName": customer.firstName,
        "lastName": customer.lastName,
        "email": customer.email,
        "country": customer.country
    }

async def update_customer(id: str, firstName: str, lastName: str, email: str, country: str) -> Dict:
    """Actualizar un cliente completo"""
    customer = CustomerUpdate(**locals())
    await app.put("/customers/{id}", json=customer)
    return {
        "id": customer.id,
        "firstName": customer.firstName,
        "lastName": customer.lastName,
        "email": customer.email,
        "country": customer.country
    }

async def delete_customer(id: str) -> Dict:
    """Eliminar un cliente"""
    await app.delete(f"/customers/{id}")
    return {"message": "Cliente eliminado correctamente"}

# Clase de tests Pytest
class TestCustomer:
    def test_get_customer(self):
        response = get_customer("123e4567-e89b-12d3-a456-426655440000")
        assert response["id"] == "123e4567-e89b-12d3-a456-426655440000"
        assert response["firstName"] == "John"
        assert response["lastName"] == "Doe"

    def test_create_customer(self):
        response = create_customer("Jane", "Doe", "jane@example.com", "USA")
        assert response["id"] == "123e4567-e89b-12d3-a456-426655440000"
        assert response["firstName"] == "John"
        assert response["lastName"] == "Doe"
        assert response["email"] == "jane@example.com"
        assert response["country"] == "USA"

    def test_update_customer(self):
        response = update_customer("123e4567-e89b-12d3-a456-426655440000", "Jane", "Doe", "new_jane@example.com", "Canada")
        assert response["id"] == "123e4567-e89b-12d3-a456-426655440000"
        assert response["firstName"] == "John"
        assert response["lastName"] == "Doe"
        assert response["email"] == "new_jane@example.com"
        assert response["country"] == "Canada"

    def test_delete_customer(self):
        response = delete_customer("123e4567-e89b-12d3-a456-426655440000")
        assert response["message"] == "Cliente eliminado correctamente"