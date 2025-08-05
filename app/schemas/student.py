from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
import re

class StudentCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    rg: str = Field(..., min_length=7, max_length=20)
    cpf: str = Field(..., min_length=11, max_length=14)
    address: str = Field(..., min_length=5, max_length=200)
    phone: str = Field(..., min_length=10, max_length=15)

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        # Remove pontuação do CPF (ex.: 123.456.789-00 -> 12345678900)
        cpf = re.sub(r"[^\d]", "", value)
        if len(cpf) != 11 or not cpf.isdigit():
            raise PydanticCustomError("invalid_cpf", "CPF deve conter exatamente 11 dígitos numéricos")
        return cpf

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        # Remove caracteres não numéricos (ex.: (11) 99999-9999 -> 11999999999)
        phone = re.sub(r"[^\d]", "", value)
        if len(phone) < 10 or not phone.isdigit():
            raise PydanticCustomError("invalid_phone", "Telefone deve conter pelo menos 10 dígitos numéricos")
        return phone

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "João Silva",
                "rg": "12.345.678-9",
                "cpf": "123.456.789-00",
                "address": "Rua das Flores, 123, São Paulo, SP",
                "phone": "(11) 99999-9999"
            }
        }
    }