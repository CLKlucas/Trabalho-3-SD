from decimal import Decimal
from typing import Any


class TopcarDatabase:
    def __init__(self) -> None:
        self.estoque = criar_estoque_inicial()
        self.clientes: dict[str, dict[str, Any]] = {}
        self.pedidos: dict[int, dict[str, Any]] = {}
        self._proximo_pedido_id = 1001

    def proximo_pedido_id(self) -> int:
        pedido_id = self._proximo_pedido_id
        self._proximo_pedido_id += 1
        return pedido_id


def criar_estoque_inicial() -> dict[int, dict[str, Any]]:
    return {
        1: {
            "id": 1,
            "classe": "Pneu",
            "nome": "Pneu aro 16",
            "valor": Decimal("420.00"),
            "dataFabricacao": "2025-01-15",
            "carro": {"nome": "Toyota Corolla", "ano": 2020, "modelo": "XEi"},
            "dimensoes": "205/55R16",
            "indiceTraction": "A",
        },
        2: {
            "id": 2,
            "classe": "Motor",
            "nome": "Motor 1.8 flex",
            "valor": Decimal("8500.00"),
            "dataFabricacao": "2024-11-04",
            "carro": {"nome": "Toyota Corolla", "ano": 2020, "modelo": "XEi"},
            "potenciaCv": 144,
            "torqueKgf": 17.5,
        },
        3: {
            "id": 3,
            "classe": "Bateria",
            "nome": "Bateria 60Ah",
            "valor": Decimal("530.00"),
            "dataFabricacao": "2025-02-20",
            "carro": {"nome": "Honda Civic", "ano": 2019, "modelo": "EXL"},
            "cca": 430,
            "tipoQuimica": "chumbo-acido",
        },
        4: {
            "id": 4,
            "classe": "Farol",
            "nome": "Farol LED esquerdo",
            "valor": Decimal("680.00"),
            "dataFabricacao": "2024-08-09",
            "carro": {"nome": "Chevrolet Onix", "ano": 2022, "modelo": "Premier"},
            "tipo": "baixo",
            "led": True,
        },
    }


database = TopcarDatabase()
