import os
import faiss
import gdown
import zipfile
import numpy as np
from flask_cors import CORS
from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from huggingface_hub import hf_hub_download
import smtplib

from utils import read_jsonl, fetch_with_retry
from sentence_transformers import SentenceTransformer

# ------------------ 数据准备 ------------------
#extract_path = "./"
#data_path = "data_big_3.zip"
#jsonl_path = "data_big_4.jsonl"
#google_drive_file_id = "1_kUOTnl2hI27rikbRY5z4eu1TApGby05"

jsonl_path=hf_hub_download(repo_id="LZYFirecn/dataset", filename="data_big_6.jsonl", repo_type="dataset", cache_dir="./")

# ------------------ 构建向量库 ------------------
data = read_jsonl(jsonl_path)
dimension = len(data[0]["embeddings"])
vector_db = faiss.IndexFlatL2(dimension)
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

embeddings = [item["embeddings"] for item in data]
texts = [item["text"] for item in data]
vector_db.add(np.array(embeddings, dtype=np.float32))

# ------------------ Flask API ------------------
app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    user_query = request.json.get("query", "")
    LLM_model = request.json.get("model", "")
    if not user_query:
        return jsonify({"result": "请输入有效的查询内容"}), 400

    query_embedding = np.array(model.encode(user_query))
    distances, indices = vector_db.search(np.array([query_embedding], dtype=np.float32), 5)

    retrieved_texts = "\n".join([texts[i] for i in indices[0] if i != -1])
    prompt = f"""
你是一名资深舆情分析专家，请从专业角度出发，基于下列用户查询与召回的相关舆情信息，综合进行事件判断，评估该事件是否可能演变为负面舆情，并说明你的分析依据与逻辑过程。

请严格按照以下结构进行回答：

1. 舆情背景提取：  
请提炼当前舆情材料中的核心观点，明确事件的主要内容、关键参与方（如政府机构、企业、公众群体等），并指出当前公众关注的核心议题与焦点。

2. 情绪与争议因素分析：  
分析舆情材料中的情绪倾向（正面、中性或负面），识别可能激发公众情绪或引发争议的关键因素（如道德冲突、政策执行矛盾、历史积怨、社会敏感群体等），并说明其潜在敏感性。

3. 历史相似舆情参考与比较：  
参考过往与本事件相似的舆情案例（如事件类型、传播路径、结果等），对比其演化过程，并指出相似性与可能借鉴的经验或教训。

4. 风险演变路径推测：  
推测该事件未来可能的扩散或情绪演化路径（如：媒体报道、KOL扩散、二次创作、公众群体共鸣等），并指出风险节点。

5. 专业判断结论：  
结合上述分析，明确判断该事件是否具备负面舆情演变风险，并以专业语言简要说明判断依据与理由（不得使用“信息不足”或模糊判断语言）。

用户查询输入：
{user_query}

相关舆情信息：
{retrieved_texts}
"""
    response = fetch_with_retry(prompt, LLM_model)
    return jsonify({"result": response.choices[0].message.content})

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.json
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("EMAIL_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")

        name = data.get("name", "")
        email = data.get("email", "")
        subject = data.get("subject", "")
        message = data.get("message", "")
        
        if not all([name, email, subject, message]):
            return jsonify({"success": False, "message": "请填写完整的表单信息"}), 400

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = f"来自 {name} 的消息: {subject}"

        body = f"姓名: {name}\n邮箱: {email}\n\n{message}"
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({"success": True, "message": "邮件发送成功！"})

    except Exception as e:
        return jsonify({"success": False, "message": f"邮件发送失败: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # 使用环境变量 PORT
    app.run(host="0.0.0.0", port=port)