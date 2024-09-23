from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

# Initialize WebDriver
def initialize_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# Load URL and wait for the page to load
def load_url(driver, url, wait_time=5):
    driver.get(url)
    time.sleep(wait_time)

# Parse page source using BeautifulSoup
def parse_page_source(driver):
    return BeautifulSoup(driver.page_source, 'html.parser')

# Extract section based on title (for the first website)
def extract_section(soup, section_title):
    section_data = {}
    caption_div = soup.find('div', class_='Caption', string=section_title)
    if caption_div:
        info_table = caption_div.find_next('div', class_='InformationBoxTable')
        if info_table:
            rows = info_table.find_all('div', class_='InformationBoxRow')
            for row in rows:
                title = row.find('div', class_='InformationBoxTitle').text.strip()
                content = row.find('div', class_='InformationBoxContents').text.strip()
                section_data[title] = content
    return section_data

# Extract data from the first website
def extract_all_data(soup):
    data = {}
    data['General Data'] = extract_section(soup, 'General Data')
    data['Personal Data'] = extract_section(soup, 'Personal Data')
    data['Career Data'] = extract_section(soup, 'Career Data')
    return data

# Extract table data (for the second website)
def extract_table(soup):
    table_div = soup.find('div', class_='Table')
    if table_div:
        return table_div.find('div', class_='TableContents')
    return None

# Extract rows from the table (for the second website)
def extract_table_rows(table_contents):
    rows_data = []
    if table_contents:
        rows = table_contents.find_all('tr', class_='TRow1')
        for row in rows:
            row_data = {}
            columns = row.find_all('td')
            if len(columns) > 0:
                row_data['Gimmick'] = columns[1].text.strip()
                row_data['Birthday'] = columns[2].text.strip()
                row_data['Birthplace'] = columns[3].text.strip()
                row_data['Height'] = columns[4].text.strip()
                row_data['Weight'] = columns[5].text.strip()
                promotion = columns[6].find('img')
                if promotion:
                    row_data['Promotion'] = promotion.get('alt')
                row_data['Rating'] = columns[7].text.strip()
                row_data['Votes'] = columns[8].text.strip()
            rows_data.append(row_data)
    return rows_data

# Close WebDriver
def close_driver(driver):
    driver.quit()

# Main function to visit both websites and consolidate data
def main():
    # Load the JSON file containing the actor data
    with open('actor_data.json') as f:
        json_data = f.read()

    # Parse the JSON data
    data = json.loads(json_data)

    # Iterate through each actor in the JSON data
    for actor in data:
        name = actor.get('name', '')

        if not name:
            print("No name found in JSON.")
            continue

        driver = initialize_webdriver()

        combined_data = {}

        try:
            # Format the name for the URLs (replace spaces with "+")
            formatted_name = name.replace(" ", "+")

            # Visit the first site using the extracted name
            url1 = f"https://www.cagematch.net/?id=2&nr=17793&gimmick={formatted_name}"
            load_url(driver, url1)
            soup1 = parse_page_source(driver)
            site1_data = extract_all_data(soup1)
            combined_data['Site 1 Data'] = site1_data

            # Visit the second site using the extracted name
            url2 = f"https://www.cagematch.net/?id=2&view=workers&search={formatted_name}"
            load_url(driver, url2)
            soup2 = parse_page_source(driver)
            table_contents = extract_table(soup2)
            site2_data = extract_table_rows(table_contents)
            combined_data['Site 2 Data'] = site2_data

            # Check if any data was found on either site
            if not site1_data and not site2_data:
                print("No exact match found")
            else:
                # Output combined data as JSON
                json_output = json.dumps(combined_data, indent=4)
                print(json_output)

        finally:
            close_driver(driver)

if __name__ == "__main__":
    main()
