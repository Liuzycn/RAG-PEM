import json
import time
from openai import OpenAI

client = OpenAI(api_key="<your api key>", base_url="https://api.deepseek.com")  

def read_jsonl(file_path):
    _data = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            _data.append(d)
    return _data

def fetch_with_retry(prompt, retries=10, delay=2):
    for _ in range(retries):
        try:
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": prompt}],
            )
            return response
        except Exception as e:
            print(f"Error: {e}, retrying...")
        time.sleep(delay)
    return None
    '''
def fetch_with_retry(prompt, retries=3, delay=2):
    response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": prompt}],
            )
    return response
    '''
