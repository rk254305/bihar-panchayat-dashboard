from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless=new')
options.add_argument('--window-size=1440,1200')
driver = webdriver.Chrome(options=options)

try:
    driver.get('http://localhost:3000')
    driver.execute_script("selectTheme('kosi-delta')")
    time.sleep(2)
    
    charts_el = driver.find_element("id", "chart-hero-comparison")
    driver.execute_script("arguments[0].scrollIntoView();", charts_el)
    time.sleep(1)
    
    driver.save_screenshot(r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b\charts_light_check.png")
finally:
    driver.quit()

from PIL import Image
im = Image.open(r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b\charts_light_check.png")
w, h = im.size
crop_im = im.crop((0, 300, w, min(h, 1100)))
crop_im.save(r"C:\Users\Raushan KUMAR\.gemini\antigravity\brain\cf2396fe-2bd0-44d9-950a-2fb0b36fdf3b\charts_light_cropped.png")
print("Saved charts_light_cropped.png")
