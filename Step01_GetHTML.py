from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set the path to your WebDriver executable
driver_path = 'C:/Users/msi/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(executable_path=driver_path))

# Navigate to the webpage with dynamic content
url = 'https://gamefi.org/discovery'
driver.get(url)

for _ in range(10):
    time.sleep(2)

# Wait for the dynamic content to load (you may need to adjust the timeout)
time.sleep(5)

# Get the full HTML code from the page_source variable
html_content = driver.page_source

file_path = 'output_games.html'

# Open the file in write mode and save the HTML content
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

# Quit the WebDriver
driver.quit()






