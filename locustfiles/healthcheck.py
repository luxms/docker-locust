import os
import resource
import random
import json

from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession

resource.setrlimit(resource.RLIMIT_NOFILE, (8192, 8192))


class DebugTaskSet(TaskSet):
    base_url = os.environ['host']

    @task
    def call_debug(self):
        print dir(self)
        print dir(self.client)
        self.client.get("/api/v0.1/_healthcheck")


class ReservationLocust(HttpLocust):
    host = os.environ['host']
    task_set = DebugTaskSet
    min_wait = 0
    max_wait = 0
