import os
import resource
import random
import json

from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession

resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 8192))

reservation_body = """{
    "tickets": [
        {"ticket_type_id": 4112466915, "event_id": 1277973654},
        {"ticket_type_id": 4112466915, "event_id": 1277973654}
    ]
}"""

checkout_body = """{
    "email": "havard+test@hoopla.no",
    "first_name": "Haavard",
    "last_name": "Lindset",
    "data": {
        "wants_sms": false,
        "wants_email": false
    },
    "return_url": "http://localhost:8765",
    "checkout_method": "creditcard"
}"""

class ReservationTaskSet(TaskSet):
    base_url = os.environ['host']

    @task
    def create_purchase(self):
        session = HttpSession(self.base_url)
        # self.client.post('/api/v0.9/reservation/', reservation_body)
        reservation_response = session.post('/api/v0.9/reservation/', data=reservation_body)

        if reservation_response.status_code != 201:
            return

        checkout_response = session.post('/api/v0.9/reservation/_checkout', data=checkout_body)

        if checkout_response.status_code != 200:
            return

        purchase = checkout_response.json()['purchase']
        completion_response = session.post('/api/v0.9/purchases/_complete', json.dumps(dict(
            purchase_id=purchase['purchase_id'],
            hash=purchase['completion_params']['hash'],
            processor=purchase['completion_params']['processor'],
            payment_ref=purchase['completion_params']['order_ref']
        )))


class DebugTaskSet(TaskSet):
    base_url = 'http://localhost:8080'

    @task
    def call_debug(self):
        print dir(self)
        print dir(self.client)
        self.client.get("/api/v0.1/_debug")


class ReservationLocust(HttpLocust):
    host = ''
    task_set = ReservationTaskSet
    min_wait = 0
    max_wait = 0
