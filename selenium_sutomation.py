from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # Login
    url = "YOUR_LOGIN_URL"
    driver.get(url)
    
    # Fill credentials (update these selectors)
    driver.find_element(By.ID, 'username').send_keys("your_username")
    driver.find_element(By.ID, 'password').send_keys("your_password")
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    
    # Wait for table to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'data-table'))
    )
    
    # Extract table
    rows = driver.find_elements(By.CSS_SELECTOR, '#data-table tr')
    data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if cells:
            data.append([cell.text for cell in cells])
    
    # Save to CSV
    pd.DataFrame(data).to_csv('output.csv', index=False)
    print(f"Saved {len(data)} rows")
    
except Exception as e:
    driver.save_screenshot('error.png')
    print(f"Error: {e}")
    
finally:
    driver.quit()