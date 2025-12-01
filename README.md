# 🚀 WORKING CS-429 Information Retrieval Project

## ✨ What You're Getting

A **COMPLETE, TESTED, WORKING** IR system that you can run right now!

### Features
Simple crawler
TF-IDF indexer with scikit-learn
Flask query processor
Complete documentation


---

## 📁 Project Structure

```
ir_project_working/
├── crawler/
│   └── simple_crawler.py      ← Crawls Wikipedia
├── indexer/
│   └── build_index.py          ← Builds TF-IDF index
├── processor/
│   └── query_processor.py      ← Handles queries
├── queries/
│   └── queries.csv             ← Sample queries
└── report/
    └── [Your notebook here]
```

Plus these will be created:
```
html/                           ← Crawled HTML files
├── [uuid].html (50 files)
└── url_mapping.json

indexer/ (output files)
├── index.json                  ← Sample for submission
├── doc_metadata.json
├── doc_ids.json
├── tfidf_vectorizer.pkl
└── tfidf_matrix.pkl

queries/ (output)
└── results.csv                 ← Ranked results
```

---

## 🎯 Quick Start

### Step 1: Install Dependencies
```bash
pip install requests beautifulsoup4 scikit-learn flask numpy lxml
```

### Step 2: Run Crawler
```bash
cd crawler
python3 simple_crawler.py
```

**Output:** 50 HTML files in `../html/`

### Step 3: Build Index
```bash
cd ../indexer
python3 build_index.py
```

**Output:** Index files created in current directory

### Step 4: Process Queries
```bash
cd ../processor
python3 query_processor.py batch
```

**Output:** `../queries/results.csv` with rankings

### Step 5: Check Results
```bash
# Check HTML files
ls ../html/*.html | wc -l    # Should show 50

# Check index
ls -lh *.json *.pkl

# Check results
cat ../queries/results.csv
```

---

## 🔍 How Each Component Works

### 1. Crawler (`simple_crawler.py`)

**What it does:**
- Starts at Wikipedia "Information Retrieval" page
- Follows links using BFS
- Saves 50 pages as HTML with UUID names
- Creates URL mapping

**Key features:**
- Rate limiting (1 sec delay)
- Polite crawling (proper User-Agent)
- Filters special pages
- Tracks visited URLs

**Run it:**
```bash
python3 simple_crawler.py
```

**Customize:**
```python
crawler = SimpleWikiCrawler(
    seed_url="https://en.wikipedia.org/wiki/Information_retrieval",
    max_pages=50,      # Change this!
    output_dir="../html"
)
```

### 2. Indexer (`build_index.py`)

**What it does:**
- Reads HTML files
- Extracts text with BeautifulSoup
- Builds inverted index with positions
- Creates TF-IDF vectors with scikit-learn

**Key features:**
- Bigram support (ngram_range=(1,2))
- Stop word removal
- Sparse matrix for efficiency
- Both JSON (sample) and pickle (full) output

**Run it:**
```bash
python3 build_index.py
```

**Output files:**
- `index.json` - Sample of inverted index
- `doc_metadata.json` - URLs, titles, lengths
- `tfidf_vectorizer.pkl` - For query vectorization
- `tfidf_matrix.pkl` - Document vectors

### 3. Query Processor (`query_processor.py`)

**What it does:**
- Loads index and TF-IDF model
- Processes queries
- Ranks using cosine similarity
- Returns top-K results

**Run standalone:**
```bash
python3 query_processor.py batch
```

**Or as Flask API:**
```bash
python3 query_processor.py
# Then: curl "http://localhost:5000/search?q=information+retrieval"
```

**Endpoints:**
- `GET /search?q=query&k=10` - Single query
- `POST /batch` - Process queries.csv
- `GET /health` - Check status

---

## 📊 Expected Results

### After Crawling:
```
✓ Crawl complete!
  Pages saved: 50
  Files in: ../html/
  Mapping: ../html/url_mapping.json
```

### After Indexing:
```
==================================================
INDEX STATISTICS
==================================================
Documents indexed: 50
Unique terms: 15234
Vocabulary size (TF-IDF): 5000
Average doc length: 1423 tokens
==================================================
```

### After Query Processing:
```
Processing 5 queries...
  Query: information retrieval systems
    Found 10 results
  Query: search engine algorithms
    Found 10 results
  ...
✓ Results saved to ../queries/results.csv
```

---

## 🐛 Troubleshooting

### Problem: "No module named 'requests'"
**Fix:**
```bash
pip install requests beautifulsoup4 scikit-learn flask numpy lxml
```

### Problem: "No HTML files found"
**Fix:**
```bash
# Make sure crawler ran successfully
cd crawler
python3 simple_crawler.py

# Check output
ls ../html/*.html
```

### Problem: "Connection timeout" during crawling
**Fix:**
```python
# In simple_crawler.py, increase timeout:
response = requests.get(url, headers=self.headers, timeout=30)  # was 10
```

### Problem: Query processor can't find files
**Fix:**
```bash
# Make sure you're in the processor/ directory
cd processor
python3 query_processor.py batch
```

---
