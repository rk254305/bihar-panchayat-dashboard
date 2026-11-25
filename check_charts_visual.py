from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1440,1200')
driver = webdriver.Chrome(options=options)

try:
    driver.get('http://localhost:3000')
    time.sleep(2)
    
    # Scroll to the charts
    charts_el = driver.find_element("id", "chart-hero-comparison")
    driver.execute_script("arguments[0].scrollIntoView();", charts_el)
    time.sleep(1)
    
    # Take screenshot of the charts area
    driver.save_screenshot(r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b\charts_area_check.png")
    print("Screenshot saved to charts_area_check.png")
    
    # Check parent and legend elements
    card1 = driver.find_element("id", "chart-hero-progression").find_element("xpath", "./ancestor::div[contains(@class, 'editorial-card')]")
    card2 = driver.find_element("id", "chart-hero-comparison").find_element("xpath", "./ancestor::div[contains(@class, 'editorial-card')]")
    
    print("Card 1 text:\n", card1.text)
    print("\n---\nCard 2 text:\n", card2.text)
finally:
    driver.quit()
