import json
import re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time




def create_driver():
    try:
        options = uc.ChromeOptions()
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
        return driver
    except Exception as e:
        print(f"创建驱动时发生错误：{e}")
        return None


def random_sleep(x,y):
    time.sleep(random.uniform(x, y))

def extract_main_content(html_content):
    """提取网页主要内容"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        info_dict = {
            'type': ''
        }
        data = []
         # 定位到 form 元素
        form_element = soup.find('form', id='msgForm')
        
        if form_element:
            # 找到所有 easysite-td-row 的 div
            td_rows = form_element.find_all('div', class_='easysite-td-row')
            for td_row in td_rows:
                type_span = td_row.find('span', class_='easysite-start-time')
                if type_span:
                    type_text = type_span.get_text(strip=True)
                    if type_text:  # 如果获取到的文本不为空
                        info_dict['type'] = type_text
                    data.append(info_dict.copy())
                    # else:
                    #     data.append(info_dict.copy())
                        # continue      
        return data
    except Exception as e:
        print(f"提取内容时发生错误: {str(e)}")
        return None
    
    
def open_website(links):

    driver = create_driver()
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.delete_all_cookies()  # 清除所有cookies

    print("第一次跳转：访问百度...")
    driver.get("http://www.baidu.com")
    random_sleep(1,3)
    print("第二次跳转：访问海关首页...")
    customs_url = "http://gdfs.customs.gov.cn/eportal/ui?currentPage=1&moduleId=3f22e92d83a04543bc0c7de623e7b034&pageId=373310"
    driver.get(customs_url)
    random_sleep(1,3)
    
    # 统计进度
    length = len(links)
    count = 0
    data = []
    try:
        # 遍历页面
        for url in links:
            print("访问目标页面...")
            driver.get(url)
            count += 1
            print("当前页数：{}/{}....\n".format(count,length))
            random_sleep(0.1,0.15)

            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if len(driver.page_source) > 1000:
                html_content = driver.page_source
                ret = extract_main_content(html_content)
                if ret:
                    data += ret
                    # data.append(ret)
                    # driver.close()
                                
        with open('QA_type.json','w',encoding='utf-8') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()


# 获取二级页面链接 
def get_second_url(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        links = []
        li_eliments = soup.find_all('li')
        
        for li in li_eliments:
            if li.find('a'):
                link = li.find('a').get('href')
                if not link.startswith('http'):
                    link = 'http://gdfs.customs.gov.cn' + link
                links.append(link)
        return links
    except Exception as e:
        print(f"提取二级页面链接时发生错误: {str(e)}")
        return None

def get_first_url():
        first_url = []
        for i in range(6,1462):
            # if i<4:
            #     prefix = "http://www.customs.gov.cn/customs/302249/302266/08654b53-"
            #     suffix = ".html"

            # else:
            prefix = "http://gdfs.customs.gov.cn/eportal/ui?currentPage="
            suffix = "&moduleId=3f22e92d83a04543bc0c7de623e7b034&pageId=373310"
            url = prefix + str(i) + suffix    
            # print(first_url)
            first_url.append(url)
        # # 将所有二级页面的链接保存
        # with open('links.txt' , 'a') as f:
        #     f.write('\n'.join(links))
        #     f.write('\n')
        return first_url



if __name__ == "__main__":
    
    first_urls = get_first_url()
    
    # with open('QA_links.txt', 'r') as f:
    #     links = f.read().splitlines()
        
    ret = open_website(first_urls)
    print(ret)
    
        
    