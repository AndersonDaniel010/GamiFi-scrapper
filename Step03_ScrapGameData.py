from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import json

# Set the path to your WebDriver executable
driver_path = 'C:/Users/msi/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(executable_path=driver_path))
all_data = []
y = 1

with open('games.txt', 'r', encoding='utf-8') as file:
    # Iterate through each line in the file
    for line in file:
        try:
            # Navigate to the webpage with dynamic content
            url = 'https://gamefi.org/games/{}'.format(line.strip())
            driver.get(url)
            time.sleep(5)

            # Scroll to the end of the page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)

            page_source = driver.page_source

            soup = BeautifulSoup(page_source, "html.parser")

            # 1. Get JSON formatted hrefs
            hrefs = [json.dumps(a["href"]) for a in soup.find_all("a") if "href" in a.attrs]

            # 2. Get text inside the specified div
            div_text_elem = soup.find("div", class_="ce-paragraph cdx-block")
            if div_text_elem:
                div_text = div_text_elem.text
            else:
                div_text = None

            # 3. Get "Released On" data
            released_on_elem = soup.find("p", text="Released On:")
            if released_on_elem:
                released_on = released_on_elem.find_next("p").text
            else:
                released_on = None

            # 4. Get "Studio" data
            studio_elem = soup.find("p", text="Studio:")
            if studio_elem:
                studio = studio_elem.find_next("p").text
            else:
                studio = None

            # 5. Get the image source for the icon
            icon_div = soup.find("div", class_="absolute left-0 right-0 top-[236px]")
            if icon_div:
                icon_src = icon_div.find("img")["src"]
            else:
                icon_src = None

            # 6. Get the image source for the banner
            banner_div = soup.find("div", class_="h-[356px] w-full rounded-t-[4px] overflow-hidden bg-[#16181d] relative")
            if banner_div:
                banner_src = banner_div.find("img")["src"]
            else:
                banner_src = None

            # Create a list of data for each HTML file
            data = [
                [", ".join(hrefs), div_text, released_on, studio, icon_src, banner_src]
            ]

            # Append the data to the list of all data
            all_data.extend(data)

            print("Done game {}".format(y))
            y = y + 1
        except Exception as e:
            print(f"Error processing game {y}: {str(e)}")

# Define the CSV file path
csv_file = "Results/output.csv"

# Write all the collected data to the CSV file
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["JSON HREFs", "Div Text", "Released On", "Studio", "Icon Source", "Banner Source"])  # Header
    writer.writerows(all_data)

# Quit the WebDriver
driver.quit()