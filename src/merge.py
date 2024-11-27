import json
import os


def merge_QA(qa_file_path,metadata_file_path,output_file_path):
    # 读取QA.json文件
    with open(qa_file_path, 'r', encoding='utf-8') as qa_file:
        qa_data = json.load(qa_file)

    # 读取metadata_QA.json文件
    with open(metadata_file_path, 'r', encoding='utf-8') as metadata_file:
        metadata_data = json.load(metadata_file)

    # 确保两个文件的长度相同
    if len(qa_data) != len(metadata_data):
        raise ValueError("两个json文件的元素数量不匹配")

    # 为每个QA元素添加metadata字段
    for qa_item, metadata_item in zip(qa_data, metadata_data):
        qa_item['metadata'] = metadata_item

    # 将结果写入新的QA_v1.json文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(qa_data, output_file, ensure_ascii=False, indent=4)
    print("新文件已生成。")
    
def merge_regulations(regulations_path, sm_content_path, sm_appendix_path, metadata_path, output_path):
    # 读取regulations.json文件
    with open(regulations_path, 'r', encoding='utf-8') as regulations_file:
        regulations_data = json.load(regulations_file)

    # 读取summarized_content.json文件
    with open(sm_content_path, 'r', encoding='utf-8') as sm_content_file:
        sm_content_data = json.load(sm_content_file)

    # 读取summarized_appendix.json文件
    with open(sm_appendix_path, 'r', encoding='utf-8') as sm_appendix_file:
        sm_appendix_data = json.load(sm_appendix_file)

    # 读取metadata_content.json文件
    with open(metadata_path, 'r', encoding='utf-8') as metadata_file:
        metadata_data = json.load(metadata_file)

    # 确保四个文件的长度相同
    if len(regulations_data) != len(sm_content_data) or len(regulations_data) != len(sm_appendix_data) or len(regulations_data) != len(metadata_data):
        raise ValueError("四个json文件的元素数量不匹配")

    # 更新regulations_data中的字段
    for regulation_item, content_item, appendix_item, metadata_item in zip(regulations_data, sm_content_data, sm_appendix_data, metadata_data):
        regulation_item['content'] = content_item
        regulation_item['appendix_content'] = appendix_item
        regulation_item['metadata'] = metadata_item

    # 将结果写入新的输出文件
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(regulations_data, output_file, ensure_ascii=False, indent=4)
    print("新文件已生成。")
    
    
if __name__ == "__main__":
    # 获取当前工作目录
    current_directory = os.getcwd()
    data_folder = os.path.join(current_directory, r'dataset\data')
    # 合并QA
    # qa_file_path = os.path.join(data_folder, 'QA.json')
    # metadata_file_path = os.path.join(data_folder, 'metadata_QA.json')
    # output_file_path = os.path.join(data_folder, 'QA_with_metadata.json')
    # merge_QA(qa_file_path,metadata_file_path,output_file_path)
    
    # 合并regulations
    regulations_path = os.path.join(data_folder, 'regulations_v1.json')
    sm_content_path = os.path.join(data_folder, 'summarized_content.json')
    sm_appendix_path = os.path.join(data_folder, 'summarized_appendix.json')
    metadata_path = os.path.join(data_folder, 'metadata_regulations.json')
    output_path = os.path.join(data_folder, 'regulations_with_metadata.json')
    merge_regulations(regulations_path, sm_content_path, sm_appendix_path, metadata_path, output_path)