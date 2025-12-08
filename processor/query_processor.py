#!/usr/bin/env python3
"""
Query Processor for CS-429 IR Project
Flask API for processing queries and returning ranked results
"""

from flask import Flask, request, jsonify
import json
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import csv
from pathlib import Path

app = Flask(__name__)

# Global variables for loaded data
doc_ids = []
doc_metadata = {}
vectorizer = None
tfidf_matrix = None

def load_index(indexer_dir="../indexer"):
    """Load all index components"""
    global doc_ids, doc_metadata, vectorizer, tfidf_matrix
    
    indexer_path = Path(indexer_dir)
    
    print("Loading index components...")
    
    # Load doc IDs
    with open(indexer_path / "doc_ids.json", 'r') as f:
        doc_ids = json.load(f)
    
    # Load metadata
    with open(indexer_path / "doc_metadata.json", 'r') as f:
        doc_metadata = json.load(f)
    
    # Load TF-IDF components
    with open(indexer_path / "tfidf_vectorizer.pkl", 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open(indexer_path / "tfidf_matrix.pkl", 'rb') as f:
        tfidf_matrix = pickle.load(f)
    
    print(f"✓ Loaded index with {len(doc_ids)} documents")

def rank_documents(query_text, top_k=10):
    """Rank documents for a query using cosine similarity"""
    # Vectorize query
    query_vec = vectorizer.transform([query_text.lower()])
    
    # Calculate cosine similarity
    similarities = cosine_similarity(query_vec, tfidf_matrix)[0]
    
    # Get top-K indices
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # Build results
    results = []
    for rank, idx in enumerate(top_indices, 1):
        score = similarities[idx]
        if score > 0:  # Only include documents with non-zero similarity
            doc_id = doc_ids[idx]
            results.append({
                'rank': rank,
                'doc_id': doc_id,
                'score': float(score),
                'url': doc_metadata[doc_id]['url'],
                'title': doc_metadata[doc_id]['title']
            })
    
    return results

@app.route('/search', methods=['GET'])
def search():
    """Search endpoint"""
    query = request.args.get('q', '')
    top_k = int(request.args.get('k', 10))
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    results = rank_documents(query, top_k)
    
    return jsonify({
        'query': query,
        'num_results': len(results),
        'results': results
    })

@app.route('/batch', methods=['POST'])
def batch_process():
    """Process batch queries from CSV"""
    queries_file = Path("../queries/queries.csv")
    results_file = Path("../queries/results.csv")
    
    if not queries_file.exists():
        return jsonify({'error': 'queries.csv not found'}), 404
    
    # Read queries
    with open(queries_file, 'r') as f:
        reader = csv.DictReader(f)
        queries = list(reader)
    
    # Process each query
    all_results = []
    for query_row in queries:
        query_id = query_row['query_id']
        query_text = query_row['query_text']
        
        results = rank_documents(query_text, top_k=10)
        
        for result in results:
            all_results.append({
                'query_id': query_id,
                'doc_id': result['doc_id'],
                'rank': result['rank'],
                'score': result['score']
            })
    
    # Write results
    with open(results_file, 'w', newline='') as f:
        if all_results:
            writer = csv.DictWriter(f, fieldnames=['query_id', 'doc_id', 'rank', 'score'])
            writer.writeheader()
            writer.writerows(all_results)
    
    return jsonify({
        'status': 'success',
        'queries_processed': len(queries),
        'results_file': str(results_file)
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'documents': len(doc_ids),
        'vocabulary': len(vectorizer.vocabulary_) if vectorizer else 0
    })

def process_queries_standalone():
    """Process queries without Flask (for notebook use)"""
    queries_file = Path("../queries/queries.csv")
    results_file = Path("../queries/results.csv")
    
    if not queries_file.exists():
        print(f"Error: {queries_file} not found")
        return
    
    # Read queries
    with open(queries_file, 'r') as f:
        reader = csv.DictReader(f)
        queries = list(reader)
    
    print(f"Processing {len(queries)} queries...")
    
    # Process each query
    all_results = []
    for query_row in queries:
        query_id = query_row['query_id']
        query_text = query_row['query_text']
        
        print(f"  Query: {query_text}")
        results = rank_documents(query_text, top_k=10)
        print(f"    Found {len(results)} results")
        
        for result in results:
            all_results.append({
                'query_id': query_id,
                'doc_id': result['doc_id'],
                'rank': result['rank'],
                'score': result['score']
            })
    
    # Write results
    with open(results_file, 'w', newline='') as f:
        if all_results:
            writer = csv.DictWriter(f, fieldnames=['query_id', 'doc_id', 'rank', 'score'])
            writer.writeheader()
            writer.writerows(all_results)
    
    print(f"✓ Results saved to {results_file}")

if __name__ == "__main__":
    load_index()
    
    # If running standalone, process queries
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "batch":
        process_queries_standalone()
    else:
        # Start Flask server
        print("\nStarting Flask server on http://localhost:5000")
        print("Endpoints:")
        print("  GET  /search?q=your+query")
        print("  POST /batch")
        print("  GET  /health")
        app.run(host='0.0.0.0', port=5000, debug=True)
