# this script is an example of how to use Selenium with Locust
# Do not run it, as google prohibits usage of automated tools
# This script is for educational purposes only


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

def get_most_popular_movie():
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    # Open Google
    driver.get("https://www.goasdasdasdasdsaogle.com")

    # Wait for the page to load
    time.sleep(2)

    # Find the search bar and enter the query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Yellowstone TV Show")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(3)

    # Get the first result
    first_result = driver.find_element(By.CSS_SELECTOR, "h3").text

    # Get the second result
    second_result = driver.find_elements(By.CSS_SELECTOR, "h3")[1].text

    # Print the results to the console
    print("Search Result (First):", first_result)
    print("Search Result (Second):", second_result)




def signin_with_google():
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Open a website with Google Sign-In (example: YouTube)
        driver.get("https://www.youtube.com")

        # Wait for the page to load
        time.sleep(2)

        # Click on the Sign-In button
        signin_button = driver.find_element(By.LINK_TEXT, "Sign in")
        signin_button.click()

        # Wait for the Google Sign-In page to load
        time.sleep(3)

        # Enter email/phone number
        email_field = driver.find_element(By.ID, "identifierId")
        email_field.send_keys("yuri.bernstein@gmail.com")
        email_field.send_keys(Keys.RETURN)

        # Wait for the password field to load
        time.sleep(3)

        # Enter the password
        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys("your_password")
        password_field.send_keys(Keys.RETURN)

        # Wait for successful login
        time.sleep(5)

        print("Successfully signed in with Google!")

    except Exception as e:
        print("An error occurred during sign-in:", e)

    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    get_most_popular_movie()
    # signin_with_google()
