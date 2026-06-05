from typing import Any

from fastapi import FastAPI, HTTPException

from api_fastapi.database import database
from api_fastapi.exceptions import RecursoNaoEncontrado
from api_fastapi.schemas import ClienteEntrada, PedidoEntrada
from api_fastapi.service import (
    ClienteService,
    PecaService,
    PedidoService,
    listar_operacoes as listar_operacoes_service,
)


app = FastAPI(
    title="Topcar API",
    description="API do Trabalho 3 de Sistemas Distribuidos.",
    version="1.0.0",
)

peca_service = PecaService(database)
cliente_service = ClienteService(database)
pedido_service = PedidoService(database)


@app.get("/api/operacoes")
def listar_operacoes() -> dict[str, list[str]]:
    return listar_operacoes_service()


@app.get("/api/pecas")
def listar_pecas() -> dict[str, list[dict[str, Any]]]:
    return peca_service.listar_pecas()


@app.get("/api/pecas/{peca_id}")
def buscar_peca(peca_id: int) -> dict[str, dict[str, Any]]:
    try:
        return peca_service.buscar_peca(peca_id)
    except RecursoNaoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.post("/api/clientes", status_code=201)
def cadastrar_cliente(cliente: ClienteEntrada) -> dict[str, dict[str, Any]]:
    return cliente_service.cadastrar_cliente(cliente)


@app.get("/api/clientes/{cpf}")
def consultar_cliente(cpf: str) -> dict[str, dict[str, Any]]:
    try:
        return cliente_service.consultar_cliente(cpf)
    except RecursoNaoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.post("/api/pedidos", status_code=201)
def criar_pedido(pedido_entrada: PedidoEntrada) -> dict[str, Any]:
    try:
        return pedido_service.criar_pedido(pedido_entrada)
    except RecursoNaoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/api/pedidos/{pedido_id}/total")
def calcular_total_pedido(pedido_id: int) -> dict[str, Any]:
    try:
        return pedido_service.calcular_total_pedido(pedido_id)
    except RecursoNaoEncontrado as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
