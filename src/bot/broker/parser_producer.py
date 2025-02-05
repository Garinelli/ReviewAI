import json
from pika import ConnectionParameters, BlockingConnection

connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


def message_to_preprocessing_queue(df_file_name):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='preprocessing')

            body_ = json.dumps({
                'df_file_name': df_file_name,
            })


            ch.basic_publish(
                exchange='',
                routing_key='preprocessing',
                body=body_.encode('utf-8'),
            )
            print('[INFO] MESSAGE HAS BEEN PUBLISHED TO preprocessing QUEUE')


if __name__ == '__main__':
    message_to_preprocessing_queue(link='https://some.ru..', user_telegram_id=1, task_id='1')