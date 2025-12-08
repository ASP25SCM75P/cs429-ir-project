# CS-429 Information Retrieval System

## Features

-  Scrapy-based crawler
-  Synthetic HTML document generator (Scrapy is included, but synthetic generation is used by default for reproducibility.)
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
