```python
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
import pytest

# Generar el archivo fixtures y components
@pytest.fixture
def fixture_customer_base():
    return {"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com"}

pytest.mark.usefixtures("fixture_customer_base")

class CustomerBase(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    country: str

class CustomerCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    country: str

class CustomerUpdate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    birthDate: str
    country: str
    status: str
    subscribedNewsletter: bool

# Inicializar la aplicación FastAPI
app = FastAPI()

# Clase para guardar los datos del cliente en el banco de datos
class Customer:
    def __init__(self, id, firstName, lastName, email, country):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.country = country

# Clase para recuperar un cliente por ID desde el banco de datos
class CustomerRetrieve:
    def get(self, id: str) -> Customer:
        # Almacenar el cliente en el servicio de reposo
        return Customer(id=id, firstName="John", lastName="Doe", email="johndoe@example.com", country="EE. UU.")

# Clase para crear un nuevo cliente al guardarlo en el reposo
class CustomerCreateService:
    def __init__(self):
        self.customer_repository = {}

    async def save(self, customer: CustomerBase) -> Customer:
        # Almacenar el cliente en el servicio de reposo
        return Customer(id=customer.id, **customer)

# Clase para recuperar un cliente por ID del reposo
class CustomerRetrieveService:
    def get(self, id: str) -> Customer:
        # Buscar el cliente en el reposo y devolverlo
        if not self.customer_repository.get(id):
            raise Exception(f"Cliente no encontrado con ID {id}")
        return Customer.from_dict(self.customer_repository[id])

# Clase para actualizar un cliente al guardarlo en el reposo
class CustomerUpdateService:
    def __init__(self):
        self.customer_repository = {}

    async def update(self, customer_id: str, data: CustomerUpdate) -> Customer:
        # Buscar el cliente por ID y actualizar sus datos
        if not self.customer_repository.get(customer_id):
            raise Exception(f"Cliente no encontrado con ID {customer_id}")
        return Customer.from_dict(data)

# Clase para eliminar un cliente al guardarlo en el reposo
class CustomerDeleteService:
    def __init__(self):
        self.customer_repository = {}

    async def delete(self, customer_id: str) -> None:
        # Eliminar el cliente por ID del reposo
        if not self.customer_repository.get(customer_id):
            raise Exception(f"Cliente no encontrado con ID {customer_id}")

# Clase para crear un servicio de reposo para obtener clientes
class CustomerService:
    def __init__(self, customer_create_service: CustomerCreateService, customer_update_service: CustomerUpdateService, customer_delete_service: CustomerDeleteService) -> None:
        self.customer_create_service = customer_create_service
        self.customer_update_service = customer_update_service
        self.customer_delete_service = customer_delete_service

    async def get(self, path: str, request: Request) -> list[Customer]:
        # Recuperar los datos de clientes utilizando el servicio de reposo
        if not path.startswith("/customers"):
            raise Exception(f"El endpoint {path} no es válido")
        
        try:
            data = await self.customer_repository.get(path)
            return [Customer.from_dict(data)]
        except Exception as e:
            # Devolver un error en caso de que haya un problema al recuperar el cliente
            print(e)

    async def post(self, path: str, request: Request) -> None:
        # Guardar los datos de clientes utilizando el servicio de reposo
        if not path.startswith("/customers"):
            raise Exception(f"El endpoint {path} no es válido")
        
        try:
            data = await self.customer_repository.post(path)
            customer_service = CustomerService(self.customer_create_service, self.customer_update_service, self.customer_delete_service)
            return [customer_service.save(customer) for customer in data]
        except Exception as e:
            # Devolver un error en caso de que haya un problema al guardar el cliente
            print(e)

    async def put(self, path: str, request: Request) -> None:
        # Actualizar los datos de clientes utilizando el servicio de reposo
        if not path.startswith("/customers"):
            raise Exception(f"El endpoint {path} no es válido")
        
        try:
            data = await self.customer_repository.post(path)
            customer_service = CustomerService(self.customer_create_service, self.customer_update_service, self.customer_delete_service)
            return [customer_service.update(data.id, data)]
        except Exception as e:
            # Devolver un error en caso de que haya un problema al actualizar el cliente
            print(e)

    async def delete(self, path: str) -> None:
        # Eliminar los datos de clientes utilizando el servicio de reposo
        if not path.startswith("/customers"):
            raise Exception(f"El endpoint {path} no es válido")
        
        try:
            data = await self.customer_repository.delete(path)
            customer_service = CustomerService(self.customer_create_service, self.customer_update_service, self.customer_delete_service)
            return [customer_service.delete(data.id)]
        except Exception as e:
            # Devolver un error en caso de que haya un problema al eliminar el cliente
            print(e)

# Generar fixtures y componentes para los servicios de reposo
def main():
    customer_base_service = CustomerCreateService()
    customer_update_service = CustomerUpdateService()
    customer_delete_service = CustomerDeleteService()

    fixture_customer_repository = {
        "customers/123": {"id": "1", "firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "country": "EE. UU."}
    }

    with pytest.fixture():
        customer_service = CustomerService(customer_create_service=customer_base_service, customer_update_service=customer_update_service, customer_delete_service=customer_delete_service)

        async def test_get_all_customers():
            # Verificar que se recopilen todos los clientes correctamente
            response = await customer_service.get("/customers", request={"Content-Type": "application/json"})
            assert len(response) == 1

        async def test_get_customer_by_id():
            # Verificar que se recupere un cliente correctamente por ID
            response = await customer_service.get("/customers/123", request={"Content-Type": "application/json"})
            assert isinstance(response, list)

        async def test_post_create_new_customer():
            # Crear un nuevo cliente con éxito
            data = {"firstName": "John", "lastName": "Doe", "email": "johndoe@example.com", "country": "EE. UU."}
            response = await customer_service.post("/customers", request={"Content-Type": "application/json"}, json=data)
            assert isinstance(response, list)

        async def test_put_update_customer():
            # Actualizar un cliente correctamente
            data = {"firstName": "Jane", "lastName": "Doe", "email": "janedoe@example.com"}
            response = await customer_service.put("/customers/123", request={"Content-Type": "application/json"}, json=data)
            assert isinstance(response, list)

        async def test_delete_customer():
            # Eliminar un cliente correctamente
            data = {"id": "1"}
            response = await customer_service.delete(data["id"], request={"Content-Type": "application/json"})
            assert isinstance(response, str)

if __name__ == "__main__":
    main()
```

Nota: La implementación del código es solo para ilustrar cómo se pueden crear los servicios de reposo y gestionar la aplicación con FastAPI. Debe adaptarse a las necesidades específicas de su proyecto.