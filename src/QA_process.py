import json
import os
from datetime import datetime

# # 定义文件路径
# QA_file_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA.json')
# QA_type_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA_type.json')

# # 读取JSON文件
# with open(QA_file_path, 'r', encoding='utf-8') as file:
#     QA_data = json.load(file)
# with open(QA_type_path, 'r', encoding='utf-8') as file:
#     QA_type = json.load(file)

# # 数据处理示例（根据需要进行修改）
# processed_data = []
# for item, type in zip(QA_data, QA_type):
#     # 假设每个item是一个字典，提取特定字段
#     processed_item = {
#         'title': item.get('title'),
#         'content': item.get('content'),
#         'type': type.get('type'),
#         'answer': item.get('answer')
#     }
    
#     processed_data.append(processed_item)
# # 保存处理后的数据到JSON文件
# output_file_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA_1.json')
# with open(output_file_path, 'w', encoding='utf-8') as output_file:
#     json.dump(processed_data, output_file, ensure_ascii=False, indent=4)
# # 输出处理后的数据
# print(processed_data)
file_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA_1.json')
with open(file_path, 'r', encoding='utf-8') as file:
    qa_data = json.load(file)
    
# 创建元数据
metadata = {
    "metadata": {
        "title": "QA Data",
        "description": "This dataset contains questions and answers related to customs inquiries.",
        "created_at": "2024-11-23",
        "version": "1.0",
        "fields": [
            {"name": "title", "description": "The title of the inquiry.", "type": "string"},
            {"name": "content", "description": "The content of the inquiry.", "type": "string"},
            {"name": "type", "description": "The type/category of the inquiry.", "type": "string"},
            {"name": "answer", "description": "The response to the inquiry.", "type": "string"}
        ],
        "data_source": "Customs Department",
        "data_format": "JSON",
        "record_count": len(qa_data),
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }
}


# 保存元数据和数据到新的 JSON 文件
output_data = {
    "metadata": metadata,
    "data": qa_data
}

output_file_path = os.path.join(os.getcwd(), 'dataset', 'data', 'QA_with_metadata.json')
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(output_data, output_file, ensure_ascii=False, indent=4)
