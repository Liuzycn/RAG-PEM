import csv
import json
import time
import requests
from tqdm import trange
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Referer': 'https://www.eefung.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

section = "yanjiu"
def crawl_eefung_news(base_url, max_pages=5):  #TODO: crawl the data from 蚁坊软件网站 and restore it in the jsonl file
    
    results = []

    for page in trange(1, max_pages+1):
        try:
            if page == 1:
                list_url = f"{base_url}/{section}"
            else:
                list_url = f"{base_url}/{section}/{page}"

            response = requests.get(list_url, headers=HEADERS, timeout=10) #TODO: find each web page's information
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.find_all('div', class_='title'): #TODO: acquire the link of each sentiment
                link = item.find('a')['href']
                web_url = base_url + link

                article_response = requests.get(web_url, headers=HEADERS, timeout=10)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                
                title = article_soup.find('h1', class_='document-title').get_text() if article_soup.find('h1', class_='document-title') else '无标题'
                date = article_soup.find('span', class_='create-time').get_text() if article_soup.find('span', class_='create-time') else '无日期'
                content = article_soup.find('div', class_='document-content').get_text() if article_soup.find('div', class_='document-content') else '无内容'
                
                results.append({
                    'title': title,
                    'date': date,
                    'content': content,
                    'url': web_url
                })
                
                time.sleep(3) 

        except Exception as e:
            print(f"Crawl {page} page fail：{str(e)}")
            continue
    return results

if __name__ == "__main__":
    base_url = "https://www.eefung.com"
    results = crawl_eefung_news(base_url, max_pages=119) #TODO: choose how many pages you want to crawl
    with open('../autodl-tmp/data1.jsonl', 'w', encoding='utf-8') as f:
        for result in results:
            json.dump(result, f, ensure_ascii=False)
            f.write('\n')
            



