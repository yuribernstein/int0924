from locust import HttpUser, User, task, between
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait between 1 to 5 seconds between tasks

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_execution_count = 0  # Counter to limit the task executions    

    @task
    def homepage(self):
        self.client.get("/")  # Simulates visiting the homepage

    @task
    def about_page(self):
        self.client.get("/systeminfo?metric=all")  



# class SeleniumUser(User):
#     wait_time = between(1, 3)  # Wait between tasks

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.driver = None
#         self.task_execution_count = 0  # Counter to limit the task executions

#     def on_start(self):
#         """Initialize the Selenium WebDriver."""
#         self.driver = webdriver.Chrome()

#     def on_stop(self):
#         """Quit the WebDriver when the test stops."""
#         if self.driver:
#             self.driver.quit()


#     @task
#     def open_systeminfo_ui(self):
#         if self.task_execution_count >= 5:  # Stop after 5 executions
#             self.environment.runner.quit()  # Signal Locust to stop
#             return

#         try:
#             # Navigate to the target UI
#             self.driver.get("http://localhost:8081")

#             # Interact with the UI elements
#             osinfo = self.driver.find_element(By.ID, "osinfo")
#             cpuinfo = self.driver.find_element(By.ID, "cpuinfo")
#             meminfo = self.driver.find_element(By.ID, "meminfo")
#             allinfo = self.driver.find_element(By.ID, "allinfo")
#             jsoninfo = self.driver.find_element(By.ID, "jsoninfo")

#             osinfo.click()
#             time.sleep(5)
#             cpuinfo.click()
#             time.sleep(5)
#             meminfo.click()
#             time.sleep(5)
#             allinfo.click()
#             time.sleep(5)
#             jsoninfo.click()
#             time.sleep(5)

#             self.task_execution_count += 1

#         except Exception as e:
#             print(f"An error occurred: {e}")
