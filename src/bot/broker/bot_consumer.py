from pika import ConnectionParameters, BlockingConnection

connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


def process_message(ch, method, properties, body):
    print(f'Получено сообщение: {body.decode()}')

    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='bot')

            # Сообщения остаются в брокере

            # ch.basic_consume(
            #     queue='parser_messages',
            #     on_message_callback=process_message,
            # )

            # ch.basic_consume(
            #     queue='parser_messages',
            #     on_message_callback=process_message,
            #     auto_ack=True,
            # )

            ch.basic_consume(
                queue='bot',
                on_message_callback=process_message,
            )

            ch.start_consuming()


if __name__ == '__main__':
    main()
