import time
from selenium.webdriver.common.by import By
from Helper.utils import parse_page_source

def awards(driver):
     
        button = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[2]/ul/li[15]/a")
        button.click()
        time.sleep(5)
        soup3 = parse_page_source(driver)

        print("-----------------------------------------------------------------------------")
        print("Nominations for Superstar Of The Week")
        data = []

        # Find all preview boxes
        for box in soup3.find_all('div', class_='PreviewBox'):
            title = box.find('div', class_='PreviewBoxTitle').get_text(strip=True)
            contents = box.find('div', class_='PreviewBoxContents').find_all('div')[-1].get_text(strip=True)
            data.append({'Title': title, 'Contents': contents})

        # # Display the results
        # for entry in data:
        #     print(f"Title: {entry['Title']}\nContents: {entry['Contents']}\n")
        # print("-----------------------------------------------------------------------------")

        # Awards
        # Find the table and extract rows
        soup = parse_page_source(driver)
        table = soup.find('table')
        rows = table.find_all('tr')

        # Extract the table headers
        headers = [header.get_text(strip=True) for header in rows[0].find_all('td')]

        # Extract the table data
        data1 = []
        for row in rows[1:]:
            columns = row.find_all('td')
            data1.append({headers[i]: columns[i].get_text(strip=True) for i in range(len(headers))})

        # # Display the results
        # for entry in data:
        #     print(entry)

        return data,data1