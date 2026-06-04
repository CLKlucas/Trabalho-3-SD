import json
import os

import pika


RABBITMQ_HOST = os.getenv("TOPCAR_RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("TOPCAR_RABBITMQ_PORT", "5672"))
EXCHANGE = os.getenv("TOPCAR_RABBITMQ_EXCHANGE", "topcar.eventos")
QUEUE = os.getenv("TOPCAR_RABBITMQ_QUEUE", "topcar.eventos.console")
BINDING_KEY = os.getenv("TOPCAR_RABBITMQ_BINDING_KEY", "#")


def main() -> None:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=BINDING_KEY)

    print(f"Consumidor aguardando eventos em {EXCHANGE} / {QUEUE}")
    print("Pressione Ctrl+C para parar.")

    def on_message(channel, method, properties, body) -> None:
        event = json.loads(body.decode("utf-8"))
        print()
        print(f"Evento recebido: {method.routing_key}")
        print(json.dumps(event, indent=2, ensure_ascii=False))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
