from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup

def group_odds(values, group_size=2):
        return [values[i:i + group_size] for i in range(0, len(values), group_size)]

def handle_click_and_scrape(driver, element):
    main_window = driver.current_window_handle
    element.click()  # Click the button to open a new window/tab
    time.sleep(2)  # Adjust as necessary
    # Switch to the new window/tab
    new_window = [window for window in driver.window_handles if window != main_window][0]
    driver.switch_to.window(new_window)
    
    # Perform your scraping here
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    wrap = soup.find_all('div', class_='m-table-cell-item')
    odds_values = []
    for element in wrap:
        odds_values.append(float(element.get_text()))

    grouped_odds = group_odds(odds_values)        
    
    # Close the new window and switch back
    driver.close()
    driver.switch_to.window(main_window)


def main():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.sportybet.com/int/sport/football')
    time.sleep(2)
    # Locate the buttons you want to click
    buttons = driver.find_elements(By.CLASS_NAME, "m-table-cell market-size")  # Adjust your selector
    
    threads = []
    for button in buttons:
        # Create a thread for each button click and scraping task
        thread = threading.Thread(target=handle_click_and_scrape, args=(driver, button))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()  # Wait for all threads to complete
    
    driver.quit()

if __name__ == "__main__":
    main()
