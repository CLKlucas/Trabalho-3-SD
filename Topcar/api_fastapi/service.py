from decimal import Decimal
from typing import Any

from api_fastapi.database import TopcarDatabase
from api_fastapi.exceptions import RecursoNaoEncontrado
from api_fastapi.schemas import ClienteEntrada, PedidoEntrada
from api_fastapi.serializers import decimal_texto, serializar_peca


class CatalogoTopcarService:
    def __init__(self, database: TopcarDatabase) -> None:
        self.database = database

    def listar_operacoes(self) -> dict[str, list[str]]:
        return {
            "operacoes": [
                "GET /api/pecas",
                "GET /api/pecas/{id}",
                "POST /api/clientes",
                "GET /api/clientes/{cpf}",
                "POST /api/pedidos",
                "GET /api/pedidos/{id}/total",
            ]
        }

    def listar_pecas(self) -> dict[str, list[dict[str, Any]]]:
        return {"pecas": [serializar_peca(peca) for peca in self.database.estoque.values()]}

    def buscar_peca(self, peca_id: int) -> dict[str, dict[str, Any]]:
        peca = self.database.estoque.get(peca_id)
        if peca is None:
            raise RecursoNaoEncontrado(f"Peca nao encontrada: {peca_id}")
        return {"peca": serializar_peca(peca)}

    def cadastrar_cliente(self, cliente: ClienteEntrada) -> dict[str, dict[str, Any]]:
        self.database.clientes[cliente.cpf] = {
            "cpf": cliente.cpf,
            "nome": cliente.nome,
            "idade": cliente.idade,
            "pedidos": [],
        }
        return {"cliente": self.database.clientes[cliente.cpf]}

    def consultar_cliente(self, cpf: str) -> dict[str, dict[str, Any]]:
        cliente = self.database.clientes.get(cpf)
        if cliente is None:
            raise RecursoNaoEncontrado(f"Cliente nao encontrado: {cpf}")
        return {"cliente": cliente}

    def criar_pedido(self, pedido_entrada: PedidoEntrada) -> dict[str, Any]:
        cliente = self.database.clientes.get(pedido_entrada.cpf)
        if cliente is None:
            raise RecursoNaoEncontrado(f"Cliente nao cadastrado: {pedido_entrada.cpf}")

        itens = []
        total = Decimal("0")
        for item_entrada in pedido_entrada.itens:
            peca = self.database.estoque.get(item_entrada.pecaId)
            if peca is None:
                raise RecursoNaoEncontrado(f"Peca nao encontrada: {item_entrada.pecaId}")

            quantidade = item_entrada.quantidade
            valor_unitario = peca["valor"]
            desconto_unitario = valor_unitario * item_entrada.descontoPercentual / Decimal("100")
            valor_total = (valor_unitario - desconto_unitario) * quantidade
            desconto_total = desconto_unitario * quantidade
            total += valor_total

            itens.append(
                {
                    "peca": serializar_peca(peca),
                    "quantidade": quantidade,
                    "valorTotal": decimal_texto(valor_total),
                    "desconto": decimal_texto(desconto_total),
                }
            )

        pedido = {"id": self.database.proximo_pedido_id(), "itens": itens}
        self.database.pedidos[pedido["id"]] = pedido
        cliente["pedidos"].append(pedido)

        return {"pedido": pedido, "total": decimal_texto(total)}

    def calcular_total_pedido(self, pedido_id: int) -> dict[str, Any]:
        pedido = self.database.pedidos.get(pedido_id)
        if pedido is None:
            raise RecursoNaoEncontrado(f"Pedido nao encontrado: {pedido_id}")

        total = sum(Decimal(item["valorTotal"]) for item in pedido["itens"])
        return {"pedidoId": pedido_id, "total": decimal_texto(total)}
