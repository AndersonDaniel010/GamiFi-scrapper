from bs4 import BeautifulSoup
import csv
import json

# Define a list of HTML file names
html_files = ["gamesHTML/game1.html", "gamesHTML/game2.html", "gamesHTML/game3.html","gamesHTML/game4.html"]

all_data = []

for html_file_path in html_files:
    # Read the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()


    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, "html.parser")

    # 1. Get JSON formatted hrefs
    hrefs = [json.dumps(a["href"]) for a in soup.find_all("a") if "href" in a.attrs]

    # 2. Get text inside the specified div
    div_text = soup.find("div", class_="ce-paragraph cdx-block").text

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

# Define the CSV file path
csv_file = "output.csv"

# Write all the collected data to the CSV file
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["JSON HREFs", "Div Text", "Released On", "Studio", "Icon Source", "Banner Source"])  # Header
    writer.writerows(all_data)