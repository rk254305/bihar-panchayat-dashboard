from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import shutil
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1440,1200')
driver = webdriver.Chrome(options=options)
driver.get('http://localhost:3000')
time.sleep(2)

# Find map container
map_box = driver.find_element(By.ID, 'bihar-map-wrapper')
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", map_box)
time.sleep(0.5)

# Screenshot default map
map_box.screenshot('current_live_map.png')

# Hover over Banka
banka = driver.find_element(By.CSS_SELECTOR, "path[data-district='Banka']")
actions = ActionChains(driver)
actions.move_to_element(banka).perform()
time.sleep(1)

map_box.screenshot('current_live_map_hover_banka.png')

driver.quit()

brain_dir = r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b"
shutil.copy('current_live_map.png', f"{brain_dir}\\current_live_map.png")
shutil.copy('current_live_map_hover_banka.png', f"{brain_dir}\\current_live_map_hover_banka.png")
print('Live map screenshots saved!')
