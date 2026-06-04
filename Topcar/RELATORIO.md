# Relatorio - Trabalho 3 FastAPI + RabbitMQ Topcar

## Objetivo

O Trabalho 3 reimplementa o servico remoto do Trabalho 2 usando uma API HTTP. A solucao substitui a comunicacao por RMI do trabalho anterior por endpoints REST implementados com FastAPI e adiciona comunicacao indireta por RabbitMQ.

## Tecnologias

- Servico: Python com FastAPI
- Servidor ASGI: Uvicorn
- Comunicacao indireta: RabbitMQ
- Cliente RabbitMQ Python: biblioteca `pika`
- Formato de dados: JSON
- Cliente 1: JavaScript, usando `fetch`
- Cliente 2: Java, usando `java.net.http.HttpClient`

## Atencao ao requisito do enunciado

O servico foi implementado em Python. Por isso, os clientes apresentados estao em JavaScript e Java, que sao linguagens diferentes da linguagem usada no servico.

Nao foram criadas classes de socket, servidores TCP manuais nem objetos RMI. A comunicacao indireta acontece por publicacao de eventos em uma exchange do RabbitMQ.

## Comunicacao indireta

O RabbitMQ atua como intermediario entre o servico FastAPI e consumidores de eventos. A API nao chama diretamente os consumidores; ela apenas publica eventos em uma exchange topica.

Fluxo:

```text
Cliente HTTP -> API FastAPI -> RabbitMQ -> Consumidor RabbitMQ
```

Exchange usada:

```text
topcar.eventos
```

Eventos publicados:

```text
cliente.cadastrado
pedido.criado
```

Quando um cliente e cadastrado, a API publica `cliente.cadastrado`. Quando um pedido e criado, a API publica `pedido.criado`. O consumidor em `consumers/rabbitmq_consumer.py` recebe esses eventos de forma assincrona e independente da API.

## Servicos remotos implementados

### Listar pecas

- Metodo HTTP: `GET`
- Endpoint: `/api/pecas`
- Retorno: lista de pecas cadastradas no catalogo.

### Buscar peca

- Metodo HTTP: `GET`
- Endpoint: `/api/pecas/{id}`
- Retorno: dados de uma peca especifica.

### Cadastrar cliente

- Metodo HTTP: `POST`
- Endpoint: `/api/clientes`
- Entrada:

```json
{
  "cpf": "12345678900",
  "nome": "Lucas",
  "idade": 22
}
```

- Retorno: cliente cadastrado.
- Evento publicado: `cliente.cadastrado`

### Consultar cliente

- Metodo HTTP: `GET`
- Endpoint: `/api/clientes/{cpf}`
- Retorno: cliente e seus pedidos associados.

### Criar pedido

- Metodo HTTP: `POST`
- Endpoint: `/api/pedidos`
- Entrada:

```json
{
  "cpf": "12345678900",
  "itens": [
    {
      "pecaId": 1,
      "quantidade": 2,
      "descontoPercentual": 5
    }
  ]
}
```

- Retorno: pedido criado e valor total.
- Evento publicado: `pedido.criado`

### Calcular total do pedido

- Metodo HTTP: `GET`
- Endpoint: `/api/pedidos/{id}/total`
- Retorno: identificador do pedido e total calculado.

## Interacao cliente-servidor

O servidor FastAPI fica em execucao na porta `8000`. Os clientes JavaScript e Java enviam requisicoes HTTP para os endpoints da API e exibem as respostas JSON recebidas.

## Organizacao do codigo

- `api_fastapi/main.py`: define as rotas HTTP e traduz erros do servico para respostas HTTP.
- `api_fastapi/schemas.py`: define os modelos de entrada validados pelo FastAPI.
- `api_fastapi/service.py`: contem as regras de negocio do catalogo, clientes e pedidos.
- `api_fastapi/database.py`: mantem o estoque, clientes e pedidos em memoria.
- `api_fastapi/messaging.py`: publica eventos no RabbitMQ.
- `api_fastapi/serializers.py`: converte valores internos para JSON de resposta.
- `api_fastapi/exceptions.py`: define excecoes usadas pela camada de servico.
- `consumers/rabbitmq_consumer.py`: consumidor RabbitMQ para demonstrar a comunicacao indireta.
- `clients/javascript/topcar_client.js`: cliente JavaScript.
- `clients/java/TopcarClient.java`: cliente Java.
- `README.md`: instrucoes para instalar dependencias e executar o projeto.
