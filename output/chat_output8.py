```python
from fastapi import FastAPI
import pytest
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

# Inicializar la aplicación de API
app = FastAPI()

# Armar un modelo para representar una cliente
class Customer(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    country: str
    phone: str
    birthDate: datetime
    status: str
    subscribedNewsletter: bool
    createdAt: str
    updatedAt: str

# Definir los endpoints y sus respuestas requeridas
@app.get("/customers", response_model=list[Customer])
def get_customers():
    # Validar que la respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers:
        return {"message": "Error: No se encontraron clientes"}, 404
    
    # Crear fixtures para los campos obligatorios y códigos de respuesta
    fixture = {
        "id": "",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "country": "USA"
    }
    
    # Validar que el cuerpo de respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers:
        return {"message": "Error: No se encontraron clientes"}, 404
    
    return [Customer(**fixture) for customer in customers]

@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    # Validar que la respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers:
        return {"message": "Error: No se encontraron clientes"}, 404
    
    # Crear el objeto de cliente en la base de datos
    customer.id = str(UUID())
    customers.append(customer)
    
    # Validar que el cuerpo de respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers):
        return {"message": "Error: No se encontraron clientes"}, 404
    
    return customer

@app.get("/customers/{id}", response_model=Customer)
def get_customer(id: str):
    # Validar que la respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers:
        return {"message": "Error: No se encontraron clientes"}, 404
    
    # Buscar el cliente por ID en la base de datos
    for customer in customers:
        if str(customer.id) == id:
            return customer
    
    # Si no se encuentra el cliente, devolver un error 404
    return {"message": "Error: Cliente no encontrado"}

@app.put("/customers/{id}", response_model=Customer)
def update_customer(id: str, customer: Customer):
    # Validar que la respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers):
        return {"message": "Error: No se encontraron clientes"}, 404
    
    # Buscar el cliente por ID en la base de datos
    for customer in customers:
        if str(customer.id) == id:
            # Validar que los campos obligatorios estén completos
            if not all(customer.values()):
                return {"message": "Error: Campos obligatorios vacíos"}, 400
            
            # Actualizar el objeto de cliente en la base de datos
            customer.id = str(UUID())
            customers.append(customer)
            
            return customer
    
    # Si no se encuentra el cliente, devolver un error 404
    return {"message": "Error: Cliente no encontrado"}

@app.delete("/customers/{id}")
def delete_customer(id: str):
    # Validar que la respuesta sea una lista vacía o tenga al menos un cliente
    if not all(customers):
        return {"message": "Error: No se encontraron clientes"}, 404
    
    # Buscar el cliente por ID en la base de datos
    for customer in customers:
        if str(customer.id) == id:
            # Eliminar el objeto de cliente de la base de datos
            customers.remove(customer)
            
            return {"message": "Cliente eliminado correctamente"}
    
    # Si no se encuentra el cliente, devolver un error 404
    return {"message": "Error: Cliente no encontrado"}

# Testar los endpoints y respuestas requeridas
def test_get_all_customers():
    assert set([customer.id for customer in customers]) == set(["1234567890abcdef"])
    
    # Poner todos los campos obligatorios vacíos en el cuerpo de respuesta
    fixture = {
        "id": "",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "country": "USA"
    }
    
    assert set([customer.id for customer in customers]) == set(["1234567890abcdef"])
    
    return True

def test_create_customer():
    customer = Customer(**fixture)
    assert customer.id != ""
    
    # Poner todos los campos obligatorios vacíos en el cuerpo de respuesta
    fixture = {
        "id": "",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "country": "USA"
    }
    
    assert set([customer.id for customer in customers]) == set(["1234567890abcdef"])
    
    return True

def test_get_customer():
    # Poner todos los campos obligatorios vacíos en el cuerpo de respuesta
    fixture = {
        "id": "",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "country": "USA"
    }
    
    assert customers[0].id == str(fixture["id"])
    
    return True

def test_put_customer():
    # Poner todos los campos obligatorios vacíos en el cuerpo de respuesta
    fixture = {
        "id": "",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "country": "USA"
    }
    
    # Poner todos los campos obligatorios vacíos en el cuerpo de respuesta
    fixture.update({" firstName": "", " lastName": ""})
    
    assert customers[0].id == str(fixture["id"])
    
    return True

def test_delete_customer():
    # Poner todos los campos obligatorios vacíos en el cuerpo de respuesta
    fixture = {
        "id": "",
        "firstName": "John",
        "lastName": "Doe",
        "email": "johndoe@example.com",
        "country": "USA"
    }
    
    assert customers[0].id != str(fixture["id"])
    
    return True

# Iniciar la aplicación de API
if __name__ == "__main__":
    from pytest.runner import ArtilleryTestCase
    test = ArtilleryTestCase()

    # Lanzar los tests para cada endpoint y respuestas requeridas
    test.add_test("get_all_customers", view_func=test_get_all_customers)
    test.add_test("create_customer", view_func=test_create_customer)
    test.add_test("get_customer", view_func=test_get_customer)
    test.add_test("put_customer", view_func=test_put_customer)
    test.add_test("delete_customer", view_func=test_delete_customer)

    # Iniciar la aplicación de API
    app.run(debug=True)
```