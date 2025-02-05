import time
import json

from pika import ConnectionParameters, BlockingConnection
from nn_producer import message_to_bot_queue

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
    message_to_bot_queue(df_file_name='5% отзывов накручены')


def main():
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='NN')

            ch.basic_consume(
                queue='NN',
                on_message_callback=process_message,
            )

            ch.start_consuming()


if __name__ == '__main__':
    main()
