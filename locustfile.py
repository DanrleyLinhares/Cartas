from locust import task, FastHttpUser

class MyUser(FastHttpUser):
    @task
    def index(self):
        response = self.client.get("/group")

    @task
    def post(self):
        response = self.client.get("/post")

    @task
    def indexlink(self):
        response = self.client.get("/")