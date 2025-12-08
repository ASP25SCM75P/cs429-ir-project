#!/usr/bin/env python3
"""
Demo Document Generator
Creates synthetic Wikipedia-like documents for testing
Use this when network access is unavailable
"""

import uuid
import json
from pathlib import Path

# Sample Wikipedia-like content about IR topics
SAMPLE_DOCS = [
    {
        "title": "Information Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Information_retrieval",
        "content": """
        Information retrieval (IR) is the activity of obtaining information system resources that are 
        relevant to an information need from a collection of those resources. Searches can be based on 
        full-text or other content-based indexing. Information retrieval is the science of searching for 
        information in a document, searching for documents themselves, and also searching for the metadata 
        that describes data, and for databases of texts, images or sounds.
        
        Automated information retrieval systems are used to reduce what has been called information overload. 
        An IR system is a software system that provides access to books, journals and other documents; stores 
        and manages those documents. Web search engines are the most visible IR applications.
        """
    },
    {
        "title": "Search Engine - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Search_engine",
        "content": """
        A search engine is a software system designed to carry out web searches. They search the World Wide 
        Web in a systematic way for particular information specified in a textual web search query. The 
        search results are generally presented in a line of results, often referred to as search engine 
        results pages (SERPs).
        
        When a user enters a query into a search engine, the engine examines its index and provides a listing 
        of best-matching web pages according to its criteria, usually with a short summary containing the 
        document's title and sometimes parts of the text. Most search engines support the use of the boolean 
        operators AND, OR and NOT to help end users refine the search query.
        """
    },
    {
        "title": "Vector Space Model - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Vector_space_model",
        "content": """
        Vector space model or term vector model is an algebraic model for representing text documents as 
        vectors of identifiers, such as index terms. It is used in information filtering, information 
        retrieval, indexing and relevancy rankings. Its first use was in the SMART Information Retrieval 
        System.
        
        Documents and queries are represented as vectors. Each dimension corresponds to a separate term. 
        If a term occurs in the document, its value in the vector is non-zero. Several different ways of 
        computing these values, also known as term weights, have been developed. One of the best known 
        schemes is tf-idf weighting.
        """
    },
    {
        "title": "TF-IDF - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Tf-idf",
        "content": """
        In information retrieval, tf-idf or TFIDF, short for term frequency-inverse document frequency, 
        is a numerical statistic that is intended to reflect how important a word is to a document in a 
        collection or corpus. It is often used as a weighting factor in searches of information retrieval, 
        text mining, and user modeling.
        
        The tf-idf value increases proportionally to the number of times a word appears in the document 
        and is offset by the number of documents in the corpus that contain the word, which helps to 
        adjust for the fact that some words appear more frequently in general. tf-idf is one of the most 
        popular term-weighting schemes today.
        """
    },
    {
        "title": "Inverted Index - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Inverted_index",
        "content": """
        In computer science, an inverted index is a database index storing a mapping from content, such as 
        words or numbers, to its locations in a table, or in a document or a set of documents. The purpose 
        of an inverted index is to allow fast full-text searches, at a cost of increased processing when a 
        document is added to the database.
        
        The inverted index data structure is a central component of a typical search engine indexing algorithm. 
        A goal of a search engine implementation is to optimize the speed of the query: find the documents 
        where word X occurs. Once a forward index is developed, which stores lists of words per document, 
        it is next inverted to develop an inverted index.
        """
    },
    {
        "title": "Web Crawler - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Web_crawler",
        "content": """
        A Web crawler, sometimes called a spider or spiderbot and often shortened to crawler, is an Internet 
        bot that systematically browses the World Wide Web and that is typically operated by search engines 
        for the purpose of Web indexing.
        
        Web search engines and some other websites use Web crawling or spidering software to update their 
        web content or indices of other sites' web content. Web crawlers copy pages for processing by a 
        search engine, which indexes the downloaded pages so that users can search more efficiently. Crawlers 
        consume resources on visited systems and often visit sites without approval.
        """
    },
    {
        "title": "Boolean Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Boolean_retrieval",
        "content": """
        Boolean retrieval is a model in information retrieval in which we can pose any query which is in 
        the form of a Boolean expression of terms, that is, in which terms are combined with the operators 
        AND, OR, and NOT. The model views each document as just a set of words.
        
        Boolean queries are a fundamental building block of information retrieval systems. They allow users 
        to combine search terms using logical operators. For example, the query 'information AND retrieval' 
        would return documents containing both terms. Boolean retrieval is precise but can be difficult for 
        users who are unfamiliar with Boolean logic.
        """
    },
    {
        "title": "Cosine Similarity - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Cosine_similarity",
        "content": """
        Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space. 
        It is defined to equal the cosine of the angle between them, which is also the same as the inner 
        product of the same vectors normalized to both have length 1.
        
        The cosine similarity is particularly used in positive space, where the outcome is neatly bounded in 
        [0,1]. The cosine of 0° is 1, and it is less than 1 for any angle in the interval (0,π] radians. It 
        is thus a judgment of orientation and not magnitude. In the case of information retrieval, the cosine 
        similarity of two documents will range from 0 to 1, since the term frequencies cannot be negative.
        """
    },
    {
        "title": "PageRank - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/PageRank",
        "content": """
        PageRank (PR) is an algorithm used by Google Search to rank web pages in their search engine results. 
        It is named after both the term 'web page' and co-founder Larry Page. PageRank is a way of measuring 
        the importance of website pages.
        
        PageRank works by counting the number and quality of links to a page to determine a rough estimate of 
        how important the website is. The underlying assumption is that more important websites are likely to 
        receive more links from other websites. Currently, PageRank is not the only algorithm used by Google 
        to order search results, but it is the first algorithm that was used by the company.
        """
    },
    {
        "title": "Natural Language Processing - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Natural_language_processing",
        "content": """
        Natural language processing (NLP) is an interdisciplinary subfield of computer science and linguistics. 
        It is primarily concerned with giving computers the ability to support and manipulate human language. 
        It involves processing natural language datasets, such as text corpora or speech corpora, using either 
        rule-based or probabilistic machine learning approaches.
        
        The goal is a computer capable of understanding the contents of documents, including the contextual 
        nuances of the language within them. NLP has many applications including machine translation, sentiment 
        analysis, question answering, and information retrieval. Modern NLP techniques are based on machine 
        learning, especially statistical machine learning.
        """
    },
    {
        "title": "Document Classification - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Document_classification",
        "content": """
        Document classification or document categorization is a problem in library science, information science 
        and computer science. The task is to assign a document to one or more classes or categories. This may 
        be done manually or algorithmically. The intellectual classification of documents has mostly been the 
        province of library science, while the algorithmic classification of documents is mainly in information 
        science and computer science.
        
        The classification task is supervised learning; categories are known beforehand and documents are 
        classified into these predefined categories. This is in contrast to document clustering, which is 
        unsupervised learning. Modern approaches use machine learning methods including support vector machines, 
        neural networks, and deep learning.
        """
    },
    {
        "title": "Text Mining - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Text_mining",
        "content": """
        Text mining, also referred to as text data mining, similar to text analytics, is the process of deriving 
        high-quality information from text. It involves the discovery by computer of new, previously unknown 
        information, by automatically extracting information from different written resources.
        
        Text mining usually involves the process of structuring the input text, deriving patterns within the 
        structured data, and finally evaluation and interpretation of the output. High quality in text mining 
        usually refers to some combination of relevance, novelty, and interestingness. Typical text mining tasks 
        include text categorization, text clustering, concept extraction, sentiment analysis, document summarization, 
        and entity relation modeling.
        """
    },
    {
        "title": "Query Expansion - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Query_expansion",
        "content": """
        Query expansion (QE) is the process of reformulating a seed query to improve retrieval performance in 
        information retrieval operations. In the context of web search engines, query expansion involves 
        evaluating a user's input and expanding the search query to match additional documents.
        
        Query expansion involves techniques like finding synonyms of words, and analyzing word frequencies and 
        patterns. Automatic query expansion is a method for improving recall in information retrieval. The goal 
        is to increase the number of relevant documents retrieved while ideally not retrieving more irrelevant 
        documents. Methods include relevance feedback, pseudo-relevance feedback, and using thesauri like WordNet.
        """
    },
    {
        "title": "Precision and Recall - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Precision_and_recall",
        "content": """
        In pattern recognition, information retrieval and classification, precision is the fraction of relevant 
        instances among the retrieved instances, while recall is the fraction of relevant instances that were 
        retrieved. Both precision and recall are therefore based on relevance.
        
        Precision can be seen as a measure of quality, and recall as a measure of quantity. Higher precision 
        means that an algorithm returns more relevant results than irrelevant ones. Higher recall means that an 
        algorithm returns most of the relevant results. In information retrieval contexts, precision and recall 
        are used to evaluate the performance of search engines and other retrieval systems.
        """
    },
    {
        "title": "Relevance Feedback - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Relevance_feedback",
        "content": """
        Relevance feedback is a feature of some information retrieval systems. The idea behind relevance feedback 
        is to take the results that are initially returned from a given query and to use information about whether 
        or not those results are relevant to perform a new query.
        
        The user gives feedback on the relevance of documents in an initial set of results. The basic procedure is 
        to start with an initial query, retrieve documents, have the user mark documents as relevant or not relevant, 
        and then modify the query and repeat. Relevance feedback is most useful in systems where the user is unsure 
        of what they are looking for or how to express their information need.
        """
    },
    {
        "title": "Latent Semantic Analysis - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Latent_semantic_analysis",
        "content": """
        Latent semantic analysis (LSA) is a technique in natural language processing, in particular distributional 
        semantics, of analyzing relationships between a set of documents and the terms they contain by producing a 
        set of concepts related to the documents and terms.
        
        LSA assumes that words that are close in meaning will occur in similar pieces of text. A matrix containing 
        word counts per document is constructed from a large piece of text and a mathematical technique called 
        singular value decomposition (SVD) is used to reduce the number of rows while preserving the similarity 
        structure among columns. Documents are then compared by taking the cosine of the angle between the two vectors.
        """
    },
    {
        "title": "BM25 - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Okapi_BM25",
        "content": """
        BM25 is a ranking function used by search engines to estimate the relevance of documents to a given search 
        query. It is based on the probabilistic retrieval framework developed in the 1970s and 1980s by Stephen E. 
        Robertson, Karen Spärck Jones, and others.
        
        The name of the actual ranking function is BM25. The abbreviation BM stands for Best Matching. It is a 
        bag-of-words retrieval function that ranks a set of documents based on the query terms appearing in each 
        document, regardless of their proximity within the document. BM25 is widely used in modern search engines 
        and is considered one of the most effective ranking functions for information retrieval.
        """
    },
    {
        "title": "Stemming - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Stemming",
        "content": """
        In linguistic morphology and information retrieval, stemming is the process of reducing inflected words to 
        their word stem, base or root form. The stem need not be identical to the morphological root of the word; 
        it is usually sufficient that related words map to the same stem, even if this stem is not in itself a 
        valid root.
        
        A stemmer for English operating on the stem 'cat' should identify such strings as 'cats', 'catlike', and 
        'catty'. A stemming algorithm might also reduce the words 'fishing', 'fished', and 'fisher' to the stem 
        'fish'. The goal of stemming is to reduce different forms of a word to a common base form. The Porter 
        stemming algorithm is one of the most common stemming algorithms in use today.
        """
    },
    {
        "title": "Stop Words - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Stop_words",
        "content": """
        In computing, stop words are words which are filtered out before or after processing of natural language 
        data. There is no single universal list of stop words used by all natural language processing tools, and 
        indeed not all tools even use such a list.
        
        Some tools specifically avoid removing stop words to support phrase search. Any group of words can be chosen 
        as the stop words for a given purpose. For some search engines, these are some of the most common, short 
        function words, such as 'the', 'is', 'at', 'which', and 'on'. In this case, stop words can cause problems 
        when searching for phrases that include them. However, most modern information retrieval systems have evolved 
        to handle stop words more intelligently.
        """
    },
    {
        "title": "Bag of Words Model - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Bag-of-words_model",
        "content": """
        The bag-of-words model is a simplifying representation used in natural language processing and information 
        retrieval. In this model, a text is represented as the bag (multiset) of its words, disregarding grammar 
        and even word order but keeping multiplicity.
        
        The bag-of-words model is commonly used in methods of document classification where the occurrence of each 
        word is used as a feature for training a classifier. An example of the bag-of-words model is used in spam 
        filtering. The model has been used in computer vision as well. The bag-of-words model is one of the foundational 
        concepts in information retrieval and forms the basis for many modern search and classification techniques.
        """
    },
    {
        "title": "N-gram - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/N-gram",
        "content": """
        In the fields of computational linguistics and probability, an n-gram is a contiguous sequence of n items 
        from a given sample of text or speech. The items can be phonemes, syllables, letters, words or base pairs 
        according to the application. The n-grams typically are collected from a text or speech corpus.
        
        An n-gram of size 1 is referred to as a 'unigram'; size 2 is a 'bigram'; size 3 is a 'trigram'. Larger 
        sizes are sometimes referred to by the value of n in modern language, e.g., 'four-gram', 'five-gram', and 
        so on. In information retrieval, n-grams are useful for capturing phrases and multi-word expressions that 
        might be lost if only individual words are indexed.
        """
    },
    {
        "title": "Lucene - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Apache_Lucene",
        "content": """
        Apache Lucene is a free and open-source search engine software library, originally written completely in 
        Java by Doug Cutting. It is supported by the Apache Software Foundation and is released under the Apache 
        Software License. Lucene is widely regarded as the de facto standard open-source search library.
        
        Lucene has been ported to other programming languages including C#, C++, Python, and Ruby. Lucene is used 
        by many applications including Twitter search, LinkedIn, Wikipedia search, and many others. It provides 
        a powerful query language, efficient indexing, and fast search capabilities. Lucene forms the core of 
        Elasticsearch and Apache Solr, two of the most popular enterprise search platforms.
        """
    },
    {
        "title": "Elasticsearch - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Elasticsearch",
        "content": """
        Elasticsearch is a search engine based on the Lucene library. It provides a distributed, multitenant-capable 
        full-text search engine with an HTTP web interface and schema-free JSON documents. Elasticsearch is developed 
        in Java and is released as open source.
        
        Elasticsearch is commonly used for log analytics, full-text search, security intelligence, business analytics, 
        and operational intelligence use cases. It provides real-time search and analytics for all types of data. 
        Whether you have structured or unstructured text, numerical data, or geospatial data, Elasticsearch can 
        efficiently store and index it in a way that supports fast searches. The ELK stack (Elasticsearch, Logstash, 
        Kibana) is a popular combination for log management and analytics.
        """
    },
    {
        "title": "Word Embedding - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Word_embedding",
        "content": """
        In natural language processing, word embedding is a term used for the representation of words for text analysis, 
        typically in the form of a real-valued vector that encodes the meaning of the word such that the words that are 
        closer in the vector space are expected to be similar in meaning.
        
        Word embeddings can be obtained using a set of language modeling and feature learning techniques where words or 
        phrases from the vocabulary are mapped to vectors of real numbers. Methods include neural networks, dimensionality 
        reduction on the word co-occurrence matrix, and probabilistic models. Popular models include Word2Vec, GloVe, and 
        FastText. These representations have become fundamental in modern NLP and information retrieval systems.
        """
    },
    {
        "title": "BERT - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/BERT_(language_model)",
        "content": """
        BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based machine learning technique 
        for natural language processing pre-training developed by Google. BERT was created and published in 2018 by Jacob 
        Devlin and his colleagues from Google.
        
        In 2019, Google announced that it had begun leveraging BERT in its search engine, and by late 2020 it was being 
        used in almost every English-language query. BERT is designed to help computers understand the meaning of ambiguous 
        language in text by using surrounding text to establish context. The BERT framework was pre-trained using text from 
        Wikipedia and can be fine-tuned with question-and-answer datasets. BERT has significantly improved the state-of-the-art 
        in many NLP tasks including information retrieval.
        """
    },
    {
        "title": "Semantic Search - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Semantic_search",
        "content": """
        Semantic search denotes search with meaning, as distinguished from lexical search where the search engine looks for 
        literal matches of the query words or variants of them, without understanding the overall meaning of the query. 
        Semantic search seeks to improve search accuracy by understanding the searcher's intent and the contextual meaning 
        of terms.
        
        Semantic search systems consider various points including context of search, location, intent, variation of words, 
        synonyms, generalized and specialized queries, concept matching and natural language queries to provide relevant 
        search results. Technologies used in semantic search include knowledge graphs, natural language processing, machine 
        learning, and deep learning. Modern search engines increasingly incorporate semantic search capabilities.
        """
    },
    {
        "title": "Index Term - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Index_term",
        "content": """
        An index term, subject term, subject heading, or descriptor, in information retrieval, is a term that captures the 
        essence of the topic of a document. Index terms make up a controlled vocabulary for use in bibliographic records. 
        They are an integral part of bibliographic control, which is the function by which libraries collect, organize and 
        disseminate documents.
        
        Index terms are often referred to as keywords, tags, descriptive metadata, taxonomies, controlled vocabularies and 
        thesauri. In information retrieval systems, index terms are extracted from documents or assigned by human indexers. 
        The choice of index terms significantly affects retrieval effectiveness. Automatic indexing methods extract terms 
        based on statistical properties of the text, while manual indexing relies on human judgment.
        """
    },
    {
        "title": "Ranking Function - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Ranking_(information_retrieval)",
        "content": """
        Ranking of query results is an important operation in information retrieval. When a query is submitted, the search 
        engine returns a list of documents in order of relevance to that query. The goal of ranking is to present the most 
        relevant documents first, minimizing the user's effort in finding what they need.
        
        Various ranking functions have been developed over the years. Classic methods include TF-IDF and BM25. Modern search 
        engines use machine learning approaches including learning to rank, neural networks, and ensemble methods. Factors 
        considered in ranking may include term frequency, document frequency, document length normalization, proximity of 
        query terms, PageRank, click-through rates, and many others. The effectiveness of a ranking function is typically 
        measured using metrics like precision, recall, and mean average precision.
        """
    },
    {
        "title": "Query Processing - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Query_language",
        "content": """
        Query processing in information retrieval is the process of deciding which documents in a collection should be 
        retrieved for a user query. The process involves query parsing, query transformation, document matching, and 
        result ranking. Modern search engines must process queries efficiently even with very large document collections.
        
        Query processing typically begins with query parsing where the user's input is analyzed and potentially transformed. 
        This may involve spell checking, stemming, stop word removal, and query expansion. The transformed query is then 
        matched against the index to identify candidate documents. Finally, a ranking function scores and orders the results. 
        Optimization techniques like caching, index compression, and parallel processing are crucial for handling the scale 
        of modern web search.
        """
    },
    {
        "title": "Information Overload - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Information_overload",
        "content": """
        Information overload is the difficulty in understanding an issue and effectively making decisions when one has too 
        much information about that issue. Generally, the term is associated with the excessive quantity of daily information. 
        The term was popularized by Alvin Toffler in his bestselling 1970 book Future Shock.
        
        Information overload is one of the primary motivations for developing information retrieval systems. Search engines, 
        recommender systems, and filtering tools are all designed to help users navigate the vast amount of information 
        available, particularly on the internet. Techniques for dealing with information overload include better search 
        algorithms, personalization, collaborative filtering, and information visualization. As the amount of digital 
        information continues to grow exponentially, managing information overload remains a critical challenge.
        """
    },
    {
        "title": "Digital Library - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Digital_library",
        "content": """
        A digital library is an online database of digital objects that can include text, still images, audio, video, digital 
        documents, or other digital media formats. Objects can consist of digitized content like print or photographs, as well 
        as originally produced digital content like word processor files or social media posts.
        
        Digital libraries provide access to information resources and services through the Internet. They support information 
        retrieval through search interfaces and browsing capabilities. Key challenges include metadata creation, preservation, 
        copyright management, and ensuring long-term access. Major digital libraries include Google Books, Internet Archive, 
        Project Gutenberg, and institutional repositories. Information retrieval techniques are essential for making digital 
        library collections accessible and useful.
        """
    },
    {
        "title": "Machine Learning in IR - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Machine_learning",
        "content": """
        Machine learning has become increasingly important in information retrieval. Machine learning is a method of data 
        analysis that automates analytical model building. It is a branch of artificial intelligence based on the idea that 
        systems can learn from data, identify patterns and make decisions with minimal human intervention.
        
        In information retrieval, machine learning is used for tasks including ranking, query understanding, spam detection, 
        personalization, and relevance feedback. Learning to rank is a particularly important application where machine 
        learning models are trained to optimize ranking functions. Features used in these models may include term frequencies, 
        click-through rates, document quality signals, and many others. Modern search engines rely heavily on machine learning 
        to improve search quality and user experience.
        """
    },
    {
        "title": "Faceted Search - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Faceted_search",
        "content": """
        Faceted search, also called faceted navigation or faceted browsing, is a technique for accessing information organized 
        according to a faceted classification system, allowing users to explore a collection of information by applying multiple 
        filters. A faceted classification system classifies each information element along multiple explicit dimensions.
        
        Faceted search is widely used in e-commerce websites and library catalogs. Users can progressively narrow down search 
        results by selecting from available facets. For example, when shopping for a laptop, facets might include price range, 
        brand, screen size, and processor type. Faceted search provides a powerful alternative to traditional keyword search, 
        especially when users are exploring a space rather than looking for a specific item. Implementation requires careful 
        design of the facet structure and efficient indexing for real-time filtering.
        """
    },
    {
        "title": "Document Clustering - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Document_clustering",
        "content": """
        Document clustering is a technique for organizing a collection of documents into meaningful groups, or clusters, such 
        that documents within a cluster are more similar to each other than to documents in other clusters. This is a form of 
        unsupervised learning since the clusters are not predefined.
        
        Document clustering has applications in organizing search results, detecting topics in a collection, and improving 
        search efficiency. Common algorithms include k-means, hierarchical clustering, and density-based methods. The similarity 
        between documents is typically measured using cosine similarity on TF-IDF vectors or other document representations. 
        Document clustering can help users explore large document collections and discover relationships between documents that 
        might not be obvious from keyword search alone.
        """
    },
    {
        "title": "Collaborative Filtering - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Collaborative_filtering",
        "content": """
        Collaborative filtering is a method of making automatic predictions about the interests of a user by collecting 
        preferences or taste information from many users. The underlying assumption is that if person A has the same opinion 
        as person B on an issue, A is more likely to have B's opinion on a different issue than that of a randomly chosen person.
        
        While not strictly an information retrieval technique, collaborative filtering is closely related and is used in many 
        information access systems including recommender systems. Netflix, Amazon, and Spotify all use collaborative filtering 
        to recommend content. Methods include user-based collaborative filtering, item-based collaborative filtering, and 
        matrix factorization. Collaborative filtering can complement traditional IR techniques by personalizing search results 
        and recommendations based on the behavior of similar users.
        """
    },
    {
        "title": "Cross-Language Information Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Cross-language_information_retrieval",
        "content": """
        Cross-language information retrieval (CLIR) is a subfield of information retrieval dealing with retrieving information 
        written in a language different from the language of the user's query. For example, a user might submit a query in 
        English to search for documents in French, German, or Japanese.
        
        CLIR systems must address the challenge of matching concepts across languages. Approaches include query translation, 
        document translation, and using interlingual representations. Machine translation systems, bilingual dictionaries, and 
        parallel corpora are key resources. Modern approaches leverage neural machine translation and multilingual word embeddings. 
        CLIR is increasingly important as the web becomes more multilingual and users need access to information regardless of 
        language barriers.
        """
    },
    {
        "title": "Question Answering - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Question_answering",
        "content": """
        Question answering (QA) is a computer science discipline within the fields of information retrieval and natural language 
        processing (NLP) which is concerned with building systems that automatically answer questions posed by humans in a natural 
        language. A QA system is a type of information retrieval system.
        
        Question answering systems can be classified as either open-domain, which attempt to answer questions about nearly anything, 
        or closed-domain, which focus on a specific domain. Modern QA systems use techniques from information retrieval, natural 
        language processing, and machine learning. They typically involve question analysis, document retrieval, answer extraction, 
        and answer validation. Recent advances using transformers like BERT have significantly improved QA performance. Virtual 
        assistants like Siri, Alexa, and Google Assistant incorporate QA capabilities.
        """
    },
    {
        "title": "Snippet Generation - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Web_search_query",
        "content": """
        A snippet is a brief summary or excerpt from a document that is displayed in search results. Snippet generation is an 
        important component of search engine results pages (SERPs) as it helps users quickly determine which results are most 
        relevant to their query without having to visit each page.
        
        Effective snippets typically highlight the query terms in context and show the most relevant portions of the document. 
        Techniques for snippet generation include extracting sentences containing query terms, using document abstracts or 
        metadata, and generating summaries using natural language processing. Query-biased summarization aims to create snippets 
        that specifically address the user's query. Rich snippets may include additional structured data like ratings, prices, 
        or images. The quality of snippets significantly affects click-through rates and user satisfaction.
        """
    },
    {
        "title": "Index Compression - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Data_compression",
        "content": """
        Index compression is crucial for large-scale information retrieval systems. Inverted indexes for web-scale collections 
        can be enormous, and compression techniques are essential for reducing storage costs and improving query processing speed 
        by allowing more of the index to fit in memory.
        
        Common compression techniques for inverted indexes include variable byte encoding, gamma codes, and delta encoding of 
        document IDs. Positional information is particularly expensive to store and benefits significantly from compression. 
        The trade-off between compression ratio and decompression speed must be carefully balanced. Modern search engines achieve 
        compression ratios of 10:1 or better while maintaining fast query processing. Compression is applied not only to posting 
        lists but also to the lexicon and document store.
        """
    },
    {
        "title": "Click-Through Rate - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Click-through_rate",
        "content": """
        Click-through rate (CTR) is the ratio of users who click on a specific link to the number of total users who view a page, 
        email, or advertisement. In information retrieval, CTR is an important metric for evaluating search result quality and 
        can be used as implicit relevance feedback.
        
        Search engines analyze click-through data to improve ranking algorithms. If users frequently skip the top result to click 
        on a lower-ranked result, this signals that the ranking may need adjustment. CTR data is used in learning-to-rank systems 
        as a feature for training ranking models. However, CTR can be influenced by factors beyond relevance, such as snippet 
        quality and position bias. Position bias refers to the tendency of users to click on higher-ranked results regardless of 
        relevance. Accounting for these biases is important when using CTR data for improving search quality.
        """
    },
    {
        "title": "Entity Linking - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Entity_linking",
        "content": """
        Entity linking, also called named entity disambiguation or named entity normalization, is the task of determining the 
        identity of entities mentioned in text. For example, the word 'Paris' could refer to the city in France, the city in 
        Texas, or Paris Hilton. Entity linking systems disambiguate such mentions by linking them to entries in a knowledge base.
        
        Entity linking is important for semantic search and information retrieval because it helps systems understand what documents 
        are about beyond simple keyword matching. Knowledge graphs like Wikipedia, DBpedia, and Wikidata serve as common targets 
        for entity linking. Modern entity linking systems use machine learning and consider features like context, entity popularity, 
        and string similarity. Once entities are linked, they enable more sophisticated retrieval operations like finding all 
        documents about a particular person, place, or organization regardless of how they're named in the text.
        """
    },
    {
        "title": "Distributed Information Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Distributed_computing",
        "content": """
        Distributed information retrieval involves searching across multiple independent search engines or document collections. 
        This is necessary when documents are distributed across multiple sites or when a single collection is too large to be 
        handled by one system. The web itself is inherently a distributed information space.
        
        Key challenges in distributed IR include resource selection (choosing which collections to search), query routing, and 
        result merging. Federated search systems search multiple sources simultaneously and combine results. Modern search engines 
        like Google and Bing use distributed architectures with thousands of servers to handle indexing and query processing at 
        web scale. MapReduce and similar frameworks enable parallel processing of large-scale IR tasks. Cloud computing platforms 
        provide infrastructure for building distributed IR systems.
        """
    },
    {
        "title": "Information Seeking Behavior - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Information_seeking",
        "content": """
        Information seeking behavior refers to the way people search for and utilize information. Understanding information seeking 
        behavior is important for designing effective information retrieval systems. Research has identified various information 
        seeking patterns and strategies that users employ when looking for information.
        
        Models of information seeking include Kuhlthau's information search process, Bates' berrypicking model, and Ellis' model of 
        information seeking behavior. Users may engage in exploratory search when their information need is unclear, or known-item 
        search when looking for a specific document. Search behavior often involves query reformulation, browsing, and navigating 
        through results. Modern IR systems aim to support various information seeking behaviors through features like query suggestions, 
        related searches, faceted navigation, and personalization. Understanding user behavior helps in designing better interfaces and 
        ranking algorithms.
        """
    },
    {
        "title": "Evaluation Metrics - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)",
        "content": """
        Evaluation is crucial in information retrieval for measuring the effectiveness of systems and algorithms. Standard evaluation 
        metrics include precision, recall, F-measure, mean average precision (MAP), normalized discounted cumulative gain (NDCG), and 
        mean reciprocal rank (MRR).
        
        Precision measures the fraction of retrieved documents that are relevant. Recall measures the fraction of relevant documents 
        that are retrieved. These metrics often trade off against each other. MAP provides a single-figure measure of quality across 
        recall levels. NDCG is particularly useful for web search where relevance is graded rather than binary. Test collections like 
        TREC provide standardized benchmarks for comparing different IR systems. Offline evaluation using test collections is complemented 
        by online evaluation using A/B testing and click-through analysis. Good evaluation methodology is essential for advancing the 
        field of information retrieval.
        """
    },
    {
        "title": "Personalized Search - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Personalized_search",
        "content": """
        Personalized search refers to web search experiences that are tailored specifically to an individual's interests by incorporating 
        information about the individual beyond the specific query provided. Search engines can personalize results based on factors like 
        search history, location, preferences, and social connections.
        
        While personalization can improve search quality by providing more relevant results, it also raises privacy concerns and can create 
        filter bubbles where users are primarily exposed to information that confirms their existing views. Personalization techniques include 
        user profiling, collaborative filtering, and contextual factors. Major search engines like Google provide personalized results by 
        default, though users can opt out or use incognito mode. Balancing personalization benefits with privacy and diversity concerns 
        remains an ongoing challenge in information retrieval.
        """
    },
    {
        "title": "Multimedia Information Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Multimedia",
        "content": """
        Multimedia information retrieval extends traditional text-based IR to handle images, audio, video, and other media types. This field 
        addresses the challenges of searching, browsing, and organizing multimedia content. As multimedia content on the web continues to grow, 
        effective multimedia IR becomes increasingly important.
        
        Content-based image retrieval (CBIR) systems search images based on visual features like color, texture, and shape. Video retrieval 
        systems may use shot detection, keyframe extraction, and audio analysis. Music information retrieval systems can search by melody, 
        rhythm, or lyrics. Modern approaches use deep learning to extract high-level semantic features from multimedia content. Multimodal 
        retrieval systems can search across different media types, for example, finding videos relevant to a text query. Multimedia IR also 
        involves challenges in metadata extraction, similarity measurement, and result presentation.
        """
    },
    {
        "title": "Mobile Information Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Mobile_search",
        "content": """
        Mobile information retrieval focuses on the unique challenges and opportunities of information access on mobile devices like 
        smartphones and tablets. Mobile search differs from desktop search in important ways including smaller screens, touch interfaces, 
        voice input, and location awareness.
        
        Mobile queries tend to be shorter and more conversational. Location-based search is particularly important for mobile users looking 
        for nearby businesses, services, or points of interest. Voice search through digital assistants has become increasingly popular on 
        mobile devices, requiring systems to handle natural language queries and spoken commands. Mobile IR systems must optimize for limited 
        bandwidth, varying connectivity, and battery consumption. Responsive design and mobile-specific result formatting are crucial. The 
        mobile-first indexing approach by search engines reflects the importance of mobile search.
        """
    },
    {
        "title": "Privacy in Information Retrieval - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Privacy",
        "content": """
        Privacy is an important concern in information retrieval systems. Search queries can reveal sensitive information about users' 
        interests, health conditions, political views, and personal situations. Search engines collect vast amounts of data about search 
        behavior, which raises privacy concerns even as it enables personalization and service improvements.
        
        Privacy-preserving IR techniques include anonymous search, encrypted search, and differential privacy. Private information retrieval 
        (PIR) protocols allow users to retrieve information from databases without revealing what they accessed. However, truly private search 
        often comes at the cost of reduced functionality or performance. Regulations like GDPR have increased attention to privacy in IR systems. 
        Search engines now provide controls for viewing and deleting search history. Balancing the benefits of data collection for service 
        improvement against user privacy remains a fundamental challenge in information retrieval.
        """
    },
    {
        "title": "Real-Time Search - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Real-time_web",
        "content": """
        Real-time search enables users to find the most recent information as events unfold. This is particularly important for news, social 
        media, and other rapidly updated content. Real-time search goes beyond traditional web crawling, which may take days or weeks to discover 
        and index new content.
        
        Social media platforms like Twitter pioneered real-time search, allowing users to find tweets about current events within seconds of 
        posting. Search engines have incorporated real-time features through news sections and specialized indexing of frequently updated sources. 
        Technical challenges include incremental indexing, handling high update rates, and determining result freshness. Streaming data processing 
        frameworks enable real-time analysis of new content. Real-time search systems must balance freshness with relevance and quality. The 
        recency ranking factor gives newer documents higher weight when appropriate. Real-time search is essential for applications like emergency 
        response, financial markets, and trend detection.
        """
    },
    {
        "title": "Social Search - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Social_search",
        "content": """
        Social search refers to systems that incorporate social signals and relationships into search results and recommendations. These systems 
        leverage the collective intelligence of social networks to improve information discovery. The assumption is that information shared or 
        endorsed by trusted connections is more likely to be relevant and reliable.
        
        Social search features include incorporating likes, shares, and comments into ranking; showing results from friends' activities; and 
        enabling question-answering within social networks. Hash tags on social media platforms function as a distributed classification system. 
        Social bookmarking sites like Delicious pioneered social search concepts. Major search engines have experimented with social signals, 
        though privacy concerns and the risk of manipulation have limited their use. Social search can be particularly effective in niche communities 
        where members share specialized knowledge. The challenge is determining which social signals are truly indicative of quality and relevance.
        """
    },
    {
        "title": "Vertical Search - Wikipedia",
        "url": "https://en.wikipedia.org/wiki/Vertical_search",
        "content": """
        Vertical search engines focus on specific segments of online content or particular domains. Unlike general web search engines that attempt 
        to index the entire web, vertical search engines specialize in areas like shopping, travel, local business, jobs, or academic papers. This 
        specialization allows them to provide deeper functionality and better results within their domain.
        
        Examples include Google Scholar for academic content, Indeed for jobs, Zillow for real estate, and Yelp for local businesses. Vertical search 
        engines can offer domain-specific search features, specialized ranking algorithms, and richer metadata that wouldn't be practical for general 
        search. They may include structured data filtering, comparison tools, and booking capabilities. Major search engines often integrate vertical 
        search results into their general search results as specialized result blocks or cards. The trade-off is between the breadth of general search 
        and the depth of vertical search.
        """
    },
]

def generate_documents(output_dir="../html", num_docs=50):
    """Generate synthetic documents"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)
    
    print(f"Generating {min(num_docs, len(SAMPLE_DOCS))} synthetic documents...")
    print(f"Output directory: {output_path}/")
    print("-" * 60)
    
    url_mapping = {
        'url_to_docid': {},
        'docid_to_url': {}
    }
    
    # Use available documents (may be less than requested if SAMPLE_DOCS is smaller)
    docs_to_generate = min(num_docs, len(SAMPLE_DOCS))
    
    for i, doc in enumerate(SAMPLE_DOCS[:docs_to_generate], 1):
        # Generate UUID
        doc_id = str(uuid.uuid4())
        
        # Create HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{doc['title']}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>{doc['title'].replace(' - Wikipedia', '')}</h1>
    {doc['content']}
</body>
</html>"""
        
        # Save HTML file with URL comment
        html_file = output_path / f"{doc_id}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(f"<!-- URL: {doc['url']} -->\n")
            f.write(html_content)
        
        # Track mapping
        url_mapping['url_to_docid'][doc['url']] = doc_id
        url_mapping['docid_to_url'][doc_id] = doc['url']
        
        print(f"[{i}/{docs_to_generate}] Created: {doc['title'][:50]}...")
    
    # Save URL mapping
    mapping_file = output_path / "url_mapping.json"
    with open(mapping_file, 'w') as f:
        json.dump(url_mapping, f, indent=2)
    
    print("-" * 60)
    print(f"✓ Generation complete!")
    print(f"  Documents created: {docs_to_generate}")
    print(f"  Files in: {output_path}/")
    print(f"  Mapping: {mapping_file}")
    
    return docs_to_generate

if __name__ == "__main__":
    import sys
    num_docs = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    generate_documents(output_dir="../html", num_docs=num_docs)
