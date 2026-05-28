const BASE_URL = process.env.TOPCAR_API_URL || "http://localhost:8080/api";

async function call(method, path, payload) {
  const options = {
    method,
    headers: {
      Accept: "application/json",
    },
  };

  if (payload) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(payload);
  }

  const response = await fetch(BASE_URL + path, options);
  const body = await response.json();
  return { status: response.status, body };
}

function show(title, result) {
  console.log(`\n${title} - HTTP ${result.status}`);
  console.log(JSON.stringify(result.body, null, 2));
  return result.body;
}

async function main() {
  show("Operacoes", await call("GET", "/operacoes"));
  show("Pecas", await call("GET", "/pecas"));
  show("Peca 2", await call("GET", "/pecas/2"));

  const cliente = { cpf: "98765432100", nome: "Cliente JavaScript", idade: 24 };
  show("Cadastrar cliente", await call("POST", "/clientes", cliente));

  const pedido = {
    cpf: "98765432100",
    itens: [
      { pecaId: 2, quantidade: 1, descontoPercentual: 10 },
      { pecaId: 4, quantidade: 1 },
    ],
  };
  const pedidoCriado = show("Criar pedido", await call("POST", "/pedidos", pedido));
  const pedidoId = pedidoCriado.pedido.id;
  show(`Total pedido ${pedidoId}`, await call("GET", `/pedidos/${pedidoId}/total`));
  show("Consultar cliente", await call("GET", "/clientes/98765432100"));
}

main().catch((error) => {
  console.error("Erro no cliente JavaScript:", error.message);
  process.exit(1);
});
