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
from docx import Document
import win32com.client
import PyPDF2
import pandas as pd
import warnings



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
    
    
def read_docx(file_path):
    """读取 .docx 文件并返回文本内容"""
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return '\n'.join(text)
    except Exception as e:
        print(f"读取 .docx 文件时发生错误：{e}")
        return None
    

def read_doc(file_path):
    """读取 .doc 文件并返回文本内容"""
    try:
        # 创建 Word 应用程序对象
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False  # 不显示 Word 窗口
        doc = word.Documents.Open(file_path)
        text = doc.Content.Text  # 获取文档内容
        doc.Close(False)
        word.Quit()

        return text
    except Exception as e:
        print(f"读取 .doc 文件时发生错误：{e}")
        return None
    
    
def read_pdf(file_path):
    """读取 PDF 文件并返回文本内容"""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text())
            return '\n'.join(text)
    except Exception as e:
        print(f"读取 PDF 文件时发生错误：{e}")
        return None
 
 
def read_excel(file_path):
    """读取 Excel 文件并返回文本内容"""
    try:
        warnings.filterwarnings("ignore", category=UserWarning)  # 忽略 UserWarning
        if file_path.endswith('.xls'):
            df = pd.read_excel(file_path, engine='xlrd')  # 处理 .xls 文件
        else:
            df = pd.read_excel(file_path, engine='openpyxl')  # 处理 .xlsx 文件
        
        # 检查 DataFrame 是否为空
        if df.empty:
            print(f"警告: 文件 {file_path} 中没有数据。")
            return None
        
        return df.to_string(index=False)  # 返回 DataFrame 的字符串表示
    except Exception as e:
        print(f"读取 Excel 文件时发生错误：{e}")
        return None   
    
    

def extract_main_content(html_content,data):
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
            "content": "" ,              # 内容
            "appendix":""               # 附件
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
        
        # 读取法规内容并获取附件
        news_div = soup.find('div',class_="easysite-news-content")
        if news_div:
            news_content = news_div.get_text(strip=True)
            news_content = re.split(r'公告下载链接|规章文本下载链接|公告正文下载链接|浏览次数|附件：', news_content)[0].strip()
            info_dict["content"] = news_content
            # 提取附件内容
            appendix = get_appendix(html_content,data)
            info_dict["appendix"] = appendix
            return info_dict
        else:
            print("No content found in the page")
            # print(response)
        return None
    except Exception as e:
        print(f"提取内容时发生错误: {str(e)}")
        return None


def get_appendix(html_content, data):
    # try:
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取附件链接
    news_div = soup.find('div',class_="easysite-news-content")
    appendix_content = ""
    
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
                # file_name = a_tag.get_text(strip=True)
                # # 检查 file_name 是否包含有效的后缀
                # valid_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.tiff', '.rar']  
                # if not any(file_name.endswith(ext) for ext in valid_extensions):
                #         # 暂存 data 到 temp.json
                #         with open('temp.json', 'w', encoding='utf-8') as json_file:
                #             json.dump(data, json_file, ensure_ascii=False, indent=4)
                        
                #         new_file_name = input(f"文件名 '{file_name}' 不包含有效后缀，请输入正确的文件名: ")
                #         # 检查新输入的文件名
                #         if new_file_name.endswith('.tiff') or new_file_name.endswith('.rar'):
                #             print(f"文件 '{new_file_name}' 不进行下载。")
                #             continue  # 跳过下载
                        
                #         file_name = new_file_name
                file_name = os.path.basename(link)
                 
                download_file(link)
                # random_sleep(0.8,1.3)
                
                # 构建完整的文件路径
                downloaded_file_path = os.path.join('temp', file_name)
                
                # 读取 .docx 文件内容
                if file_name.endswith('.docx'):
                    text_content = read_docx(downloaded_file_path)                    
                # 读取 .doc 文件内容
                elif file_name.endswith('.doc'):
                    text_content = read_doc(downloaded_file_path)    
                # 读取 .pdf 文件内容
                elif file_name.endswith('.pdf'):
                    text_content = read_pdf(downloaded_file_path)
                # 读取 .xls 和 .xlsx 文件内容
                elif file_name.endswith('.xls') or file_name.endswith('.xlsx'):
                    text_content = read_excel(downloaded_file_path)
                else:
                    text_content = None
                    
                if text_content:
                    appendix_content += text_content + "\n"
                        
                # 删除下载的文件
                os.remove(downloaded_file_path)            
                # links.append(link)
            # else:
            #     print("No appendix found in the page")
            #     return None
            if re.search(r'公告下载链接|规章文本下载链接|公告正文下载链接', p.get_text()):
                break
            
        return appendix_content
    else:
        print("No content found in the page")
        return None
    # except Exception as e:
    #     print(f"提取内容时发生错误: {str(e)}")
    #     return None
    
    
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
                ret = extract_main_content(html_content,data)
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
    

def open_website(links):

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
    
    get_content(links,driver)
    
        
def download_file(url):
    """下载文件并保存到本地"""
    # 创建temp文件夹（如果不存在）
    folder_path = 'temp'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 构建完整的文件路径
    file_name = os.path.basename(url)  # 从 URL 中提取文件名
    file_path = os.path.join(folder_path, file_name)
    
    # # 检查是否存在同名文件，如果存在则重新命名
    # base_name, extension = os.path.splitext(file_name)
    # counter = 1
    # while os.path.exists(file_path):
    #     file_path = os.path.join(folder_path, f"{base_name}_{counter}{extension}")
    #     counter += 1
        
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
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    links_file_path = os.path.join(current_dir, 'link_test.txt')
    
    with open(links_file_path, 'r') as f:
        links = f.read().splitlines()
        
    ret = open_website(links)
    print(ret)

    
    