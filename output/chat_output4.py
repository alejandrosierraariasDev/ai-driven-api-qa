```python
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pytest
from unittest.mock import patch, Mock
from typing import List, Dict
from fastapi.testclient import TestClient
from fastapi.requests import Request  # type: ignore

# Configura el FastAPI y sus componentes
app = FastAPI()

# Componente de Pydantic para las respuestas de la API
CustomerBase = BaseModel()
CustomerCreate = CustomerBase.copy()
CustomerUpdate = CustomerBase.copy()

# Clase de fixtures para cada endpoint
class TestCustomers(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    country: str

# Endpoint para obtener la lista de clientes
@app.get("/customers")
async def get_customers(request: Request):
    # Obtiene todos los clientes desde el backend
    response = await request.get_json()
    
    # Verifica si se obtuvieron los campos obligatorios y su tipo correcto
    if 'firstName' not in response or 'lastName' not in response or 'email' not in response:
        pytest.fail("Obligatorio: campo firstName")
    if 'country' not in response or not response['country'].startswith('http'):
        pytest.fail("Obligatorio: campo country")

    # Devuelve la lista de clientes
    return {"data": response["data"]}

# Endpoint para crear un nuevo cliente
@app.post("/customers")
async def create_customer(request: Request):
    data = await request.json()
    
    # Verifica si se proporcionó todos los campos obligatorios y su tipo correcto
    if not all(key in data for key in ["firstName", "lastName", "email", "country"]):
        pytest.fail("Obligatorio: campo firstName")
    if not isinstance(data["country"], str) or not data["country"].startswith("http"):
        pytest.fail("Obligatorio: campo country")

    # Crear el cliente desde el modelo
    customer = CustomerBase(data)

    # Devuelve un respuesta de respuesta 201
    return {"data": customer}

# Endpoint para obtener un cliente por ID
@app.get("/customers/{id}")
async def get_customer(request: Request, id: str):
    # Verifica si se proporcionó el ID obligatorio
    if not id:
        pytest.fail("Obligatorio: campo id")

    # Obtiene el cliente desde el backend
    response = await request.get_json()
    
    # Verifica si se obtuvieron los campos obligatorios y su tipo correcto
    if 'firstName' not in response or 'lastName' not in response or 'email' not in response:
        pytest.fail("Obligatorio: campo firstName")
    if 'country' not in response or not response['country'].startswith('http'):
        pytest.fail("Obligatorio: campo country")

    # Devuelve el cliente
    return {"data": response["data"]}

# Endpoint para actualizar un cliente
@app.put("/customers/{id}")
async def update_customer(request: Request, id: str):
    # Verifica si se proporcionó el ID obligatorio
    if not id:
        pytest.fail("Obligatorio: campo id")

    # Obtiene los campos obligatorios y su tipo correcto
    response = await request.get_json()
    
    # Verifica si se obtuvieron todos los campos obligatorios y su tipo correcto
    if 'firstName' not in response or 'lastName' not in response or 'email' not in response:
        pytest.fail("Obligatorio: campo firstName")
    if 'country' not in response or not response['country'].startswith('http'):
        pytest.fail("Obligatorio: campo country")

    # Actualiza el cliente desde el modelo
    customer = CustomerBase(data=response)
    
    # Devuelve un respuestas de respuesta 200
    return {"data": customer}

# Endpoint para eliminar un cliente por ID
@app.delete("/customers/{id}")
async def delete_customer(request: Request, id: str):
    # Verifica si se proporcionó el ID obligatorio
    if not id:
        pytest.fail("Obligatorio: campo id")

    # Obtiene los campos obligatorios y su tipo correcto
    response = await request.get_json()
    
    # Verifica si se obtuvieron todos los campos obligatorios y su tipo correcto
    if 'firstName' not in response or 'lastName' not in response or 'email' not in response:
        pytest.fail("Obligatorio: campo firstName")
    if 'country' not in response or not response['country'].startswith('http'):
        pytest.fail("Obligatorio: campo country")

    # Devuelve un respuestas de respuesta 204
    return {"data": None}
```

```python
import pytest
from fastapi.testclient import TestClient

# Clase para testear los diferentes endpoints
class CustomerTest:
    def test_get_customers(self):
        client = TestClient(app)
        response = client.get("/customers")
        
        # Verifica el código de respuesta
        assert response.status_code == 200
        
        # Verifica si se obtuvieron todos los campos obligatorios y su tipo correcto
        data = []
        for item in response.json():
            if 'firstName' not in item or 'lastName' not in item or 'email' not in item:
                pytest.fail("Obligatorio: campo firstName")
            if 'country' not in item or not item['country'].startswith('http'):
                pytest.fail("Obligatorio: campo country")
            
            data.append(item)
        
        # Verifica que se obtuvieron todos los campos obligatorios
        assert all(key in data for key in ["firstName", "lastName", "email", "country"])
        
    def test_create_customer(self):
        client = TestClient(app)
        response = client.post("/customers")
        
        # Verifica el código de respuesta
        assert response.status_code == 201
        
        # Verifica si se obtuvieron todos los campos obligatorios y su tipo correcto
        data = []
        for key, value in response.json().items():
            if 'firstName' not in value or 'lastName' not in value or 'email' not in value:
                pytest.fail("Obligatorio: campo firstName")
            if 'country' not in value or not value['country'].startswith('http'):
                pytest.fail("Obligatorio: campo country")
            
            data.append((key, value))
        
        # Verifica que se obtuvieron todos los campos obligatorios
        assert all(key in data for key in ["firstName", "lastName", "email", "country"])
        
    def test_get_customer(self):
        client = TestClient(app)
        response = client.get("/customers/12345")
        
        # Verifica el código de respuesta
        assert response.status_code == 200
        
        # Verifica si se obtuvieron todos los campos obligatorios y su tipo correcto
        data = []
        for key, value in response.json().items():
            if 'firstName' not in value or 'lastName' not in value or 'email' not in value:
                pytest.fail("Obligatorio: campo firstName")
            if 'country' not in value or not value['country'].startswith('http'):
                pytest.fail("Obligatorio: campo country")
            
            data.append((key, value))
        
        # Verifica que se obtuvieron todos los campos obligatorios
        assert all(key in data for key in ["firstName", "lastName", "email", "country"])
        
    def test_update_customer(self):
        client = TestClient(app)
        response = client.put("/customers/12345")
        
        # Verifica el código de respuesta
        assert response.status_code == 200
        
        # Verifica si se obtuvieron todos los campos obligatorios y su tipo correcto
        data = []
        for key, value in response.json().items():
            if 'firstName' not in value or 'lastName' not in value or 'email' not in value:
                pytest.fail("Obligatorio: campo firstName")
            if 'country' not in value or not value['country'].startswith('http'):
                pytest.fail("Obligatorio: campo country")
            
            data.append((key, value))
        
        # Verifica que se obtuvieron todos los campos obligatorios
        assert all(key in data for key in ["firstName", "lastName", "email", "country"])
        
    def test_delete_customer(self):
        client = TestClient(app)
        response = client.delete("/customers/12345")
        
        # Verifica el código de respuesta
        assert response.status_code == 204
        
        # Verifica si se obtuvo un respuestas
        data = []
        for key, value in response.json().items():
            if 'firstName' not in value or 'lastName' not in value or 'email' not in value:
                pytest.fail("Obligatorio: campo firstName")
            if 'country' not in value or not value['country'].startswith('http'):
                pytest.fail("Obligatorio: campo country")
            
            data.append((key, value))
        
        # Verifica que se eliminó correctamente
        assert "None" in response.json()
```