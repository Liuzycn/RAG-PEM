import faiss
import gdown
import numpy as np
from flask import Flask, request, jsonify
from utils import read_jsonl, fetch_with_retry
from sentence_transformers import SentenceTransformer

google_drive_file_id = "15rWF7sczyymhGM7u1pgCwtZEzB1mW4pS"
data_path = "data.jsonl"

gdown.download(f"https://drive.google.com/uc?id={google_drive_file_id}", data_path, quiet=False)

data = read_jsonl("data.jsonl")
dimension = len(data[0]["embeddings"])
vector_db = faiss.IndexFlatL2(dimension)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

embeddings = [item["embeddings"] for item in data]
texts = [item["text"] for item in data]
vector_db.add(np.array(embeddings, dtype=np.float32))

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"result": "请输入有效的查询内容"}), 400

    query_embedding = model.encode(user_query, convert_to_numpy=True)
    distances, indices = vector_db.search(np.array([query_embedding], dtype=np.float32), 5)
    
    retrieved_texts = "\n".join([texts[i] for i in indices[0] if i != -1])
    prompt = f"你是一名舆情分析专家。请根据以下用户输入的查询，结合相关的舆情信息进行回答，你的主要任务是分析一下该事件是否可能演变为负面舆情事件。\n\n用户查询输入：{user_query}\n\n相关舆情信息：{retrieved_texts}"
    
    response = fetch_with_retry(prompt)
    return jsonify({"result": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
