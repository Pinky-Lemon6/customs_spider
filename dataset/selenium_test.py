from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 指定ChromeDriver的路径
s = Service(r'C:\Users\Administrator.DESKTOP-CH7LIQO\Downloads\chromedriver-win64\chromedriver.exe')


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    #options.add_argument("--no-sandbox") # linux only
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options,service=s)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver

def open_website(url):
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            driver = getDriver()
            driver.get(url)
            break
        except:
            retry_count += 1

# 初始化WebDriver对象
#driver = webdriver.Chrome(service=s)
driver = getDriver()
for i in range(1):
    # 打开网页
    driver.get('https://www.baidu.com')
    
    driver.get('http://www.customs.gov.cn')

    # 在这里添加你的代码
    # 获取所有Cookie
    cookies = driver.get_cookies()

    # 打印所有Cookie
    for cookie in cookies:
        print(cookie)
# 关闭浏览器
driver.quit()