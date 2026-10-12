
from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    date_of_birth: date
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=250)
    enrollment_date: Optional[date] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty.")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            value = value.strip()

            if value == "":
                return None

            if not value.replace("+", "").isdigit():
                raise ValueError(
                    "Phone must contain digits and an optional leading +."
                )

        return value
