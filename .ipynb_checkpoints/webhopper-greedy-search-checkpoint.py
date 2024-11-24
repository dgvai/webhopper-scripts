# !pip install requests
# !pip install bs4
# !pip install emoji
# !pip install python-docx

import requests 
from bs4 import BeautifulSoup 
import json
import emoji
from collections import deque
from urllib.parse import urljoin
from docx import Document

class WebHopperSearch:
    def __init__(self, start_url, goal_keyword, max_depth=3):
        self.start_url = start_url
        self.goal_keyword = goal_keyword
        self.max_depth = max_depth
        self.visited = set()

    def heuristic(self, url):
        """Heuristic function: prioritize URLs with the goal keyword."""
        return -url.count(self.goal_keyword)

    def fetch_links(self, url):
        """Fetch all hyperlinks from a given URL."""
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = set(
                urljoin(url, a['href'])
                for a in soup.find_all('a', href=True)
                if urljoin(url, a['href']).startswith(self.start_url)
            )
            return links
        except Exception as e:
            print(f"Failed to fetch links from {url}: {e}")
            return set()

    def find_match(self, url):
        """find the goal from the page"""
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        titleSoup = soup.find(id='title')
        textSoup = soup.find(id='text')
        
        title = titleSoup.get_text().lower() if titleSoup else None
        text = textSoup.get_text().lower() if textSoup else None

        if not title or not text: 
            return False

        if(title.find(self.goal_keyword.lower()) >= 0 or text.find(self.goal_keyword.lower()) >= 0):
            return True
        return False

    def crawl(self):
        """A* algorithm for crawling and searching."""
        open_set = [(self.start_url, 0)]  # (URL, cost so far)
        g_scores = {self.start_url: 0}

        while open_set:
            # Sort open_set by total cost (g + h)
            open_set.sort(key=lambda x: g_scores[x[0]] + self.heuristic(x[0]))
            current_url, current_cost = open_set.pop(0)

            # Mark as visited
            if current_url in self.visited:
                continue
            self.visited.add(current_url)
            print(f"Visiting: {current_url}")

            # Check if goal is found
            if self.find_match(current_url):
                print(f"Goal found: {current_url}")
                return

            # Fetch and process neighbors
            if current_cost < self.max_depth:
                for neighbor in self.fetch_links(current_url):
                    tentative_g_score = current_cost + 1
                    if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                        g_scores[neighbor] = tentative_g_score
                        open_set.append((neighbor, tentative_g_score))

        print("Goal not found within max depth.")

if __name__ == "__main__":
    # set the root domain to crawl
    DOMAIN = "https://webhopper-client.vercel.app"
    
    goal_keyword = "human intervention"
    webhopper_search = WebHopperSearch(DOMAIN, goal_keyword)
    webhopper_search.crawl()