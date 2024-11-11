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


def random_sleep(x,y):
    time.sleep(random.uniform(x, y))

def extract_main_content(html_content):
    """提取网页主要内容"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        info_dict = {
            "question_head": "",  # 问题标题
            "question_content": "", # 问题内容
            "category": "",     # 问题类型
            "awnser": "",  # 回答
        }
        
        # 定位到留言板详情部分
        board_detail = soup.find('div', class_='easysite-board-detail easysite-border')
        
        # 文本提取
        if board_detail:
            info_dict["question_head"] = board_detail.find('span', class_='easysite-detail-key').find_next('div').find('p').get_text(strip=True)
            info_dict["question_content"] = board_detail.find('span', class_='easysite-detail-key').find_next('div').find('p').find_next('p').get_text(strip=True)
            info_dict["awnser"] = board_detail.find('span', class_='easysite-detail-key').find_next('div').find('p').find_next('p').find_next('p').get_text(strip=True)
            return info_dict
        
        return None
    except Exception as e:
        print(f"提取内容时发生错误: {str(e)}")
        return None
    
    
def open_website(links,style):

    driver = create_driver()
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.delete_all_cookies()  # 清除所有cookies
    random_sleep()
    print("第一次跳转：访问百度...")
    driver.get("http://www.baidu.com")
    random_sleep(1,3)
    print("第二次跳转：访问海关首页...")
    customs_url = "http://gdfs.customs.gov.cn/customs/302249/302266/index.html"
    driver.get(customs_url)
    random_sleep(1,3)
    
    data = []
    # 统计进度
    length = len(links)
    count = 0
    try:
        # 遍历二级页面
        for url in links:
            print("访问目标页面...")
            driver.get(url)
            count += 1
            print("当前页数：{}/{}....\n".format(count,length))
            random_sleep(0.5,1.5)

            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if len(driver.page_source) > 1000:
                html_content = driver.page_source
                if style == "first":
                    ret = get_second_url(html_content)
                    if ret:
                        with open('policy_links.txt', 'a') as f:
                            f.write('\n'.join(ret) + '\n')
                elif style == "second":
                    ret = extract_main_content(html_content)
                    if ret:
                        data.append(ret)
                    else:
                        break    
        if style == "first":
            return 1
        elif style == "second":
            with open('policys.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return 2
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()


# 获取二级页面链接 
def get_second_url(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        links = []
        ul_tag = soup.find('ul', class_='conList_ull')
        
        if ul_tag:
            for a_tag in ul_tag.find_all('a',href = True):
                link = a_tag.get('href')
                if not link.startswith('http'):
                    link = 'http://gdfs.customs.gov.cn' + link
                links.append(link)
        return links
    except Exception as e:
        print(f"提取二级页面链接时发生错误: {str(e)}")
        return None

def get_first_url():
        first_url = []
        for i in range(1,107):
            if i<4:
                prefix = "http://http://gdfs.customs.gov.cn/customs/302249/302270/302272/b600eb6d-"
                suffix = ".html"
            else:
                prefix = "http://gdfs.customs.gov.cn/eportal/ui?pageId=302272&currentPage="
                suffix = "&moduleId=b600eb6d22ff4eca8712ae56dd689014&staticRequest=yes"
        url = prefix + str(i) + suffix    
        # print(first_url)
        first_url.append(url)
        return first_url


if __name__ == "__main__":
    
    first_urls = get_first_url()
    ret = open_website(first_urls,"first")
    
    if ret == 1:
        with open('policy_links.txt', 'r') as f:
            links = f.read().splitlines()
        
    ret = open_website(links)
    print(ret)
    
        
    