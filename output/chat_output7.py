```python
# Import required libraries
from fastapi import FastAPI, Request
from pydantic import BaseModel
import pytest
from openapi_specification import OpenAPISpec, PathItem
from openapi_specification.components import Schemas, Schema
from openapi_specification.endpoints import (
    Endpoint,
    Method,
    ResponseSchema,
)
from openapi_specification.fixtures import fixtures
from openapi_specification.request_body import RequestBody
from openapi_specification.responses import Responses
from openapi_specification.responses_schema import ResponseSchemaType
from openapi_specification.test_config import test_config

# Define the FastAPI app
app = FastAPI()

# Define schemas for each endpoint
customer_base_schema = Schemas.CustomerBase()
customer_schema = Schemas.Customer()
customer_create_schema = Schemas.CustomerCreate()

# Define response schema types
response_types = {
    '200': ResponseSchemaType.CUSTOMER_LIST,
}

# Define request body for POST endpoint
request_body = RequestBody(
    required=True,
    content={
        'application/json': {
            'schema': customer_schema
        }
    }
)

# Define route for POST /customers

@app.post("/customers")
def create_customer(request: Request, customer_base_schema: CustomerBase):
    # Validate input data (not implemented in this example)
    return ResponseSchemaType.CUSTOMER_CREATED(customer_base_schema)
```

```python
# Define the test configuration for the application
test_config = OpenAPISpec(
    info={
        "title": "Customer API",
        "version": "1.0.0"
    },
    openapi: True,
    external_schemas=True,
    servers=[
        {"url": "http://localhost:8080"}
    ]
)

# Define fixtures for each endpoint
customer_base_fixtures = fixtures.CustomerBaseFixtures()
customer_schema_fixtures = fixtures.CustomerSchemaFixtures()
customer_create_fixtures = fixtures.CustomerCreateFixtures()

# Test the GET /customers endpoint

@pytest.mark.parametrize("schema, response_type", [
    (customer_base_schema, ResponseTypes["200"]),
    (customer_schema, ResponseTypes["200"])
])
def test_get_customer_endpoint(schema: Schemas.CustomerBase, response_type):
    # Send a request to the endpoint
    response = requests.get("/customers")

    # Check if the response is of expected type and content
    assert response.status_code == 200
    assert response.headers['Content-Type'] in ['application/json']
    for item in response.json():
        assert isinstance(item, Schema)
```

```python
# Define routes for GET /customers/{id}, PUT /customers/{id} and DELETE /customers/{id}
customer_id_fixtures = fixtures.CustomerIdFixtures()
customer_endpoint_fixtures = fixtures.CustomerEndpointFixtures()

@app.get("/customers/{id}")
def get_customer(id: str):
    # Validate id (not implemented in this example)
    return ResponseSchemaType.CUSTOMER_LIST

@app.put("/customers/{id}")
def update_customer(id: str, customer_schema: Schemas.Customer):
    # Validate input data
    return ResponseSchemaType.CUSTOMER_UPDATED(customer_schema)

@app.delete("/customers/{id}")
def delete_customer(id: str):
    # Validate id (not implemented in this example)
    return ResponseSchemaType.CUSTOMER_DEleted()
```

```python
# Define route for POST /customers

@pytest.mark.parametrize("request_body, response_type", [
    (request_body, ResponseTypes["201"]),
    (customer_create_schema, ResponseTypes["200"])
])
def test_post_customer_endpoint(request_body: RequestBody, response_type):
    # Send a request to the endpoint with valid data
    response = requests.post("/customers", json=request_body)

    # Check if the response is of expected type and content
    assert response.status_code == 201
    assert response.headers['Content-Type'] in ['application/json']
    for item in response.json():
        assert isinstance(item, Schema)
```

```python
# Define route for GET /customers/{id} with fixture

@pytest.mark.parametrize("customer_id_fixtures, expected_response_type", [
    (customer_id_fixtures[0], ResponseTypes["200"]),
    (customer_id_fixtures[1], ResponseTypes["404"])
])
def test_get_customer_endpoint_fixture(customer_id_fixtures):
    # Send a request to the endpoint
    response = requests.get(f"/customers/{customer_id_fixtures[0]}")

    # Check if the response is of expected type and content
    assert response.status_code == 200
    assert response.headers['Content-Type'] in ['application/json']
    for item in response.json():
        assert isinstance(item, Schema)
```

```python
# Define route for PUT /customers/{id} with fixture

@pytest.mark.parametrize("customer_id_fixtures, expected_response_type", [
    (customer_id_fixtures[0], ResponseTypes["200"]),
    (customer_id_fixtures[1], ResponseType.SUSPENDED)
])
def test_put_customer_endpoint_fixture(customer_id_fixtures):
    # Send a request to the endpoint
    response = requests.put(f"/customers/{customer_id_fixtures[0]}", json=customer_schema_fixtures[0])

    # Check if the response is of expected type and content
    assert response.status_code == 200
    assert response.headers['Content-Type'] in ['application/json']
    for item in response.json():
        assert isinstance(item, Schema)
```