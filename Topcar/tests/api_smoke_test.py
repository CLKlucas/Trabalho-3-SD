import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api_fastapi.main import app


def main() -> None:
    client = TestClient(app)

    assert client.get("/api/operacoes").status_code == 200
    assert client.get("/api/pecas").status_code == 200
    assert client.get("/api/pecas/1").status_code == 200

    cliente_response = client.post(
        "/api/clientes",
        json={"cpf": "12345678900", "nome": "Cliente Teste", "idade": 22},
    )
    assert cliente_response.status_code == 201

    pedido_response = client.post(
        "/api/pedidos",
        json={
            "cpf": "12345678900",
            "itens": [
                {"pecaId": 1, "quantidade": 2, "descontoPercentual": 5},
                {"pecaId": 3, "quantidade": 1},
            ],
        },
    )
    assert pedido_response.status_code == 201
    pedido_id = pedido_response.json()["pedido"]["id"]

    total_response = client.get(f"/api/pedidos/{pedido_id}/total")
    assert total_response.status_code == 200
    assert total_response.json()["total"] == "1328.00"

    consulta_response = client.get("/api/clientes/12345678900")
    assert consulta_response.status_code == 200

    print("Smoke test FastAPI passou.")


if __name__ == "__main__":
    main()
