from decimal import Decimal
from typing import Any


def serializar_peca(peca: dict[str, Any]) -> dict[str, Any]:
    return {
        chave: decimal_texto(valor) if isinstance(valor, Decimal) else valor
        for chave, valor in peca.items()
    }


def decimal_texto(valor: Decimal) -> str:
    return f"{valor.quantize(Decimal('0.01'))}"
