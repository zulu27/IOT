import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()

# We use a 'fanout' exchange to broadcast to everyone
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = "info: Hello World!"
channel.basic_publish(
    exchange='logs',
    routing_key='',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ))

print(f" [x] Sent {message}")
connection.close()