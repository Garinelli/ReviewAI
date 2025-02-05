import time
import json

from pika import ConnectionParameters, BlockingConnection
from parser_producer import message_to_preprocessing_queue

connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


def process_message(ch, method, properties, body):
    body = body.decode('utf-8')
    body = json.loads(body)
    print(f'Получено сообщение: {body}')
    print(f'Получено сообщение: {type(body)}')

    ch.basic_ack(delivery_tag=method.delivery_tag)

    time.sleep(2)
    message_to_preprocessing_queue(df_file_name='df.csv')


def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='parser')

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
                queue='parser',
                on_message_callback=process_message,
            )

            ch.start_consuming()


if __name__ == '__main__':
    main()
