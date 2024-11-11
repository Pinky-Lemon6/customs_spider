from bs4 import BeautifulSoup

def extract_data_from_html(file_path):
    # 读取HTML文件
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html, 'html.parser')

    # 定位到留言板详情部分
    board_detail = soup.find('div', class_='easysite-board-detail easysite-border')

    # 留言板详情部分文本提取
    if board_detail:
        Q_head = board_detail.find('h3').text
        Q_content = board_detail.find('span', class_='easysite-detail-key').find_next('div').find('p').find_next('p').find_next('p').get_text(strip=True)
        Awnser = board_detail.find('span', class_='easysite-detail-key').find_next('div').find('p').find_next('p').find_next('p').find_next('p').find_next('p').find_next('p').find_next('p').get_text(strip=True)

        # 返回数据为元组
        return ((Q_head, Q_content), Awnser)
    else:
        # 如果未找到数据，返回None
        return None

# 调用函数并保存返回的数据
data = extract_data_from_html('test.html')

# 检查数据是否有效并打印
if data:
    print("Q_head:", data[0][0])
    print("Q_content:", data[0][1])
    print("Awnser:", data[1])
else:
    print("未找到数据。")

# 将数据以元组的形式保存在JSON文件中
import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f,ensure_ascii=False, indent=4)

