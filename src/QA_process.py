import json
import os

# 定义文件路径
file_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA_data.json')

# 读取JSON文件
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 数据处理示例（根据需要进行修改）
processed_data = []
for item in data:
    # 假设每个item是一个字典，提取特定字段
    processed_item = {
        'title': item.get('标题'),
        'content': item.get('留言内容'),
        'type': '',
        'answer': item.get('回复内容')
    }
    processed_data.append(processed_item)
    # 保存处理后的数据到JSON文件
    output_file_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA.json')
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(processed_data, output_file, ensure_ascii=False, indent=4)
# # 输出处理后的数据
# print(processed_data)