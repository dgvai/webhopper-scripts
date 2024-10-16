# !pip install requests
# !pip install bs4
# !pip install emoji

import requests 
from bs4 import BeautifulSoup 
import json
import emoji
from collections import deque

# set the root domain to crawl
DOMAIN = "https://webhopper-client.vercel.app"

def paragraph_extractor(soup, paragraphs):
    titleSoup = soup.find(id='title')
    textSoup = soup.find(id='text')
    
    title = titleSoup.get_text() if titleSoup else None
    text = textSoup.get_text() if textSoup else None

    if title in paragraphs:
        paragraphs[title].append(text)
    else:
        paragraphs[title] = [text]

def DFS_crawler(url, visited, paragraphs):
    if url in visited:
        return
    visited.add(url)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    paragraph_extractor(soup, paragraphs)
    print(emoji.emojize("✅ crawling completed: "), url)
    
    links = soup.find_all('a', href=True)
    for link in links:
        next_url = f"{DOMAIN}{link.get('href')}"
        DFS_crawler(next_url, visited, paragraphs)

def BFS_crawler(url, visited, paragraphs):
    queue = deque([url])
    
    while queue:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        paragraph_extractor(soup, paragraphs)
        print(emoji.emojize("✅ crawling completed: "), url)

        links = soup.find_all('a', href=True)
        for link in links:
            next_url = f"{DOMAIN}{link.get('href')}"
            if next_url not in visited:
                queue.append(next_url)

def webhopper(start_url):
    visited = set()
    paragraphs = {}
    BFS_crawler(start_url, visited, paragraphs)
    return paragraphs

if __name__ == "__main__":
    paragraphs = webhopper(DOMAIN)
    print(json.dumps(paragraphs, indent=4))