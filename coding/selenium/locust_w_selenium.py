# this script is an example of how to use Selenium with Locust
# Do not run it, as google prohibits usage of automated tools
# This script is for educational purposes only

from locust import User, task, events, between
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import os
import time
import requests

class SeleniumUser(User):
    wait_time = between(1, 3)  # Wait between tasks

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = None

    def on_start(self):
        """Initialize the Selenium WebDriver."""
        self.driver = webdriver.Chrome()

    def on_stop(self):
        """Quit the WebDriver when the test stops."""
        if self.driver:
            self.driver.quit()

    @task
    def search_google(self):
        """Simulate a Google search and save images from the first link."""
        try:
            # Navigate to Google
            self.driver.get("https://www.google.com")
            
            # Search for a query
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys("News In Israel Today")
            search_box.send_keys(Keys.RETURN)

            # Wait for the page to load
            self.driver.implicitly_wait(5)

            # Click on the first link in the search results
            first_link = self.driver.find_element(By.CSS_SELECTOR, "h3")
            first_link.click()

            # Wait for the page to load
            time.sleep(5)

            # Find all images on the page
            images = self.driver.find_elements(By.TAG_NAME, "img")

            # Directory to save images
            os.makedirs("downloaded_images", exist_ok=True)

            # Download and save images
            for index, img in enumerate(images):
                src = img.get_attribute("src")
                if src and src.startswith("http"):
                    try:
                        response = requests.get(src, stream=True)
                        if response.status_code == 200:
                            with open(f"downloaded_images/image_{index}.jpg", "wb") as file:
                                for chunk in response.iter_content(1024):
                                    file.write(chunk)
                    except Exception as e:
                        print(f"Failed to download image {index}: {e}")

            print(f"Downloaded {len(images)} images.")

            # Go back to the search results page
            self.driver.back()

        except Exception as e:
            print(f"An error occurred: {e}")
