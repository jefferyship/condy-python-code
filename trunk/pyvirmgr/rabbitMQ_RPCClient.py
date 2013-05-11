#!/usr/bin/env python
import pika
import uuid
import simplejson as json
RABBITMQ_HOST='117.27.135.204'
RABBITMQ_PORT='30038'
class fullTerminalInfoRpcClient(object):
    def __init__(self):
        self.connection =pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST,port=int(RABBITMQ_PORT)))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, company_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        exchange_name='fullcrement_terminal'
        self.channel.basic_publish(exchange='',
                                   routing_key=exchange_name,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=str(company_id))
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

fibonacci_rpc = fullTerminalInfoRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call('1146')
jsonMap=json.loads(response)
print jsonMap['data'][0]['staff_name']
#print " [.] Got %r" % (response.decode('GBK'),)
