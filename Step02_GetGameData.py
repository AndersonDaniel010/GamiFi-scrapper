from bs4 import BeautifulSoup
import csv

# Read the saved HTML file
with open('output_games.html', 'r', encoding='utf-8') as html_file:
    html_content = html_file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Create a list to store the extracted data
data_list = []

# Find all div elements that match the pattern
divs = soup.find_all('div', class_='rounded overflow-hidden h-full group p-[10px] transition-all duration-200 bg-lightDark-300 hover:bg-[#2e3239] relative')

# Iterate through the div elements and extract information
for index, div in enumerate(divs, start=1):
    # Extract the game title from the img alt attribute
    img_elem = div.find('img', class_='object-cover w-full group-hover:scale-110 transition-all')
    if img_elem:
        game_title = img_elem.get('alt', 'N/A')
    else:
        game_title = "N/A"

    # Extract the image source
    img_src = img_elem.get('src', 'N/A')

    # Extract the category
    category_elem = div.find('div', class_='truncate flex-1')
    if category_elem:
        category = category_elem.get('title', 'N/A')
    else:
        category = "N/A"

    # Extract the number of followers
    followers_elem = div.find('div', class_='flex md:hidden')
    if followers_elem:
        followers = followers_elem.get_text(strip=True)
    else:
        followers = "N/A"

    # Extract the status
    status_elem = div.find('span', class_='text-[#57f000]')
    if status_elem:
        status = status_elem.get_text(strip=True)
    else:
        status = "N/A"

    # Append the extracted data to the list
    data_list.append([game_title, img_src, category, followers, status])

# Define the CSV file name
csv_file_name = 'Results/game_names_data.csv'

# Write the data to the CSV file
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write the header row
    writer.writerow(['Game Title', 'Image Source', 'Category', 'Followers', 'Status'])
    
    # Write the data rows
    writer.writerows(data_list)

print(f'Data has been saved to {csv_file_name}.')