# WebHopper 
The project, WebHopper, was initiated with the objective of developing a web crawler capable of efficiently extracting paragraphs from web pages. To achieve this, a mock website was created using the JavaScript framework NextJS. This framework was chosen for its robust features and support for server-side rendering, which ensures that the web crawler can scrape content without relying on client-side rendering. The website, consisting of 18 pages each containing a unique article, was successfully deployed on Vercel, providing a stable and accessible platform for testing. The core functionality of WebHopper revolves around the implementation of two fundamental algorithms: Depth-First Search (DFS) and Breadth-First Search (BFS). These algorithms were meticulously integrated into the web crawler, which was developed using Python 3. Several Python libraries were utilized to facilitate the data scraping process, enhancing the efficiency and accuracy of the crawler.

## Installation
```bash
pip3 install -r requirements.txt
```

## Run Scripts
### Crawler Script
```bash
python3 webhopper-script.py
```
### Greedy Search Script
```bash
python3 webhopper-greedy-search.py "keyword to search"
```