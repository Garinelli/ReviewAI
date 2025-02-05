import json
from pika import ConnectionParameters, BlockingConnection

connection_params = ConnectionParameters(
    host='localhost',
    port=5672,
)


def message_to_parser_queue(link: str, user_telegram_id: int, task_id: str):
    with BlockingConnection(connection_params) as conn:
        with conn.channel() as ch:
            ch.queue_declare(queue='parser')

            body_ = json.dumps({
                "link": link,
                "user_tg_id": user_telegram_id,
                "task_id": task_id,
            })


            ch.basic_publish(
                exchange='',
                routing_key='parser',
                body=body_.encode('utf-8'),
            )
            print('[INFO] MESSAGE HAS BEEN PUBLISHED TO PARSER QUEUE')


if __name__ == '__main__':
    message_to_parser_queue(link='https://some.ru..', user_telegram_id=1, task_id='1')