from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import os
from threading import Lock

# Initialize WebDriver
def initialize_webdriver():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        return None
    
# Load URL and wait for the page to load
def load_url(driver, url, wait_time=5):
    try:
        driver.get(url)
        time.sleep(wait_time)
    except Exception as e:
        print(f"Error loading URL {url}: {e}")

# Parse page source using BeautifulSoup
def parse_page_source(driver):
    try:
        return BeautifulSoup(driver.page_source, 'html.parser')
    except Exception as e:
        print(f"Error parsing page source: {e}")
        return None    

# Close WebDriver
def close_driver(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Error closing WebDriver: {e}")

# Save output to JSON file
def save_output(output_file, combined_data):
    lock = Lock()
    lock.acquire()
    try:
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.append(combined_data)
        with open(output_file, 'w') as f:
            json.dump(existing_data, f, indent=4)
    except Exception as e:
        print(f"Error saving output to file: {e}")
    finally:
        lock.release()