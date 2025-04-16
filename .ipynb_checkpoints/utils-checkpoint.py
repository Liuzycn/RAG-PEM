import json
import time
import numpy as np
from tqdm import tqdm
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("../all-mpnet-base-v2", local_files_only=True)

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

def compute_sentence_similarity(sentences):
    """计算相邻句子的语义相似度"""
    embeddings = model.encode(sentences, convert_to_numpy=True)
    similarities = [cosine_similarity([embeddings[i]], [embeddings[i+1]])[0,0] for i in range(len(sentences) - 1)]
    return np.array(similarities)

def find_split_points(similarities):
    """寻找相似度突变最大的点"""
    if len(similarities) < 2:
        return []

    split_index = np.argmax(np.abs(np.diff(similarities))) + 1  # 选取突变最大的位置
    return [split_index]

def recursive_split(sentences):
    """递归拆分文本，确保每个段落小于600字"""
    if len("".join(sentences)) < 600:
        return ["".join(sentences)]  # 整体小于600字，直接返回

    similarities = compute_sentence_similarity(sentences)
    split_points = find_split_points(similarities)

    if not split_points:
        return ["".join(sentences)]  # 没有合理的分割点，返回整个文本

    split_idx = split_points[0]  # 选择相似度突变最大的点
    left_part = sentences[:split_idx]
    right_part = sentences[split_idx:]

    left_text = "".join(left_part)
    right_text = "".join(right_part)

    if len(left_text) >= 600:
        left_segments = recursive_split(left_part)  # 递归拆分左侧
    else:
        left_segments = [left_text]  # 不再拆分

    if len(right_text) >= 600:
        right_segments = recursive_split(right_part)  # 递归拆分右侧
    else:
        right_segments = [right_text]  # 不再拆分

    return left_segments + right_segments

def process_news(news_list, output_file="../autodl-tmp/data_big.jsonl", save_interval=1000):
    """处理新闻列表，边处理边存储，每1000条存一次"""
    results = []
    
    with open(output_file, "a", encoding="utf-8") as outfile:
        for i, text in enumerate(tqdm(news_list, desc="Processing News", unit="item")):
            text = text.strip()

            if len(text) < 600:
                results.append({"original_text": text, "segments": [text]})
            else:
                # 分割句子
                sentences = text.split("。")
                sentences = [s.strip() + "。" for s in sentences if s.strip()]  # 保留句号

                segments = recursive_split(sentences)  # 递归分割文本
                results.append({"original_text": text, "segments": segments})

            # 每 `save_interval` 条存一次
            if (i + 1) % save_interval == 0:
                for item in results:
                    json.dump(item, outfile, ensure_ascii=False)
                    outfile.write("\n")
                outfile.flush()  # 立即写入磁盘
                results.clear()  # 清空缓存

        # 处理剩余数据
        if results:
            for item in results:
                json.dump(item, outfile, ensure_ascii=False)
                outfile.write("\n")
            outfile.flush()

    print(f"处理完成，已保存至 {output_file}")
    '''
def fetch_with_retry(prompt, retries=3, delay=2):
    response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[{"role": "user", "content": prompt}],
            )
    return response
    '''