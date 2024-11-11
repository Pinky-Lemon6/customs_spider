import json
import re
import undetected_chromedriver as uc  # 改用 undetected_chromedriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time
from bs4 import BeautifulSoup  # 添加 BeautifulSoup 导入

def create_driver():
    # 使用 undetected_chromedriver
    options = uc.ChromeOptions()
    # 关键设置
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    options.add_argument('--ignore-ssl-errors')  # 忽略SSL错误
    
    # 随机窗口大小（避免统一的窗口特征）
    window_sizes = [(1200, 800), (1366, 768), (1440, 900), (1920, 1080)]
    window_size = random.choice(window_sizes)
    options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
    
    # 设置中文环境
    options.add_argument('--lang=zh-CN')
    
    # 添加自定义 headers
    options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    options.add_argument('--accept-language=zh-CN,zh;q=0.9')
    
    # 创建driver
    driver = uc.Chrome(options=options)
    return driver

def random_sleep():
    """随机等待1-3秒"""
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
            # news_content = news_content.split("公告下载链接")[0].strip()
            news_content = re.sub(r'下载链接.*?\n', '', news_content)
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
    max_retries = 1
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            driver = create_driver()
            
            # 设置页面加载超时
            driver.set_page_load_timeout(30)
            driver.set_script_timeout(30)
            
            # 随机延时
            random_sleep()
            
            # 第一次跳转：访问百度
            print("第一次跳转：访问百度...")
            driver.get("http://www.baidu.com")
            random_sleep()
            
            # 第二次跳转：访问海关首页
            print("第二次跳转：访问海关首页...")
            customs_url = "http://gdfs.customs.gov.cn/customs/302249/302266/index.html"
            driver.get(customs_url)
            random_sleep()
            
            for url in links:
                # 访问目标页面
                print("访问目标页面...")
                driver.get(url)
                random_sleep()
                
                # 等待页面加载
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                
                if len(driver.page_source) > 1000:
                    # 提取HTML内容并解析
                    html_content = driver.page_source
                    main_content = extract_main_content(html_content)
                    # driver.quit()
                    if main_content:
                        with open('regulations.json', 'a', encoding='utf-8') as f:
                            json.dump(main_content, f,ensure_ascii=False, indent=4)
                        
                else:
                    print(f"页面内容异常，重试第 {retry_count + 1} 次")
                    # driver.quit()
                    retry_count += 1
                    continue
                
        except Exception as e:
            print(f"发生错误: {str(e)}")
            if 'driver' in locals():
                driver.quit()
            retry_count += 1
            print(f"重试第 {retry_count} 次")
            time.sleep(5)
            
    print("达到最大重试次数，访问失败")
    return None

if __name__ == "__main__":
    # 目标网站URL
    # url = 'http://gdfs.customs.gov.cn/eportal/ui?currentPage=1&moduleId=3f22e92d83a04543bc0c7de623e7b034&pageId=373310'
    
    with open('relinks.txt', 'r') as f:
        links = f.read().splitlines()
    
    content = open_website(links)
    
    # if content:
    #     print("\n=== 页面标题 ===")
    #     print(content['title'])
    #     print("\n=== 主要内容 ===")
    #     print(content['content'])