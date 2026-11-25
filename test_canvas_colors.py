from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)

try:
    driver.get('http://localhost:3000')
    info = driver.execute_script("""
        const colors = getThemeColors();
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = colors.mutedText;
        const fillMuted = ctx.fillStyle;
        
        ctx.fillStyle = colors.zp;
        const fillZp = ctx.fillStyle;

        ctx.fillStyle = colors.bp;
        const fillBp = ctx.fillStyle;
        
        ctx.fillStyle = colors.alertSoft;
        const fillAlertSoft = ctx.fillStyle;
        
        return {
            colors: colors,
            fillMuted: fillMuted,
            fillZp: fillZp,
            fillBp: fillBp,
            fillAlertSoft: fillAlertSoft
        };
    """)
    print("Computed colors from getThemeColors():")
    for k, v in info['colors'].items():
        print(f"  {k}: {v}")
    print("\nCanvas 2D parsed fillStyle:")
    print(f"  fillMuted: {info['fillMuted']}")
    print(f"  fillZp: {info['fillZp']}")
    print(f"  fillBp: {info['fillBp']}")
    print(f"  fillAlertSoft: {info['fillAlertSoft']}")
finally:
    driver.quit()
