from locust import HttpLocust, TaskSet, task
from locust.clients import HttpSession

body = """{
  "organization_id": 3136845990,
  "price": 15000,
  "vat_factor": 0,
  "name": "Pols",
  "description": "arne"
}"""

class UserTasks(TaskSet):
  base_url = "https://85fopamqpf.execute-api.eu-west-1.amazonaws.com"

  @task
  def post(self):
    session = HttpSession(self.base_url)
    reservation_response = session.post('/prod/insert-product', data=body)


class WebsiteUser(HttpLocust):
  task_set = UserTasks
  host = ""
  min_wait=0
  max_wait=5000
