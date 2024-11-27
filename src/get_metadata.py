import concurrent
import json
from openai import OpenAI
import os

client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key  = "*************************")


def extract_json_from_response(response):
    # 去掉可能的代码块标记
    if response.startswith("json"):
        response = response[len("json"):].strip()
    if response.startswith("python"):
        response = response[len("python"):].strip()
    if response.startswith("```json"):
        response = response[len("```json"):].strip()
    if response.startswith("```python"):
        response = response[len("```python"):].strip()
    if response.endswith("```"):
        response = response[:-len("```")].strip()

    # Parse the JSON string
    try:
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析错误: {e}")


# 定义函数：对单条长文本生成整体总结
def process_long_text(text, max_length=512,llm_model="gpt-4", llm_max_tokens=512,task='QA'):
    """
    对长文本分段处理，并生成整体总结，最终限制在max_length字符内。
    """
    if task == 'QA':
        messages=[
                {"role": "system", "content":'''你是一名优秀的文本总结助手，下面的文本是一个涉及海关法规的问题的标题、内容和问题类型以及回答，请从文本中提取关键信息，并以字典形式返回，格式如下（注意：这些字段不一定需要全部提取，如果有就提取，没有则不提取）：
                  {
                    "主题关键词": ["xxx",...],
                    "相关法规": "xxx",(只需要给出带有书名号的法规名称，没有涉及可以不给出)
                    "涉及行业或产品": ["xxx",...],
                    "涉及范围或地区":["xxx",...],
                    "相关机构":["xxx",...],（没有涉及可以不给出）
                    "程序名称":["xxx",...]
                    }
                    （重要提示：请不要给出要求的字典以外的任何内容，否则会影响总结的准确性）
                    '''},
                {"role": "user", "content": text}
            ]
    elif task == 'regulations':
        messages=[
                {"role": "system", "content":'''你是一名优秀的文本总结助手，下面的文本是一个海关法规的标题以及对应的内容和附件的名称，请从文本中提取关键信息，并以字典形式返回，格式如下（这些字段不一定需要全部提取，如果有就提取，没有则不提取）：
                  {
                    "主题关键词": ["xxx",...],
                    "法律条款": ["xxx",...](只需要给出带有书名号的法规名称)
                    "涉及行业或产品": ["xxx",...],
                    "适用范围或地区":["xxx",...],
                    "相关表格或文件":["xxx",...],（涉及附件中的文件无需给出后缀，未涉及则不用给出）
                    "程序名称":["xxx",...]
                    }
                    （重要提示：请不要给出要求的字典以外的任何内容，否则会影响总结的准确性）
                    '''},
                {"role": "user", "content": text}
            ]
    
    try:
        
        response = client.chat.completions.create(
            model=llm_model,
            messages=messages,
            temperature=0.7
        )
        # print(response)
        message_content = response.choices[0].message.content.strip()
        # print(message_content)
        return message_content
    except Exception as e:
        return f"Error during final compression: {e}"
    
  
# 定义函数：对单条文本处理
def process_text(text, max_length=512, llm_model="gpt-4", llm_max_tokens=512,task='QA'):
    response_content = process_long_text(text, max_length=max_length, llm_model=llm_model, llm_max_tokens=llm_max_tokens)
    
    metadata = extract_json_from_response(response_content)
    return metadata

# 定义函数：处理单条文本的线程
def process_single_text(idx, text, max_length, llm_model, task='QA'):
    print(f"Processing {idx+1}...")
    return process_text(text, max_length=max_length, llm_model=llm_model, task=task)

# 修改批量处理文本函数以支持多线程
def process_texts_from_file(input_file, output_file, max_length=512, llm_model="gpt-4",task='QA'):
    # 读取 JSON 文件
    with open(input_file, "r", encoding="utf-8") as file:
        datas = json.load(file)

    if task=='QA':
        # 获取标题和内容
        texts = [f"quesion:{data['title']}:{data['content']},type:{data['type']},answer:{data['answer']}" for data in datas]
    elif task=='regulations':
        texts = [f"title:{data['title']},content:{data['content']},appendix:{data['appendix']}" for data in datas]

    processed_indices = set()
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            processed_data = json.load(file)
            processed_indices = {idx for idx, _ in enumerate(processed_data)}

    meatadatas = processed_data if processed_indices else [None] * len(texts)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_single_text, idx, text, max_length, llm_model,task): idx for idx, text in enumerate(texts) if idx not in processed_indices}

        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            try:
                metadata = future.result()
                meatadatas[idx] = metadata  # 保持原始数据的顺序
            except Exception as e:
                with open(output_file, "w", encoding="utf-8") as file:
                    json.dump(meatadatas, file, ensure_ascii=False, indent=4)
                print(f"Error processing {idx+1}: {e}")

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(meatadatas, file, ensure_ascii=False, indent=4)

    print(f"处理完成！结果已保存到 {output_file}")
                
    
# 主程序
if __name__ == "__main__":
    llm_model = "qwen-plus"
    # 处理QA数据
    input_file = r'./dataset/data/QA.json'  
    output_file = "metadata_QA.json"  
    task = 'QA'  # 工作模式（QA:问答，content：文本内容）
    # 处理regulations数据
    # input_file = r'./dataset/data/regulations.json'
    # output_file = "metadata_regulations.json"
    # task = 'regulations'
    # 批量处理文本
    process_texts_from_file(input_file, output_file,llm_model=llm_model,task=task)

    