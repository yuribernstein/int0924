from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 to 5 seconds between tasks

    @task
    def homepage(self):
        self.client.get("/")  # Simulates visiting the homepage

    @task
    def about_page(self):
        self.client.get("/about")  # Simulates visiting the About page
