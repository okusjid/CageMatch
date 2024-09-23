from Helper.utils import initialize_webdriver, load_url, parse_page_source, save_output, close_driver
from Helper.basev2 import extract_all_data
from Helper.base import extract_table_rows, extract_table
from Helper.carrer_year import extract_career_years
from Helper.nominations_awards import awards
from selenium.webdriver.common.by import By
import json
import concurrent.futures
import time

# Retry logic with backoff for failures
MAX_RETRIES = 2
INITIAL_SLEEP_TIME = 5  # Initial sleep time for retries

# Worker function for multithreading
def process_actor(actor, output_file):
    name = actor.get('name', '')
    
    if not name:
        print("No name found in JSON.")
        return
    
    retries = 0
    sleep_time = INITIAL_SLEEP_TIME
    combined_data = {'Actor': name}

    while retries < MAX_RETRIES:
        try:
            driver = initialize_webdriver()
            if not driver:
                print(f"Failed to initialize webdriver for {name}")
                return

            formatted_name = name.replace(" ", "+")
            # Visit the site using the extracted name
            url1 = f"https://www.cagematch.net/?id=2&view=workers&search={formatted_name}"
            print(url1)
            load_url(driver, url1)
            soup2 = parse_page_source(driver)
            table_contents = extract_table(soup2)
            site1_data = extract_table_rows(table_contents)
            combined_data['Basic Data'] = site1_data

            # Click button and extract detailed data
            try:
                button = driver.find_element(By.XPATH, "/html/body/div[3]/div[1]/div[3]/div/div[2]/div[3]/table/tbody/tr[2]/td[2]/a")
                button.click()
                time.sleep(5)
            except Exception as e:
                print(f"Error finding or clicking the button for {name}: {e}")
                raise

            soup1 = parse_page_source(driver)
            site2_data = extract_all_data(soup1)
            combined_data['Detailed Data'] = site2_data

            career_years, matches = extract_career_years(driver)
            combined_data['Career Years'] = career_years
            combined_data['Matches'] = matches

            nominations, awards_data = awards(driver)
            combined_data['Nominations'] = nominations
            combined_data['Awards'] = awards_data

            # Save output after each actor is processed
            save_output(output_file, combined_data)

            print(f"Successfully processed {name}")
            break  # Exit retry loop if successful

        except Exception as e:
            retries += 1
            print(f"Error processing actor {name}: {e}. Retrying {retries}/{MAX_RETRIES}...")
            time.sleep(sleep_time)
            sleep_time *= 2  # Exponential backoff for retries

        finally:
            close_driver(driver)
    
    if retries == MAX_RETRIES:
        print(f"Failed to process {name} after {MAX_RETRIES} retries.")


# Main function to visit both websites and consolidate data
def main():
    output_file = 'actor_output.json'

    # Load the JSON file containing the actor data
    try:
        with open('actor_data.json') as f:
            json_data = f.read()
    except Exception as e:
        print(f"Error loading actor data: {e}")
        return

    # Parse the JSON data
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}")
        return

    # Use ThreadPoolExecutor to process multiple actors concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_actor, actor, output_file) for actor in data]

        # Wait for all threads to complete and check for errors
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread execution: {e}")

if __name__ == "__main__":
    main()
