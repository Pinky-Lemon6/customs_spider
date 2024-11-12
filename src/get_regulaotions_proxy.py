import json
import re
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# 指定ChromeDriver的路径
s = Service(r'C:\Users\Administrator.DESKTOP-CH7LIQO\Downloads\chromedriver-win64\chromedriver.exe')
driver_path = r'C:\Users\Administrator.DESKTOP-CH7LIQO\Downloads\chromedriver-win64\chromedriver.exe'

# 提取代理API接口，获取1个代理IP
api_url = "https://dps.kdlapi.com/api/getdps/?secret_id=oy03n7c0uqh4ti6uyqk1&signature=b99hnq3pojrm2oqifnjbu4ncox75eml2&num=1&pt=1&format=text&sep=2"


def create_driver(proxy = None):
    try:
        options = uc.ChromeOptions()
        # options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # 设置代理服务器
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
            
        window_sizes = [(1200, 800), (1366, 768), (1440, 900), (1920, 1080)]
        window_size = random.choice(window_sizes)
        options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        options.add_argument('--lang=zh-CN')
        options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
        options.add_argument('--accept-language=zh-CN,zh;q=0.9')
        driver = uc.Chrome(options=options,executable_path=driver_path)
        
        # driver = webdriver.Chrome(service=s,options=options)
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
            "document_type": "",  # 法规类型
            "category": "",       # 内容类别
            "announcement_number": "",  # 文号
            "issuing_authority": "",     # 发文机关
            "issue_date": "",           # 发布日期
            "effective_date": "",       # 生效日期
            "status": "",               # 效力
            "remarks": "",              # 效力说明
            "title":"",                 # 标题
            "content": ""               # 内容
        }
        # 查找所有的 hgfg_list
        hgfg_lists = soup.find_all('div', class_='hgfg_list')

        for item in hgfg_lists:
            span = item.find('span')
            if span:
                label = span.get_text(strip=True)  # 获取标签文本
                class_content = item.get_text(strip=True).replace(label, '').strip()  # 获取内容并去掉标签文本

                # 根据标签填充 info_dict
                if label == "【法规类型】":
                    info_dict["document_type"] = class_content
                elif label == "【内容类别】":
                    info_dict["category"] = class_content
                elif label == "【文　　号】":
                    info_dict["announcement_number"] = class_content
                elif label == "【发文机关】":
                    info_dict["issuing_authority"] = class_content
                elif label == "【发布日期】":
                    info_dict["issue_date"] = class_content
                elif label == "【生效日期】":
                    info_dict["effective_date"] = class_content
                elif label == "【效力】":
                    info_dict["status"] = class_content
                elif label == "【效力说明】":
                    info_dict["remarks"] = class_content
                
        # 读取法规标题
        title_div = soup.find('div',class_="easysite-news-title")
        if title_div:
            h2_tag = title_div.find('h2')
            title = h2_tag.get_text(strip=True)
            info_dict["title"] = title
        else:
            print("No title found in the page")
        
        # 读取法规内容
        news_div = soup.find('div',class_="easysite-news-content")
        if news_div:
            news_content = news_div.get_text(strip=True)
            news_content = re.split(r'公告下载链接|规章文本下载链接|公告正文下载链接', news_content)[0].strip()
            news_content = re.split(r'pdf浏览次数|浏览次数|附件', news_content)[0].strip()
            info_dict["content"] = news_content
            return info_dict
        else:
            print("No content found in the page")
            # print(response)
            return None
    except Exception as e:
        print(f"提取内容时发生错误: {str(e)}")
        return None
    
    
def open_website(links,proxy):

    # driver = create_driver(proxy=f'http://{ip_list[0]}')
    ip = requests.get(api_url).text
    print(ip)
    proxy_ip = f'http://{ip}/'
    proxys_ip = f'https://{ip}/'
    print(proxy_ip)

    driver = create_driver(proxy=proxy_ip)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.delete_all_cookies()  # 清除所有cookies
    # random_sleep()
    print("第一次跳转：访问百度...")
    driver.get("http://www.baidu.com")
    random_sleep(1,2)
    print("第二次跳转：访问海关首页...")
    customs_url = "http://gdfs.customs.gov.cn/customs/302249/index.html"
    driver.get(customs_url)
    random_sleep(1,2)
    
    all_data = []
    # 统计进度
    length = len(links)
    count = 0
    try:
        # 遍历二级页面
        for url in links:
            # proxy = f'http://{ip_list[count % len(ip_list)]}'
            # driver = create_driver(proxy=proxy)
            count += 1
            if count % 8 == 0:
                driver.quit()
                proxy_ip = requests.get(api_url).text
                driver = create_driver(proxy=f'http://{proxy_ip}/')
              
            print("访问目标页面...")
            driver.get(url)
            
            print("当前页数：{}/{}....\n".format(count,length))
            random_sleep(1,1.5)

            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if len(driver.page_source) > 1000:
                html_content = driver.page_source
                ret = extract_main_content(html_content)
                # print(ret)
                if ret:
                    all_data.append(ret)
                    driver.close()
                else:
                    break   
        with open('regulations.json', 'w', encoding='utf-8') as f:
            json.dump(all_data, f,ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()
        

if __name__ == "__main__":
    
    # tiquApiUrl = 'http://proxy.siyetian.com/apis_get.html?token=AesJWLNpWQ39EVJdXTqFFeNRVR31kend3TR1STqFUeORUR41EVBpXTq1UNOR0az0EVndnT6VlM.AOyMDNzITMzcTM&limit=100&type=0&time=&split=1&split_text='
    # apiRes = requests.get(tiquApiUrl,timeout=5)
    # ip = apiRes.text
    # ip_list = ip.replace('<br />', '\n').splitlines()
    # # 去除每个 IP 地址的前后空白
    # ip_list = [ip.strip() for ip in ip_list if ip.strip()]  # 过滤掉空字符串
    # print(ip_list)
    #代理服务器
    # ipport = f'http://{ip}'
    # #如果有账号密码 
    # ipport = f'http://账号:密码@{ip}'
    
    # proxies={
    #     'http':ipport,
    #     'https':ipport
    # }
    
    # proxy = f'http://{ip}'
    
    with open('link_test.txt', 'r') as f:
        links = f.read().splitlines()
        
    proxy = None   
    ret = open_website(links,proxy)
    print(ret)
    
    
    # # 从海关总署.html文件中获取html文本：
    # # 定义文件路径
    # file_path = '海关总署.html'
    # all_data = []
    # # 读取 HTML 文件内容
    # for i in range(3):
    #     try:
    #         with open(file_path, 'r', encoding='utf-8') as file:
    #             html_content = file.read()  # 读取文件内容
    #             print("成功读取 HTML 内容")
    #             info  =extract_main_content(html_content)
    #             all_data.append(info)
    #             print(info)
    #     except FileNotFoundError:
    #         print(f"文件 {file_path} 未找到")
    #     except Exception as e:
    #         print(f"读取文件时发生错误: {e}")
    #     with open('regu.json', 'w', encoding='utf-8') as f:
    #         json.dump(all_data, f,ensure_ascii=False, indent=4)
    
        
    