import json
import os
from datetime import datetime, timezone
from typing import Any


class RabbitMQPublisher:
    def __init__(self) -> None:
        self.enabled = os.getenv("TOPCAR_RABBITMQ_ENABLED", "false").lower() == "true"
        self.host = os.getenv("TOPCAR_RABBITMQ_HOST", "localhost")
        self.port = int(os.getenv("TOPCAR_RABBITMQ_PORT", "5672"))
        self.exchange = os.getenv("TOPCAR_RABBITMQ_EXCHANGE", "topcar.eventos")

    def publish(self, event_type: str, payload: dict[str, Any]) -> None:
        if not self.enabled:
            return

        import pika

        message = {
            "type": event_type,
            "occurredAt": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, port=self.port)
        )
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.exchange,
                exchange_type="topic",
                durable=True,
            )
            channel.basic_publish(
                exchange=self.exchange,
                routing_key=event_type,
                body=json.dumps(message).encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2,
                ),
            )
        finally:
            connection.close()


publisher = RabbitMQPublisher()
