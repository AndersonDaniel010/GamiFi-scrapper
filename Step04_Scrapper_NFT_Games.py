from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import itertools
import re

driver_path = 'C:/Users/msi/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(executable_path=driver_path))
# Open the main page

working_links = []

with open('games.txt', 'r', encoding='utf-8') as file:
    game_names = file.read().splitlines()

# Define stopwords
stopwords = {}

for name in game_names:
    search_combinations = set()  # Using a set to prevent duplicates

    # Remove hyphens and spaces
    name_without_hyphens = name.replace("-", "")
    name_with_spaces = name.replace("-", " ")

    # Add variations in a specific order
    search_combinations.add(name)  # Original name
    search_combinations.add(name_without_hyphens)  # Name without hyphens
    search_combinations.add(name_with_spaces)  # Name with spaces

    # Split words based on spaces
    words = name_without_hyphens.split()
    for r in range(1, len(words) + 1):
        word_combinations = itertools.combinations(words, r)
        for combo in word_combinations:
            search_combinations.add(" ".join(combo))

    # Add individual words separately
    words = name_without_hyphens.split()
    for word in words:
        search_combinations.add(word)

    for combo in search_combinations:
        try:
            # Navigate to the link
            page_link = "https://gamefi.org/nft/collection/{}".format(combo)
            driver.get(page_link)

            # Check if "Collection not found" message is present
            not_found_message = driver.find_element(By.XPATH, "//*[text()='Collection not found']")

        except NoSuchElementException:
            # Handle the case when the message is not found, i.e., the collection exists
            # You can perform actions on the page here
            working_links.append(page_link)
            break  # Break the loop when a result is found

    else:
        # This block is executed when no result is found for any combination
        working_links.append("NULL")  # Add "NULL" to indicate no result

# Close the browser
driver.quit()

df = pd.DataFrame({'links': working_links})

# Export the DataFrame to a CSV file
df.to_csv('Results/working_links.csv', index=False)
