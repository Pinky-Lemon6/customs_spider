import json
import os
import re
from bs4 import BeautifulSoup
import requests
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
            news_content = re.split(r'公告下载链接|规章文本下载链接|公告正文下载链接|浏览次数', news_content)[0].strip()
            info_dict["content"] = news_content
            return info_dict
        else:
            print("No content found in the page")
            # print(response)
        return None
    except Exception as e:
        print(f"提取内容时发生错误: {str(e)}")
        return None


def extract_links_and_download(html_content):
    # try:
    soup = BeautifulSoup(html_content, 'html.parser')
    # 判断当前法规是否有效
    hgzs_lis4_div = soup.find('div', class_='hgzs_lis4')
    if hgzs_lis4_div:
        hgfg_list_div = hgzs_lis4_div.find('div', class_='hgfg_list')
        if hgfg_list_div:
            span = hgfg_list_div.find('span')
            if span:
                status = hgfg_list_div.get_text(strip=True).replace(span.get_text(strip=True), '').strip()
                if status != '有效':
                    print("该法规已失效")
                    return 2
    
    # 提取附件链接
    news_div = soup.find('div',class_="easysite-news-content")
    if news_div:
        p_tags = news_div.find_all('p')
        # links = []
        for p in p_tags:
            a_tag = p.find('a',href = True)
            # print(a_tag)
            if a_tag:
                link = a_tag['href']
                if not link.startswith('http'):
                    link = 'http://gdfs.customs.gov.cn' + link
                    # print(link)
                    file_name = a_tag.get_text(strip=True)
                    # 检查 file_name 是否包含有效的后缀
                    if not file_name.endswith('.doc') and not file_name.endswith('.docx'):
                        file_name += '.doc'  # 默认添加 .doc 后缀  
                    download_file(link, file_name)
                    random_sleep(0.8,1.3)
                # links.append(link)
            # else:
            #     print("No appendix found in the page")
            #     return None
            if re.search(r'公告下载链接|规章文本下载链接|公告正文下载链接', p.get_text()):
                break
        return 1
    else:
        print("No content found in the page")
        # print(response)
        return None
    # except Exception as e:
    #     print(f"提取内容时发生错误: {str(e)}")
    #     return None
    

def open_website(links,mode):

    driver = create_driver()
    print(driver)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    driver.delete_all_cookies()  # 清除所有cookies
    # random_sleep()
    print("第一次跳转：访问百度...")
    driver.get("http://www.baidu.com")
    random_sleep(1,3)
    print("第二次跳转：访问海关首页...")
    customs_url = "http://gdfs.customs.gov.cn/customs/302249/index.html"
    driver.get(customs_url)
    random_sleep(1,3)
    
    if mode == "content":
        get_content(links,driver)
    elif mode == "appendix":
        get_appendix(links,driver)
    
        
def get_content(links,driver):
    data = []
    
    # 统计进度
    length = len(links)
    count = 0
    try:
        # 遍历二级页面
        for url in links:
            # print("访问目标页面...")
            driver.get(url)
            count += 1
            print("访问目标页面，当前页数：{}/{}....\n".format(count,length))
            random_sleep(0.1,0.3)

            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if len(driver.page_source) > 1000:
                html_content = driver.page_source
                ret = extract_main_content(html_content)
                # print(ret)
                if ret:
                    data.append(ret)
                    # driver.close()
                else:
                    break   
        with open('regulations.json', 'w', encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()
        

def get_appendix(links,driver):
    # 统计进度
    length = len(links)
    # link = ["http://gdfs.customs.gov.cn/customs/302249/302266/302267/6162604/index.html"]
    count = 0
    try:
        # 遍历二级页面
        for url in links:
            # print("访问目标页面...")
            driver.get(url)
            count += 1
            print("访问目标页面，当前页数：{}/{}....\n".format(count,length))
            random_sleep(0.1,0.3)

            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            if len(driver.page_source) > 1000:
                html_content = driver.page_source
                ret = extract_links_and_download(html_content)
                # print(ret)
                if ret == 1:
                    print("Get appendix")
                    # data.append(ret)
                    # driver.close()
                else:
                    break   
        
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

        

def download_file(url, file_name):
    """下载文件并保存到本地"""
    # 创建 appendix 文件夹（如果不存在）
    folder_path = 'appendix'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 构建完整的文件路径
    file_path = os.path.join(folder_path, file_name)
    
    # 检查是否存在同名文件，如果存在则重新命名
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(folder_path, f"{base_name}_{counter}{extension}")
        counter += 1
        
    headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }
    try:
        
        response = requests.get(url, stream=True,headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 确保文件名合法
        file_name = file_name.replace('/', '_').replace('\\', '_')  # 替换非法字符
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"文件已下载: {file_name}")
    except Exception as e:
        print(f"下载文件时发生错误: {e}")
        
        


if __name__ == "__main__":
    
    with open('relinks.txt', 'r') as f:
        links = f.read().splitlines()
        
    ret = open_website(links,mode="appendix")
    print(ret)

    
    