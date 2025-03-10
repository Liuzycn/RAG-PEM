# RAG-PEM
Retrieval-Augmented Generation for Potential Event Mining

## Overview 📚
This project focuses on leveraging retrieval-augmented generation (RAG) and prompt engineering to analyze online statements and events, assessing their potential public opinion risks. By integrating historical public opinion data, a domain-specific knowledge base, and large language models (LLMs), the system extracts key viewpoints, measures sentiment intensity, and compares similar past events to aid public opinion analysis.

## Key Features & Implementation

### 1. Data Preprocessing

+ **Collecting the data from 蚁坊软件网站 (https://www.eefung.com/yanjiu/).**
+ **1189 pieces of data in total.**

## Codes

### 1_data_acquire.py
Using Web Crawler to crawl the data down and store them into a data1.jsonl file

### 2_text_cut.py
This code file is to delete the meaningless information in the raw data like 
舆情分析报告自动生成工具免费试用入口>>> 
相关阅读推荐：舆情简评｜*** 
(部分文字、图片来自网络，如涉及侵权，请及时与我们联系，我们会在第一时间删除或处理侵权内容。电话：***    负责人：***）
