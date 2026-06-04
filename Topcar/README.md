# Topcar - Trabalho 3 FastAPI + RabbitMQ

Projeto da disciplina de Sistemas Distribuidos.

Esta versao reimplementa o servico remoto do Trabalho 2 como uma API HTTP usando FastAPI. Alem da comunicacao direta cliente-servidor por REST, o projeto tambem usa comunicacao indireta com RabbitMQ para publicar eventos do dominio.

## Precisa de extensao?

Nao precisa de extensao obrigatoria na IDE. O que precisa instalar sao dependencias Python:

- `fastapi`
- `uvicorn`
- `pika`

Extensoes como Python, Pylance ou REST Client no VS Code ajudam, mas sao opcionais.

## Estrutura

```text
api_fastapi/main.py        Rotas HTTP da API FastAPI
api_fastapi/schemas.py     Modelos de entrada das requisicoes
api_fastapi/service.py     Regras de negocio do catalogo Topcar
api_fastapi/database.py    Dados em memoria usados pela API
api_fastapi/messaging.py   Publicacao de eventos no RabbitMQ
api_fastapi/serializers.py Formatacao das respostas JSON
api_fastapi/exceptions.py  Excecoes da camada de servico
consumers                  Consumidor RabbitMQ de demonstracao
clients/javascript         Cliente em JavaScript
clients/java               Cliente em Java
RELATORIO.md               Relatorio resumido dos servicos remotos
```

## Instalar dependencias

No PowerShell, dentro da pasta `Topcar`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se nao quiser criar ambiente virtual:

```powershell
python -m pip install -r requirements.txt
```

## Executar servidor

```powershell
uvicorn api_fastapi.main:app --reload
```

A API fica disponivel em:

```text
http://localhost:8000/api
```

A documentacao automatica do FastAPI fica em:

```text
http://localhost:8000/docs
```

## RabbitMQ

O RabbitMQ e usado para comunicacao indireta. A API publica eventos em uma exchange topica chamada `topcar.eventos`.
Por padrao, a publicacao fica desabilitada para permitir testar a API sem precisar subir o broker.

Eventos publicados:

```text
cliente.cadastrado
pedido.criado
```

Se voce tiver Docker instalado, suba o RabbitMQ com:

```powershell
docker compose up -d
```

Painel de administracao:

```text
http://localhost:15672
usuario: guest
senha: guest
```

Para habilitar a publicacao de eventos na API:

```powershell
$env:TOPCAR_RABBITMQ_ENABLED = "true"
uvicorn api_fastapi.main:app --reload
```

Em outro terminal, rode o consumidor:

```powershell
.\.venv\Scripts\Activate.ps1
python consumers\rabbitmq_consumer.py
```

Fluxo esperado:

```text
Cliente -> FastAPI -> RabbitMQ -> consumidor de eventos
```

## Teste automatico

Com as dependencias instaladas, rode:

```powershell
python tests\api_smoke_test.py
```

Esse teste usa a API em memoria e nao exige RabbitMQ ativo.

## Endpoints

| Metodo | Caminho | Descricao |
| --- | --- | --- |
| GET | `/api/operacoes` | Lista as operacoes disponiveis |
| GET | `/api/pecas` | Lista as pecas do catalogo |
| GET | `/api/pecas/{id}` | Busca uma peca por id |
| POST | `/api/clientes` | Cadastra um cliente |
| GET | `/api/clientes/{cpf}` | Consulta um cliente por CPF |
| POST | `/api/pedidos` | Cria um pedido |
| GET | `/api/pedidos/{id}/total` | Calcula o total de um pedido |

## Exemplos de JSON

Cadastrar cliente:

```json
{
  "cpf": "12345678900",
  "nome": "Lucas",
  "idade": 22
}
```

Criar pedido:

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

## Clientes

Como o servico agora e Python/FastAPI, os clientes usados para atender ao enunciado estao em linguagens diferentes: JavaScript e Java.

Cliente JavaScript com Node.js 18 ou superior:

```powershell
node clients\javascript\topcar_client.js
```

Cliente Java:

```powershell
javac -d target\java-client clients\java\TopcarClient.java
java -cp target\java-client TopcarClient
```

Para apontar os clientes para outra porta, defina `TOPCAR_API_URL`:

```powershell
$env:TOPCAR_API_URL = "http://localhost:8000/api"
node clients\javascript\topcar_client.js
```
