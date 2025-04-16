import json
from tqdm import tqdm
from itertools import chain
from utils import read_jsonl
from sentence_transformers import SentenceTransformer

datas = read_jsonl("../autodl-tmp/data_big.jsonl")

outcome = list(chain.from_iterable(x["segments"] for x in datas))
#outcome = outcome[0:100001]

print(f"Finished generating texts list,{len(outcome)} in total")
model = SentenceTransformer('../all-mpnet-base-v2', local_files_only=True)
print(f"Finished loading model")
# 生成 embeddings
embeddings = model.encode(outcome, batch_size=128, show_progress_bar=True)

# 准备数据
output_file_path = "../autodl-tmp/data_big_3.jsonl"
with open(output_file_path, 'w', encoding='utf-8') as f:
    for i, (out, emb) in tqdm(enumerate(zip(outcome, embeddings)), total=len(outcome), desc="Processing"):
        json.dump({"id": i, "text": out, "embeddings": emb.tolist()}, f, ensure_ascii=False)
        f.write('\n')
