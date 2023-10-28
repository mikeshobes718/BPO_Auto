from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import warnings
import urllib3

# Ignore specific category of warning
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)

def main():
    # Instantiate the WebDriver
    driver = webdriver.Chrome()

    try:
        # Navigate to the desired webpage
        driver.get('https://vendor.voxturappraisal.com/Account/Login')

        # Wait until the username element is present in the DOM, and is visible on the page
        username_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'Login.Username'))
        )

        # Enter data into the username element
        username_element.send_keys('401154')
        print('Data entered successfully in the username field')

        # Wait until the password element is present in the DOM, and is visible on the page
        password_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'Login.Password'))
        )

        # Enter data into the password element
        password_element.send_keys('Tr@vel2023')
        print('Data entered successfully in the password field')

        # Wait until the login button is present in the DOM, and is visible on the page
        login_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'BtnLogin'))
        )

        # Click the login button
        login_button.click()
        print('Login button clicked')

        # Wait until the verification field is present in the DOM, and is visible on the page
        verification_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'VerificationFieldName'))  # Replace 'VerificationFieldName' with the actual name attribute of the verification field
        )

        # Enter data into the verification field
        verification_field.send_keys('YourVerificationCodeHere')  # Replace 'YourVerificationCodeHere' with the actual verification code
        print('Verification code entered')

    except Exception as e:
        # If an exception occurs, print the exception
        print(f'An error occurred: {e}')

    finally:
        # Uncomment the line below if you want to close the browser automatically after entering the verification code
        # driver.quit()
        pass

if __name__ == "__main__":
    main()
