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


class ReservationTaskSet(TaskSet):
    base_url = os.environ['host']

    @task
    def create_purchase(self):
        session = HttpSession(self.base_url)
        reservation_response = session.post('/api/v0.9/reservation/', data=reservation_body)


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
