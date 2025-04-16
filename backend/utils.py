import os
import json
import time
from openai import OpenAI
from volcenginesdkarkruntime import Ark

#client = OpenAI(api_key="sk-21839635f9f44970bddcd1f4fca8f674", base_url="https://api.deepseek.com")  

def read_jsonl(file_path):
    _data = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            _data.append(d)
    return _data

def fetch_with_retry(prompt, input_model="mistral", retries=10, delay=1):
    #client = None  # 预先初始化 client
    #input_model = None   # 预先初始化 model

    if input_model == "deepseek-r1-distill-qwen-32b":
        model = "deepseek-r1-distill-qwen-32b-250120"
        client = Ark(api_key="<your-api-key-here>")
    elif input_model == "deepseek-r1":
        model = "deepseek-r1-250120"
        client = Ark(api_key="<your-api-key-here>")
    elif input_model == "deepseek-v3":
        model = "deepseek-v3-250324"
        client = Ark(api_key="<your-api-key-here>")
    elif input_model == "doubao-1.5-pro":
        model = "doubao-1-5-pro-256k-250115"
        client = Ark(api_key="<your-api-key-here>")
    elif input_model == "doubao-pro":
        model = "doubao-pro-256k-241115"
        client = Ark(api_key="<your-api-key-here>")
    elif input_model == "mistral":
        model = "mistral-7b-instruct-v0.2"
        client = Ark(api_key="<your-api-key-here>")
    elif input_model == "moonshot":
        model = "moonshot-v1-128k"
        client = Ark(api_key="<your-api-key-here>")
    else:
        raise ValueError(f"Unsupported model: {input_model}")

    for _ in range(retries):
        try:
            response = client.chat.completions.create(
                model= model, 
                messages=[{"role": "system","content": "你是舆情分析专家"},
                {"role": "user", "content": prompt}],
            )
            return response
        except Exception as e:
            print(f"Error: {e}, retrying...")
        time.sleep(delay)
    return None