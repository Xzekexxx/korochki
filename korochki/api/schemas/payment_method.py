from pydantic import BaseModel, Field, ConfigDict


class PaymentMethodCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class PaymentMethodResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
