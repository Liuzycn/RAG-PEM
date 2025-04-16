import json
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import read_jsonl,process_news

datas = read_jsonl("../autodl-tmp/zh/part-663de978334d-000019.jsonl")
#datas_before = read_jsonl("../autodl-tmp/data2_2.jsonl")

data_content = [data["content"] for data in datas[:100000]]
#data_content = data_content + [data["content"] for data in datas_before]
print(f"共计{len(data_content)}条新闻")

model = SentenceTransformer("../all-mpnet-base-v2", local_files_only=True)

processed_news = process_news(data_content)
