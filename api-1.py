import boto3
import json
import threading
import time
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

escuela = {
    1: {'subject': 'Mathematics', 'teacher': 'Mr. Smith'},
    2: {'subject': 'Science', 'teacher': 'Ms. Johnson'},
    3: {'subject': 'History', 'teacher': 'Mr. Brown'},
    4: {'subject': 'English', 'teacher': 'Ms. Davis'},
    5: {'subject': 'Physical Education', 'teacher': 'Mr. Wilson'},
}

sqs = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/my-queue"

def consume_sqs():
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )
        messages = response.get('Messages', [])
        for message in messages:
            body = json.loads(message['Body'])
            if body['action'] == 'create_schedule':
                class_id = body['payload']['class_id']
                if class_id in escuela:
                    print(f"Nuevo horario para la clase {class_id}: {body['payload']}")

            # Eliminar el mensaje de la cola
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )

        time.sleep(2)

# Iniciar el consumidor SQS en un hilo separado
threading.Thread(target=consume_sqs, daemon=True).start()

class AllClasses(Resource):
    def get(self):
        return escuela

api.add_resource(AllClasses, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
