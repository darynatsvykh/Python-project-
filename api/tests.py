from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SignupTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_signup(self):
        self.browser.get(self.live_server_url + "/signup/")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys("testuser")

        self.browser.find_element(By.NAME, "username").send_keys("testcase")
        self.browser.find_element(By.NAME, "name").send_keys("test")
        self.browser.find_element(By.NAME, "surname").send_keys("case")
        self.browser.find_element(By.NAME, "email").send_keys("testcase@example.com")
        self.browser.find_element(By.NAME, "dob").send_keys("01-01-2001")
        self.browser.find_element(By.NAME, "password").send_keys("testcase123")
        self.browser.find_element(By.NAME, "ConfirmPassword").send_keys("testcase123")


        self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

   
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("/login/")
        )

 class LoginTest(LiveServerTestCase):
     def setUp(self):
        self.browser = webdriver.Chrome()
    def test_successful_login():
    # Find the username and password fields and enter valid credentials
    username_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='password']")
    
    username_input.send_keys("your-username")  # Replace with actual username for testing
    password_input.send_keys("your-password")  # Replace with actual password for testing

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the page to load (adjust the time if needed)
    time.sleep(3)

    # Verify that the user is redirected to the main page
    assert "Main Page" in driver.title  # Adjust this check based on your actual page title
    print("Login test passed successfully!")

def test_failed_login():
    # Find the username and password fields and enter invalid credentials
    username_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='username']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='password']")
    
    username_input.send_keys("wrong-username")
    password_input.send_keys("wrong-password")

    # Find and click the login button
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the error message to appear
    time.sleep(3)

    # Check if the error message is displayed
    error_message = driver.find_element(By.CSS_SELECTOR, ".error")
    assert error_message.is_displayed()
    print("Error message displayed, login test failed as expected.")

# Run the test
test_failed_login()

def test_redirect_after_login():
    # Assuming you're already logged in from a previous test
    # Check if the user is redirected to the main page
    driver.get("http://127.0.0.1:8080/login")  # Make sure to reload the login page

    time.sleep(3)
    # Check if the URL contains 'main' or some unique identifier
    assert "main" in driver.current_url  # Adjust the check to match your actual redirect URL
    print("Redirection after login test passed.")

driver.quit()
     
