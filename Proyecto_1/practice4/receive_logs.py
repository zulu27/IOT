import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
channel = connection.channel()


channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Creamos una cola con nombre fijo y durable para que los mensajes se guarden si el receptor se cae
result = channel.queue_declare(queue='cola_persistente', durable=True)
queue_name = result.method.queue

# Bind the temporary queue to the 'logs' exchange
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()