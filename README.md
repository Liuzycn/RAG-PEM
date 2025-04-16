# RAG-PEM
Retrieval-Augmented Generation for Potential Event Mining （基于检索增强生成的潜在舆情事件挖掘）

<p align='center'>
  <img height='40%'  src='assets/logo.png' />
</p>

## Overview 📚
本项目设计了一种基于检索增强生成（RAG）的大语言模型辅助舆情事件分析平台，旨在帮助用户分析尚未发酵的舆情，判断其是否具有较强的负面性及其原因。通过爬虫技术和整合现有舆情数据，获取了2023-2025年的舆情信息，确保知识库的时效性。采用基于句子相似度突变的文档分割方法，有效提高了信息独立性，避免了过长文档导致的信息重叠。平台最终实现了通过交互式网页，满足用户的舆情分析与问答需求。

## Key Features & Implementation ✨

### 1. Data Preprocessing

+ **Collecting the data from [蚁坊软件网站](https://www.eefung.com/yanjiu/).**
+ **1189 pieces of data in total.**

## Codes 🛠️

Before you run the code please register a deepseek or other model's api key and place it in the utils.py file.

### 1_data_acquire.py
Using Web Crawler to crawl the data down and store them into a data1.jsonl file

### 2_text_cut.py
This code file provides two options to process the codes.

### One is only to delete the meaningless information in the raw data like:
+ **舆情分析报告自动生成工具免费试用入口>>> **
+ **相关阅读推荐：舆情简评｜ **
+ **部分文字、图片来自网络，如涉及侵权，请及时与我们联系，我们会在第一时间删除或处理侵权内容。电话：负责人: **

You can choose task = delete to utilize this method.

### The other is to summarize the content in the data by using the LLM
You can choose task = delete to utilize this method.

### 2.5_chunk_paragraph.ipynb
Chunk the texts and encoding them using [all-mpnet-base-v2](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)

### 3_construct_base.ipynb
+ **Implement a retrieval-augmented generation (RAG) pipeline for public opinion event analysis by leveraging FAISS for efficient text similarity search and SentenceTransformer for embedding generation.**
+ **Build a vector database to store and retrieve relevant texts based on user queries, helping to analyze potential public opinion risks.**
+ **Retrieved texts are incorporated into a structured prompt, which is then sent to an LLM to generate an informed analysis of whether the queried event might escalate into a negative public opinion incident.**

## Package Usage ⚙️
### Requirements 📋
You can quickly install the corresponding dependencies,

```bash
pip install -r requirements.txt
```
## Example 

