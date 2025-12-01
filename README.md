# CS-429 Information Retrieval System

## Features

-  Scrapy-based crawler
-  Synthetic HTML document generator
-  TF-IDF indexer with scikit-learn
-  Cosine similarity query processor
-  Full Jupyter Notebook report

---

##  Project Structure

```
cs429-ir-project/
├── crawler/
│   ├── simple_crawler.py          ← Scrapy crawler
│   └── generate_demo_docs.py      ← Synthetic HTML generator
│
├── html/                          ← HTML document collection
│   └── [UUID].html
│
├── indexer/
│   └── build_index.py             ← Builds TF-IDF index + inverted index
│
├── processor/
│   └── query_processor.py         ← Handles queries and ranking
│
├── queries/
│   ├── queries.csv                ← Input queries
│   └── results.csv                ← Ranked output
│
├── report/
│   ├── COMPLETE_REPORT.ipynb      ← Full notebook report
│   └── COMPLETE_REPORT.pdf
│
├── requirements.txt
└── verify.py
```

### Files Created During Execution

```
indexer/ (output files)
├── index.json
├── doc_metadata.json
├── doc_ids.json
├── inverted_index_full.pkl
├── tfidf_vectorizer.pkl
└── tfidf_matrix.pkl

queries/
└── results.csv
```

---

##  Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install requests beautifulsoup4 scikit-learn flask numpy lxml pandas scrapy
```

### Step 2: Generate Documents

#### Option A — Synthetic (recommended for reproducibility)

```bash
cd crawler
python3 generate_demo_docs.py 50
```

Creates 50 HTML files in:

```
../html/
```

#### Option B — Scrapy Crawler

```bash
cd crawler
scrapy crawl simple -a start_url="https://en.wikipedia.org/wiki/Information_retrieval" \
                    -a max_pages=20 -a max_depth=1 \
                    -O data/crawled_html/mapping.json
```

Outputs to:

```
data/crawled_html/
```

### Step 3: Build Index

```bash
cd ../indexer
python3 build_index.py
```

**Creates:**
- TF-IDF vectorizer
- TF-IDF matrix
- Inverted index
- Metadata

### Step 4: Process Queries

#### Batch mode

```bash
cd ../processor
python3 query_processor.py batch
```

Creates:

```
../queries/results.csv
```

#### Flask API mode

```bash
python3 query_processor.py
```

Then open:

```
http://localhost:5000/search?q=information+retrieval
```

---

##  How Each Component Works

### 1. Crawler (`simple_crawler.py`)

**What it does:**
- Uses Scrapy to fetch real HTML pages
- Supports configurable seed URL, depth, and max pages
- Saves all pages as UUID-named HTML files

**Run it:**

```bash
scrapy crawl simple
```

### 2. Synthetic Document Generator (`generate_demo_docs.py`)

**What it does:**
- Creates a consistent, stable collection of HTML documents
- Designed for grading and reproducibility
- Pulls Wikipedia snippets and formats them into HTML

**Run it:**

```bash
python3 generate_demo_docs.py 50
```

### 3. Indexer (`build_index.py`)

**What it does:**
- Extracts text from HTML
- Builds inverted index with terms and positions
- Creates TF-IDF vectors using scikit-learn

**Key features:**
- Bigram support (1–2 grams)
- Stopword removal
- Sparse TF-IDF matrices

### 4. Query Processor (`query_processor.py`)

**What it does:**
- Loads TF-IDF model and matrix
- Preprocesses query text
- Computes cosine similarity against all documents
- Returns top-K results

**Run it:**

```bash
python3 query_processor.py batch
```

---

##  Expected Results

### After Document Generation:

```
Generated 50 synthetic documents
Output directory: ../html/
```

### After Indexing:

```
==================================================
Indexing complete
Documents indexed: 50
Unique terms: XXXX
Vocabulary size: XXXX
==================================================
```

### After Query Processing:

```
Processing queries.csv...
Saved ranked results to ../queries/results.csv
```

---

##  Troubleshooting

### Problem: "No HTML files found"

**Fix:**

```bash
cd crawler
python3 generate_demo_docs.py 50
```

### Problem: "Module not found"

**Fix:**

```bash
pip install -r requirements.txt
```

### Problem: Scrapy not installed

**Fix:**

```bash
pip install scrapy
```

### Problem: Query processor can't find index files

**Fix:**

```bash
cd indexer
python3 build_index.py
```

---

##  Requirements

### Python Version
- Python 3.8 or higher

### Required Packages
```
requests
beautifulsoup4
scikit-learn
flask
numpy
lxml
pandas
scrapy
```

---

##  Complete Workflow Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate documents
cd crawler
python3 generate_demo_docs.py 50

# 3. Build index
cd ../indexer
python3 build_index.py

# 4. Process queries
cd ../processor
python3 query_processor.py batch

# 5. View results
cat ../queries/results.csv
```

---

##  Documentation

Full project documentation is available in:
- `report/COMPLETE_REPORT.ipynb` - Interactive Jupyter notebook
- `report/COMPLETE_REPORT.pdf` - PDF export of the report

---

## Academic Information

**Course:** CS-429 Information Retrieval  
**Institution:** Illinois Institute of Technology  
**Instructor:** Professor Jawahar Panchal

---

##  System Architecture

```
┌─────────────────┐
│  HTML Documents │
│   (Crawler)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Extraction│
│   & Indexing    │
│   (build_index) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TF-IDF Model  │
│ Inverted Index  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Query Processor │
│ (Cosine Sim.)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Ranked Results  │
│  (results.csv)  │
└─────────────────┘
```

---

## Technical Details

### TF-IDF Configuration
- **N-gram range:** 1-2 (unigrams and bigrams)
- **Max features:** Configurable
- **Stop words:** English stopwords removed
- **Sublinear TF:** Enabled

### Cosine Similarity
- Uses sparse matrix operations for efficiency
- Returns top-K documents by relevance score
- Scores range from 0.0 (no match) to 1.0 (perfect match)

### Query Processing
- Query text is preprocessed with same pipeline as documents
- TF-IDF transformation applied to query vector
- Cosine similarity computed against all document vectors

---


## Author

Aryan Pathak
Illinois Institute of Technology  
CS-429 Information Retrieval

---

## Acknowledgments

- Professor Jawahar Panchal for course instruction
- scikit-learn for TF-IDF implementation
- Scrapy framework for web crawling capabilities
- Wikipedia for synthetic document content

---

## Support

For issues or questions regarding this project, please refer to the course materials or contact the instructor.

---
