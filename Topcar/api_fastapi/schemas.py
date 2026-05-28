from decimal import Decimal

from pydantic import BaseModel, Field


class ClienteEntrada(BaseModel):
    cpf: str = Field(..., examples=["12345678900"])
    nome: str = Field(..., examples=["Lucas"])
    idade: int = Field(..., ge=0, examples=[22])


class ItemPedidoEntrada(BaseModel):
    pecaId: int = Field(..., gt=0, examples=[1])
    quantidade: int = Field(..., gt=0, examples=[2])
    descontoPercentual: Decimal = Field(default=Decimal("0"), ge=0, le=100, examples=[5])


class PedidoEntrada(BaseModel):
    cpf: str = Field(..., examples=["12345678900"])
    itens: list[ItemPedidoEntrada] = Field(..., min_length=1)
