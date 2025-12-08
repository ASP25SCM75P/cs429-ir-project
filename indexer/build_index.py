#!/usr/bin/env python3
"""
Indexer for CS-429 IR Project
Builds inverted index with TF-IDF from HTML files
"""

import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class SearchIndexer:
    def __init__(self, html_dir="../html", output_dir="."):
        self.html_dir = Path(html_dir)
        self.output_dir = Path(output_dir)
        self.documents = {}  # doc_id -> cleaned_text
        self.doc_metadata = {}  # doc_id -> {url, title, length}
        self.inverted_index = defaultdict(lambda: {"df": 0, "postings": []})
        self.vectorizer = None
        self.tfidf_matrix = None
        self.doc_ids = []
    
    def clean_text(self, text):
        """Basic text cleaning"""
        # Lowercase
        text = text.lower()
        # Remove special chars, keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_from_html(self, html_content):
        """Extract URL, title, and text from HTML"""
        # Get URL from comment
        url_match = re.search(r'<!-- URL: (.*?) -->', html_content)
        url = url_match.group(1) if url_match else "unknown"
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"
        
        # Get body text
        text = soup.get_text(separator=' ', strip=True)
        
        return url, title, text
    
    def build_inverted_index(self):
        """Build positional inverted index"""
        print("Building inverted index...")
        
        for doc_id, text in self.documents.items():
            tokens = text.split()
            
            # Build positional index
            term_positions = defaultdict(list)
            for pos, token in enumerate(tokens):
                term_positions[token].append(pos)
            
            # Add to inverted index
            for term, positions in term_positions.items():
                # Update document frequency
                if not any(p['doc_id'] == doc_id for p in self.inverted_index[term]['postings']):
                    self.inverted_index[term]['df'] += 1
                
                # Add posting
                self.inverted_index[term]['postings'].append({
                    'doc_id': doc_id,
                    'tf': len(positions),
                    'positions': positions[:10]  # Limit to first 10 for space
                })
        
        print(f"  Indexed {len(self.inverted_index)} unique terms")
    
    def build_tfidf(self):
        """Build TF-IDF vectors using scikit-learn"""
        print("Building TF-IDF vectors...")
        
        # Prepare corpus
        corpus = [self.documents[doc_id] for doc_id in self.doc_ids]
        
        # Build TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams
            min_df=1,
            max_df=0.95
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        
        print(f"  Vocabulary size: {len(self.vectorizer.vocabulary_)}")
        print(f"  Matrix shape: {self.tfidf_matrix.shape}")
    
    def load_documents(self):
        """Load all HTML documents"""
        print(f"Loading documents from {self.html_dir}/...")
        
        html_files = sorted(self.html_dir.glob("*.html"))
        if not html_files:
            raise ValueError(f"No HTML files found in {self.html_dir}/")
        
        for html_file in html_files:
            doc_id = html_file.stem
            
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            url, title, text = self.extract_from_html(html_content)
            cleaned_text = self.clean_text(text)
            
            self.documents[doc_id] = cleaned_text
            self.doc_ids.append(doc_id)
            self.doc_metadata[doc_id] = {
                'url': url,
                'title': title,
                'length': len(cleaned_text.split())
            }
        
        print(f"  Loaded {len(self.documents)} documents")
    
    def save_index(self):
        """Save all index components"""
        print("Saving index files...")
        
        # Save inverted index (sample for submission)
        index_sample = dict(list(self.inverted_index.items())[:100])
        with open(self.output_dir / "index.json", 'w') as f:
            json.dump(index_sample, f, indent=2)
        
        # Save full inverted index as pickle (for actual use)
        with open(self.output_dir / "inverted_index_full.pkl", 'wb') as f:
            pickle.dump(dict(self.inverted_index), f)
        
        # Save metadata
        with open(self.output_dir / "doc_metadata.json", 'w') as f:
            json.dump(self.doc_metadata, f, indent=2)
        
        # Save doc_ids
        with open(self.output_dir / "doc_ids.json", 'w') as f:
            json.dump(self.doc_ids, f, indent=2)
        
        # Save TF-IDF components
        with open(self.output_dir / "tfidf_vectorizer.pkl", 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        with open(self.output_dir / "tfidf_matrix.pkl", 'wb') as f:
            pickle.dump(self.tfidf_matrix, f)
        
        print(f"  Saved to {self.output_dir}/")
        print("  Files created:")
        print("    - index.json (sample)")
        print("    - inverted_index_full.pkl")
        print("    - doc_metadata.json")
        print("    - doc_ids.json")
        print("    - tfidf_vectorizer.pkl")
        print("    - tfidf_matrix.pkl")
    
    def get_stats(self):
        """Print index statistics"""
        print("\n" + "=" * 60)
        print("INDEX STATISTICS")
        print("=" * 60)
        print(f"Documents indexed: {len(self.documents)}")
        print(f"Unique terms: {len(self.inverted_index)}")
        print(f"Vocabulary size (TF-IDF): {len(self.vectorizer.vocabulary_) if self.vectorizer else 0}")
        print(f"Average doc length: {np.mean([m['length'] for m in self.doc_metadata.values()]):.0f} tokens")
        print("=" * 60)
    
    def build(self):
        """Main build process"""
        self.load_documents()
        self.build_inverted_index()
        self.build_tfidf()
        self.save_index()
        self.get_stats()

if __name__ == "__main__":
    indexer = SearchIndexer(html_dir="../html", output_dir=".")
    indexer.build()
