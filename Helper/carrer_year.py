from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from .utils import parse_page_source

def extract_career_years(driver):
    button = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/ul/li[5]/a")
    button.click()
    time.sleep(10)

    soup = parse_page_source(driver)

    # Extract the career highlights from the ul with class "careerPath"
    career_years = [li.text for li in soup.find_all('li', class_='careerYear')]

    # Extract table rows with match details from the tbody
    match_rows = soup.select('table.TBase tbody tr')

    # Prepare to store match details
    matches = []

    # Iterate over each row and extract data
    for row in match_rows:
        cells = row.find_all('td')
        
        if len(cells) > 1:  # Skip empty rows
            # Get the relevant details from each column
            number = cells[0].text.strip()
            date = cells[1].text.strip()
            promotion = cells[2].find('img')['alt'] if cells[2].find('img') else None
            match = cells[3].text.strip()

            # Store the data in a dictionary
            match_data = {
                'number': number,
                'date': date,
                'promotion': promotion,
                'match': match
            }
            
            matches.append(match_data)

    # Output extracted data
    print("-----------------------------------------------------------------------------")
    print("Career Years:", career_years)
    print("Matches:")
    for match in matches:
        print(match)
    print("-----------------------------------------------------------------------------")
    return career_years, matches
