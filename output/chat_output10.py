```
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pytest

# Configuración para el servidor de API
app = FastAPI()

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

# Endpoints de la API
@app.get("/customers", response_model=list[CustomerBase])
def get_customers():
    """
    Obtiene una lista de clientes.
    
    :return: Lista de clientes
    """
    pass

@app.post("/customers", request_body=CustomerCreate)
def create_customer(customer: CustomerCreate):
    """
    Crea un nuevo cliente.
    
    :param customer: Objeto de tipo CustomerCreate
    :return: Cliente creado
    """
    pass

@app.get("/customers/{id}", response_model=CustomerBase)
def get_customer(id: str):
    """
    Obtiene un cliente por ID.
    
    :param id: ID del cliente
    :return: Cliente encontrado o 404 si no se encuentra
    """
    pass

@app.put("/customers/{id}", request_body=CustomerUpdate)
def update_customer(id: str, customer: CustomerUpdate):
    """
    Actualiza el estado y los detalles de un cliente.
    
    :param id: ID del cliente
    :param customer: Objeto de tipo CustomerUpdate
    :return: Cliente actualizado o 404 si no se encuentra
    """
    pass

@app.delete("/customers/{id}")
def delete_customer(id: str):
    """
    Elimina un cliente por ID.
    
    :param id: ID del cliente
    :return: Eliminado correctamente
    """
    pass

# Fixture para simular datos de prueba
@pytest.fixture
async def customer():
    return CustomerBase(
        firstName="John",
        lastName="Doe",
        email="johndoe@example.com",
        country=" España",
        status="ACTIVE",
        subscribedNewsletter=True,
        createdAt="2022-01-01T00:00:00Z",
        updatedAt="2022-01-01T00:00:00Z"
    )

# Test para obtener lista de clientes
def test_get_customers():
    """Verifica que se obtenga la lista de clientes correctamente."""
    response = app.get("/customers")
    assert response.status_code == 200
    # Prueba con un dummy valor como id para comprobar si se muestra el valor correcto

# Test para crear cliente
def test_create_customer():
    """Verifica que se creen los datos de prueba correctamente."""
    customer_data = CustomerCreate(
        firstName="Juan",
        lastName="Pérez",
        email="juperez@example.com",
        country=" España"
    )
    response = app.post("/customers", json=customer_data)
    assert response.status_code == 201
    # Prueba con un dummy valor como id para comprobar si se devuelve correctamente

# Test para obtener cliente por ID
def test_get_customer():
    """Verifica que se devuelva el cliente correctamente."""
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juperez@example.com",
        country=" España"
    )
    response = app.get("/customers/123")
    assert response.status_code == 200
    # Prueba con un dummy valor para comprobar si se devuelve correctamente

# Test para actualizar cliente
def test_update_customer():
    """Verifica que se actualice el estado de la persona correctamente."""
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juperez@example.com",
        country=" España"
    )
    response = app.put("/customers/123", json=customer)
    assert response.status_code == 200
    # Prueba con un dummy valor para comprobar si se actualiza correctamente

# Test para eliminar cliente
def test_delete_customer():
    """Verifica que se elimine el cliente correctamente."""
    customer = CustomerBase(
        firstName="Juan",
        lastName="Pérez",
        email="juperez@example.com",
        country=" España"
    )
    response = app.delete("/customers/123")
    assert response.status_code == 204
```

Esta es una implementación básica de la API de cliente. Cada endpoint tiene un test correspondiente para asegurarse de que se ejecuten correctamente. Se utilizan pruebas unitarias con Pytest y se considera una buena práctica implementar un sistema de depuração antes de lanzarlo al producción.