import json
from openai import OpenAI
import os


client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                api_key  = "********************")


# 定义函数：对单条长文本生成整体总结
def process_long_text(text, max_length=512, llm_model="gpt-4", llm_max_tokens=512):
    """
    对长文本分段处理，并生成整体总结，最终限制在max_length字符内。
    """
    try:
        # print("summary")
        response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content":'''你是一名优秀的文本总结助手，请在保留所有关键信息的前提下，将以下内容压缩到512字符以内，并以字符串形式返回，要求总结后的内容长度为500到512字符（返回内容中不用告诉我总结长度）：'''},
                {"role": "user", "content": text}
            ],
            max_tokens=llm_max_tokens,
            temperature=0.7
        )
        # print(response)
        message_content = response.choices[0].message.content.strip()[:max_length]
        return message_content
    except Exception as e:
        return f"Error during final compression: {e}"
    

# 定义函数：对单条文本处理
def process_text(text, max_length=512, llm_model="gpt-4", llm_max_tokens=512):
    """
    判断文本长度并处理：
    - 若长度小于max_length，直接返回原文。
    - 若长度超过max_length，分段处理并生成总结。
    """
    if len(text) <= max_length:
        return text
    else:
        response_content = process_long_text(text, max_length=max_length,  llm_model=llm_model, llm_max_tokens=llm_max_tokens)
        return response_content


# 定义函数：批量处理文本
def process_texts_from_file(input_file, output_file, max_length=512, llm_model="gpt-4"):
    """
    批量处理文本：
    - 从 input_file 读取数据。
    - 对每条数据进行处理（长度判断和总结）。
    - 将处理结果保存到 output_file 中。
    """
    # 读取 JSON 文件
    with open(input_file, "r", encoding="utf-8") as file:
        texts = json.load(file)

    # 检查数据格式
    if not isinstance(texts, list) or not all(isinstance(item, str) for item in texts):
        raise ValueError("输入文件格式错误，应为字符串列表！")
    # 检查输出文件是否存在，若存在则读取已处理的文本
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as file:
            summarized_texts = json.load(file)
    else:
        summarized_texts = []

    # 记录已处理的文本数量
    processed_count = len(summarized_texts)

    # 批量处理文本
    for idx, text in enumerate(texts[processed_count:], start=processed_count):
        print(f"Processing {idx+1}/{len(texts)}...")  # 进度提示
        summary = process_text(text, max_length=max_length, llm_model=llm_model)
        summarized_texts.append(summary)

    # 保存结果为新的 JSON 文件
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(summarized_texts, file, ensure_ascii=False, indent=4)
    

# 主程序
if __name__ == "__main__":
    # 压缩法规内容
    input_file = r'./dataset/data/content.json'  # 输入 JSON 文件
    output_file = "summmarized_content.json"  # 输出 JSON 文件
    # 压缩附件内容
    # input_file = r'./dataset/data/appendix_content.json'  # 输入 JSON 文件
    # output_file = "summarized_appendix.json"  # 输出 JSON 文件
    llm_model = "qwen-plus"
    # 批量处理文本
    process_texts_from_file(input_file, output_file,llm_model=llm_model)
