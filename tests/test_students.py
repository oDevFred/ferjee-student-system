import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

def test_create_student(client, test_db):
    response = client.post(
        "/students",
        json={
            "name": "João Silva",
            "rg": "12.345.678-9",
            "cpf": "12345678900",
            "address": "Rua das Flores, 123, São Paulo, SP",
            "phone": "11999999999"
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "João Silva",
        "rg": "12.345.678-9",
        "cpf": "12345678900",
        "address": "Rua das Flores, 123, São Paulo, SP",
        "phone": "11999999999"
    }

def test_create_student_duplicate_cpf(client, test_db):
    # Criar primeiro aluno
    client.post(
        "/students",
        json={
            "name": "João Silva",
            "rg": "12.345.678-9",
            "cpf": "12345678900",
            "address": "Rua das Flores, 123, São Paulo, SP",
            "phone": "11999999999"
        }
    )
    # Tentar criar outro com mesmo CPF
    response = client.post(
        "/students",
        json={
            "name": "Maria Souza",
            "rg": "98.765.432-1",
            "cpf": "12345678900",
            "address": "Avenida Brasil, 456, São Paulo, SP",
            "phone": "11888888888"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "CPF já cadastrado"