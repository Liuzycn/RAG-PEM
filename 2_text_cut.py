import json
import time
from openai import OpenAI
from tqdm import trange
from utils import read_jsonl, fetch_with_retry

task = "delete"
begin = 0 #TODO: decide where to start
prompts = [] #TODO: restore all the sentiment texts' prompts
#results = [] #TODO: restore the results
count = [begin, "unknown"]
#summary_content = [] #TODO: restore the cut texts
#reasoning_content = [] #TODO: restore the process of thinking

if task == "summary":
    prompt = '''
你是一个负责总结舆情信息的大语言模型。请根据以下提供的舆情信息，进行简明扼要的总结，并过滤掉与事件本身无关的内容。

标题：[title]
日期：[date]
内容：[content]

请确保总结后的信息包括事件的核心内容、关键信息以及情感倾向，同时去除无关的背景或细节信息。
'''
    output_file = "data2.jsonl"
    
elif task == "delete":
    prompt = '''
你是一个负责清理舆情信息的大语言模型。请在不改变原文信息长度的情况下，去除以下舆情内容中所有无关信息，如广告、免责声明、推广内容、联系方式、无关推荐文章等，仅保留与事件本身相关的内容。

标题：[title]  
日期：[date]  
内容：[content]  

请确保：
1. 事件核心内容、关键信息和情感倾向**完全保留**。  
2. **仅**删除无关的广告、推荐、免责声明等内容，不改变其余内容的结构和长度。  
3. **不得添加、改写或缩短事件的原始信息**。  
4. 仅输出清理后的文本，不需要额外解释。  
'''
    output_file = "data2_2.jsonl"
else:
    raise ValueError("输入值不符合要求")

datas = read_jsonl("../autodl-tmp/data1.jsonl")

for data in datas: #TODO: generate prompts
    prom = prompt.replace("[title]",data["title"]).replace("[date]",data["date"]).replace("[content]",data["content"]) 
    prompts.append(prom)

for i in trange(begin, len(prompts), desc="Process Prompts"):
    prompt = prompts[i]
    data = datas[i]
    count[1] = i
    response = fetch_with_retry(prompt)
    
    reasoning_content = response.choices[0].message.reasoning_content
    summary_content = response.choices[0].message.content
    data["summary_content"] = summary_content
    data["reasoning_content"] = reasoning_content

    with open(f'../autodl-tmp/{output_file}', 'a', encoding='utf-8') as f:  
        json.dump(data, f, ensure_ascii=False)
        f.write('\n')
    time.sleep(2)

print(f"Processed data from {count[0]} to {count[1]}")