#!/usr/bin/env python3
"""
Simple Wikipedia Crawler for CS-429 IR Project
Uses requests + BeautifulSoup (simpler than Scrapy)
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import uuid
import time
import json
from pathlib import Path
from collections import deque

class SimpleWikiCrawler:
    def __init__(self, seed_url, max_pages=50, output_dir="html"):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.visited = set()
        self.url_to_docid = {}
        self.docid_to_url = {}
        self.queue = deque([seed_url])
        
        # Be polite
        self.headers = {
            'User-Agent': 'CS429-IR-Project Educational Crawler (contact: student@iit.edu)'
        }
        self.delay = 1  # seconds between requests
    
    def is_valid_wiki_url(self, url):
        """Check if URL is a valid Wikipedia article"""
        parsed = urlparse(url)
        if 'wikipedia.org' not in parsed.netloc:
            return False
        if not parsed.path.startswith('/wiki/'):
            return False
        # Skip special pages
        if any(x in parsed.path for x in [':', 'Special:', 'Talk:', 'File:', 'Help:']):
            return False
        return True
    
    def crawl(self):
        """Main crawl loop"""
        print(f"Starting crawl from: {self.seed_url}")
        print(f"Target: {self.max_pages} pages")
        print(f"Output: {self.output_dir}/")
        print("-" * 60)
        
        page_count = 0
        
        while self.queue and page_count < self.max_pages:
            url = self.queue.popleft()
            
            if url in self.visited:
                continue
            
            try:
                # Fetch page
                print(f"[{page_count + 1}/{self.max_pages}] Fetching: {url[:60]}...")
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Generate doc ID
                doc_id = str(uuid.uuid4())
                
                # Save HTML
                html_file = self.output_dir / f"{doc_id}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    # Add URL as comment at top
                    f.write(f"<!-- URL: {url} -->\n")
                    f.write(response.text)
                
                # Track mapping
                self.url_to_docid[url] = doc_id
                self.docid_to_url[doc_id] = url
                self.visited.add(url)
                page_count += 1
                
                # Extract links for BFS
                if page_count < self.max_pages:
                    for link in soup.find_all('a', href=True):
                        next_url = urljoin(url, link['href'])
                        if self.is_valid_wiki_url(next_url) and next_url not in self.visited:
                            self.queue.append(next_url)
                
                # Be polite - rate limit
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"  ERROR: {e}")
                continue
        
        # Save URL mapping
        mapping_file = self.output_dir / "url_mapping.json"
        with open(mapping_file, 'w') as f:
            json.dump({
                'url_to_docid': self.url_to_docid,
                'docid_to_url': self.docid_to_url
            }, f, indent=2)
        
        print("-" * 60)
        print(f"✓ Crawl complete!")
        print(f"  Pages saved: {page_count}")
        print(f"  Files in: {self.output_dir}/")
        print(f"  Mapping: {mapping_file}")

if __name__ == "__main__":
    crawler = SimpleWikiCrawler(
        seed_url="https://en.wikipedia.org/wiki/Information_retrieval",
        max_pages=50,
        output_dir="../html"
    )
    crawler.crawl()
