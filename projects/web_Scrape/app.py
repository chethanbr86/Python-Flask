import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Automatically manage ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open the IPL stats page
url = "https://www.iplt20.com/stats/2021"
driver.get(url)

# Wait for the table to load
try:
    table = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    
    # Extract headers
    headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, "th")]
    
    # Extract table rows
    data = []
    rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text.strip() for col in columns])

    # Create a Pandas DataFrame
    df = pd.DataFrame(data, columns=headers)

    # Save to Excel
    df.to_excel("ipl_stats_2021.xlsx", index=False)

    print("Data successfully saved to ipl_stats_2025.xlsx")

finally:
    driver.quit()
