import json
from pika import ConnectionParameters, BlockingConnection

connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


def message_to_bot_queue(df_file_name):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='bot')

            body_ = json.dumps({
                'df_file_name': df_file_name,
            })


            ch.basic_publish(
                exchange='',
                routing_key='bot',
                body=body_.encode('utf-8'),
            )
            print('[INFO] MESSAGE HAS BEEN PUBLISHED TO bot QUEUE')


if __name__ == '__main__':
    message_to_bot_queue(link='https://some.ru..', user_telegram_id=1, task_id='1')