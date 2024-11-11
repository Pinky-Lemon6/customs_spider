import time
from bs4 import BeautifulSoup
import re
import json
import requests


def extract_data_from_html(url,session):
    
    response = fetch_content(url,session).text
    # if respone.status_code == 200:
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(response, 'lxml')
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
    else:
        print("No content found in the page")
        print(response)
            
    return content_tuples

# 一级页面获取二级页面链接
def get_second_url(url,session):
    respone = fetch_content(url,session)
    # print(respone)
    # if respone.status_code == 200:
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(respone, 'lxml')
    # print(soup)
    # 查找所有的链接
    links = []
    li_elements = soup.find_all('li')  # 查找所有的<li>标签
    # print(li_elements)
    for li in li_elements:
        if li.find('a',target = '_blank') and li.find('span'):
            link = li.find('a')['href']
            if not link.startswith('http'):
                link = 'http://www.customs.gov.cn' + link 
            links.append(link)
    print(links)
    return links
    
    
def waiting(x):
    print("waiting:", end=" ")
    for i in range(x):
        time.sleep(1)
        print("*", end="")
    print("\t")



# 使用request获取网页内容
def fetch_content(url,session):
    headers = {
    "Cookie": "__jsluid_h=4776bcee6f6c6b95d1d16589903b464c; AV7KYchI7HHaS=5vZ0F_COTV1DRufEEDYoJsBAHGHquBozsHO48ov9_7_W9gkqTE.0sJ8Z2y6UvS43RCDluwAIxyXfeHdQ8xyWoGA; EPORTALJSESSIONID=dugOcfEvJAXlrudmH24i8a_yGpURZdARIx1aM68YzZe1sHfAB1ka!1433066114; AV7KYchI7HHaT=UK0NRo254rHt7zdQlTZ4AYy.SSK0SO3PeMXY9AUQHQQVvqumJNDeC6rsLT3b8XoXU4nUMzAP6Ch1ldtnqzs3MnsNM0YfrMcNRpCiQQgSNItRONB8e7YQj0HkawsqDQzWBPNFUsXYUuLiQJ7.ySjiai5PnYEu_N47uQWZcndbwwsE34lnxyk8S_4vcF3eoS6J5ny2fyCW8bl_DUdwzxI822UtfLat45GtLsThdKQZISYP.._D12KXQLA3lOWm5ILQ8NNJlRoSYaGiUEappHugyeuuVX8hL7nqMAVjiP0VHSSAytQm72J_7KcT_9FD5PIlkbOpiRsYvmRq7SHsz4RT3hzBBMJ6NHcFtb0t22MIB3W; __jsl_clearance=1731115839.194|0|9iWC2f4GmWbl9r6jkI0L3ZCZCKc%3D",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
    }
    
        
    with session.get(url, headers = headers) as resp:
        resp.encoding = "utf-8"
        ret = resp
        # print(ret)
        # ret = resp.json()[0]
        resp.close()
        return ret 
    
# 爬取所有二级页面的链接并保存    
def get_links():
    for i in range(1,177):
        # waiting(1)
        if i<4:
            prefix = "http://www.customs.gov.cn/customs/302249/302266/08654b53-"
            suffix = ".html"

        else:
            prefix = "http://www.customs.gov.cn/eportal/ui?pageId=302266&currentPage="
            suffix = "&moduleId=08654b53d1cc42478813b0b2feddcb57&staticRequest=yes"
        first_url = prefix + str(i) + suffix    
        print(first_url)
        session = requests.Session()

        # 将所有二级页面的链接保存
        links = get_second_url(first_url,session)
        with open('links.txt' , 'a') as f:
            f.write('\n'.join(links))
            f.write('\n')
     

# 打开links.txt文件
with open('relinks.txt', 'r') as f:
    links = f.read().splitlines()
    # print(links)

    session = requests.Session()
    first_url = "http://www.customs.gov.cn/customs/302249/302266/08654b53-1.html"
    
    ret1 = fetch_content(first_url,session)
    # print(ret1)
    # if ret1.status_code == 200:
    new_session = requests.Session()
    new_session.cookies = ret1.cookies
    # 爬取二级页面的内容
    for url in links:
        waiting(1)
        print(url)
        
        data = extract_data_from_html(url,new_session)
        if data: 
            with open('regulations.json', 'a', encoding='utf-8') as f:
                json.dump(data, f,ensure_ascii=False, indent=4)
            # 从links中删除当前url
            links.remove(url)
        else:
            with open('relinks.txt' , 'w') as f:
                f.write('\n'.join(links))
                f.write('\n')
                print("Cookie is invalid!\n")
            break   
    # else :
        # print("Cookie is invalid!\n")
     

    
    

