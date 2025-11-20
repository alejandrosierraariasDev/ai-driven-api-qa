Primero, creamos un archivo `requirements.txt` con las dependencias necesarias:

```bash
pip freeze > requirements.txt
```

Luego, podemos crear el archivo `openapi.yaml` y agregar el contenido proporcionado:

```yml
openapi: 3.0.3
info:
  title: Customer API
  version: 1.0.0
  description: API CRUD para gestionar clientes.

servers:
  - url: http://localhost:8080

paths:
  /customers:
    get:
      summary: Obtener lista de clientes
      responses:
        '200':
          description: Lista de clientes
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Customer'

    post:
      summary: Crear un cliente nuevo
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomerCreate'
      responses:
        '201':
          description: Cliente creado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'

  /customers/{id}:
    get:
      summary: Obtener cliente por ID
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Cliente encontrado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'
        '404':
          description: Cliente no encontrado

    put:
      summary: Actualizar cliente completo
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CustomerUpdate'
      responses:
        '200':
          description: Cliente actualizado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Customer'

    delete:
      summary: Eliminar cliente por ID
      parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Eliminado correctamente

components:
  schemas:
    CustomerBase:
      type: object
      required:
        - firstName
        - lastName
        - email
        - country
      properties:
        id:
          type: string
          format: uuid
        firstName:
          type: string
        lastName:
          type: string
        email:
          type: string
          format: email
        phone:
          type: string
          nullable: true
        birthDate:
          type: string
          format: date
          nullable: true
        country:
          type: string
        status:
          type: string
          enum: [ACTIVE, INACTIVE, SUSPENDED]
        subscribedNewsletter:
          type: boolean
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    Customer:
      allOf:
        - $ref: '#/components/schemas/CustomerBase'

    CustomerCreate:
      allOf:
        - $ref: '#/components/schemas/CustomerBase'
      required:
        - firstName
        - lastName
        - email
        - country

    CustomerUpdate:
      type: object
      properties:
        firstName:
          type: string
        lastName:
          type: string
        email:
          type: string
        phone:
          type: string
        birthDate:
          type: string
          format: date
        country:
          type: string
        status:
          type: string
          enum: [ACTIVE, INACTIVE, SUSPENDED]
        subscribedNewsletter:
          type: boolean

    CustomerUpdateNested:
      allOf:
        - $ref: '#/components/schemas/CustomerBase'
        - $ref: '#/components/schemas/CustomerCreate'

    CustomerDelete:
      allOf:
        - $ref: '#/components/schemas/CustomerBase'
```

Luego, creamos un archivo `test.py` con las pruebas:

```python
from fastapi.testclient import TestClient
import pytest

class CustomerTest:
    @pytest.fixture
    def client(self):
        test_client = TestClient(FastAPI())

    def test_get_customers(self, client):
        response = client.get("/customers")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_create_customer(self, client):
        response = client.post("/customers", json={"firstName": "Juan", "lastName": "Diaz"})
        assert response.status_code == 201

    def test_get_customer_by_id(self, client):
        response = client.get(f"/customers/{client.client.base_path}/1")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_update_customer(self, client):
        customer = {"firstName": "Juan", "lastName": "Diaz"}
        response = client.put(f"/customers/1", json=customer)
        assert response.status_code == 200

    def test_update_customer_nested(self, client):
        customer = {"firstName": "Juan", "lastName": "Diaz"}
        new_customer = {"firstName": "Jose", "lastName": "Garcia"}
        response = client.put(f"/customers/1/update", json=new_customer)
        assert response.status_code == 200
        assert all(item in response.json() for item in customer)

    def test_delete_customer(self, client):
        response = client.delete("/customers/1")
        assert response.status_code == 204

if __name__ == "__main__":
    pytest.main()
```

Espero que esto te ayude a implementar tus pruebas. Recuerda agregar las dependencias de Pytest y FastAPI según sea necesario, además de los fixtures necesarios para cada endpoint.