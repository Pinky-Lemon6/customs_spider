import json
import re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# 指定ChromeDriver的路径
s = Service(r'C:\Users\Administrator.DESKTOP-CH7LIQO\Downloads\chromedriver-win64\chromedriver.exe')


def create_driver():
    # options = uc.ChromeOptions()
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    window_sizes = [(1200, 800), (1366, 768), (1440, 900), (1920, 1080)]
    window_size = random.choice(window_sizes)
    options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    options.add_argument('--lang=zh-CN')
    options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    options.add_argument('--accept-language=zh-CN,zh;q=0.9')
    driver = uc.Chrome(options=options)
    # driver = webdriver.Chrome(service=s,options=options)
    return driver


def random_sleep():
    time.sleep(random.uniform(1, 3))

def extract_main_content(html_content):
    """提取网页主要内容"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        info_dict = {}
        # 查找所有的span标签
        spans = soup.find_all('span')
        
        # 遍历每个span标签，提取其文本和紧随其后的文本
        for span in spans:
        # 使用正则表达式匹配<span>标签中的文本
            match = re.match(r'【(.*?)】', span.text)
            if match:
                label = match.group(1).replace("　　", "").strip() 
                class_content = span.next_sibling.strip() if span.next_sibling else "无内容"
                info_dict[label] = class_content
                
        content_tuples = list(info_dict.values())
        # 读取法规内容
        news_div = soup.find('div',class_="easysite-news-content")
        if news_div:
            news_content = news_div.get_text(strip=True)
            news_content = re.split(r'公告下载链接|规章文本下载链接|公告正文下载链接', news_content)[0].strip()
            # news_content = re.sub(r'下载链接.*?\n', '', news_content)
            news_content = news_content.split("pdf浏览次数")[0].strip()
            content_tuples.append(news_content)
            return content_tuples
        else:
            print("No content found in the page")
            # print(response)
        return None
    except Exception as e:
        print(f"提取内容时发生错误: {str(e)}")
        return None
    
    
def open_website(links):

    driver = create_driver()
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.delete_all_cookies()  # 清除所有cookies
    random_sleep()
    print("第一次跳转：访问百度...")
    driver.get("http://www.baidu.com")
    random_sleep()
    print("第二次跳转：访问海关首页...")
    customs_url = "http://gdfs.customs.gov.cn/customs/302249/302266/index.html"
    driver.get(customs_url)
    random_sleep()
    
    try:
        # 遍历二级页面
        for url in links:
            print("访问目标页面...")
            driver.get(url)
            random_sleep()
            # ret.append(driver.open_website())

            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if len(driver.page_source) > 1000:
                # ret.append(driver.open_website())
                html_content = driver.page_source
                ret = extract_main_content(html_content)
                # print(html_content)
                if ret:
                    with open('regulations3.json', 'a', encoding='utf-8') as f:
                        json.dump(ret, f,ensure_ascii=False, indent=4)
                    # driver.close()
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()
        

if __name__ == "__main__":
    # url = 'http://gdfs.customs.gov.cn/customs/302249/302266/302267/6176833/index.html'
    # html_content = open_website(url)
    # if html_content:
    #     print(html_content)
    
    with open('links.txt', 'r') as f:
        links = f.read().splitlines()
        
    ret = open_website(links)
    print(ret)
    
        
    