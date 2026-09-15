# CertFlow RAG Assistant

**CertFlow RAG Assistant** is a Retrieval-Augmented Generation (RAG) project for answering questions about synthetic enterprise **Account Data Certification** documentation.

The system is designed as an analyst decision-support assistant: it retrieves relevant policy sections, passes the retrieved context to an LLM, and generates a grounded answer with source references. It does **not** make certification decisions autonomously.

> **Project status:** Core RAG pipeline implemented and evaluated. UI and deployment are the main remaining productization steps.

---

## Business Problem

Enterprise data-governance teams often work with policies, validation rules, evidence requirements, source hierarchies, exception procedures, and escalation guidance distributed across multiple documents.

Manually locating the correct rule can be slow and can lead to inconsistent interpretation. CertFlow demonstrates how a RAG system can make this information easier to retrieve while preserving document and section traceability.

Example questions:

- What evidence is required before an account can be certified?
- Which source should be used when systems contain conflicting information?
- When should a certification case be escalated?
- How should potential duplicate accounts be handled?
- What rules apply when an account legal name changes?

---

## Current Architecture

```text
10 synthetic policy documents
        ↓
YAML metadata parsing
        ↓
Structure-aware Markdown chunking
        ↓
81 section-level chunks
        ↓
SentenceTransformer embeddings
multi-qa-MiniLM-L6-cos-v1
        ↓
FAISS dense retrieval
        ↓
Top-k policy sections
        ↓
Context construction
        ↓
OpenAI generation
        ↓
Grounded answer + sources
```

The project also evaluates alternative retrieval strategies including **BGE embeddings, BM25, Reciprocal Rank Fusion (RRF), weighted RRF, and CrossEncoder reranking**. The final retrieval strategy is selected from measured evaluation results rather than architecture complexity.

---

## Knowledge Base

The repository contains **10 synthetic enterprise documents** in both Markdown and PDF format:

```text
01_account_certification_overview
02_roles_and_responsibilities
03_end_to_end_certification_workflow
04_account_fields_and_validation_rules
05_source_hierarchy_and_evidence
06_address_certification_and_duplicate_prevention
07_request_types_and_change_management
08_quality_review_exceptions_and_escalations
09_frequently_asked_questions
10_policy_change_log
```

Source files:

```text
data/raw/source_markdown/
data/raw/pdf/
```

Synthetic documentation is used so the project can reproduce a realistic enterprise RAG use case without exposing confidential company information.

---

## Metadata and Chunking

Each Markdown document contains structured YAML metadata such as:

```yaml
document_id: ACD-KB-001
title: Account Data Certification Overview
document_type: policy
version: "1.0"
effective_date: 2026-04-01
last_updated: 2026-03-15
owner: Master Data Governance Team
status: active
confidentiality: internal
```

The ingestion pipeline uses document structure rather than arbitrary fixed-length splitting. Markdown `##` sections are converted into section-level chunks while document metadata is propagated to every chunk.

Example:

```json
{
  "chunk_id": "ACD-KB-001-chunk-001",
  "content": "...",
  "metadata": {
    "document_id": "ACD-KB-001",
    "title": "Account Data Certification Overview",
    "version": "1.0",
    "status": "active",
    "section": "Purpose",
    "section_number": 1
  }
}
```

Current output:

**10 documents → 81 structured chunks**

Serialized chunks are stored in:

```text
data/raw/processed/chunks.json
```

---

## Retrieval Experiments

Retrieval was evaluated on a **20-query labelled evaluation set** using section-level relevance targets.

### Embedding model comparison

Two sentence embedding models were compared:

| Model | Hit@5 | MRR@5 |
|---|---:|---:|
| `multi-qa-MiniLM-L6-cos-v1` | **0.85** | **0.618** |
| `BAAI/bge-small-en-v1.5` | 0.75 | 0.499 |

`multi-qa-MiniLM-L6-cos-v1` was retained as the dense retrieval baseline.

### Dense, BM25 and hybrid retrieval

| Retrieval strategy | Hit@5 | MRR@5 |
|---|---:|---:|
| Dense + FAISS | **0.85** | **0.618** |
| BM25 | 0.35 | 0.233 |
| Unweighted RRF | 0.70 | 0.422 |
| Weighted RRF (0.8 dense / 0.2 BM25) | 0.75 | 0.488 |

For this knowledge base, semantic similarity was more effective than lexical overlap. Adding BM25 through RRF did not improve the stronger dense retriever.

### Reranking experiment

A CrossEncoder (`cross-encoder/ms-marco-MiniLM-L6-v2`) was evaluated on top of dense retrieval.

| Retrieval strategy | Hit@5 | MRR@5 |
|---|---:|---:|
| Dense FAISS baseline | **0.85** | **0.618** |
| Dense FAISS + CrossEncoder | 0.75 | 0.571 |

The reranker reduced retrieval coverage and ranking quality by sometimes promoting broadly related passages over the most specific policy sections. It was therefore **not selected** for the final pipeline.

### Final retrieval choice

```text
multi-qa-MiniLM-L6-cos-v1
        ↓
normalized embeddings
        ↓
FAISS IndexFlatIP
        ↓
Top-k dense retrieval
```

This is intentionally simpler than the tested hybrid/reranking alternatives because it achieved the best measured retrieval performance.

---

## End-to-End RAG Pipeline

The reusable pipeline is implemented in:

```text
src/rag/rag_pipeline.py
```

Core flow:

```text
User question
     ↓
DenseRetriever
     ↓
Top-k chunks
     ↓
build_context()
     ↓
OpenAI Responses API
     ↓
Grounded answer
     ↓
Document + section sources
```

The current implementation uses:

- `SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")`
- normalized dense embeddings
- `faiss.IndexFlatIP` for cosine-similarity retrieval
- top-k retrieval (default `k=5`)
- a controlled system prompt that instructs the model to use only retrieved context
- explicit fallback when documentation is insufficient
- document and section references in generated answers

The generation model is configurable in `rag_pipeline.py`, and the OpenAI API key is read from `OPENAI_API_KEY` or passed directly to `CertFlowRAG`.

---

## Generation Evaluation

Generation quality is evaluated separately from retrieval quality in:

```text
src/rag/02_generation_evaluation.ipynb
```

The evaluation measures four dimensions on a 0–2 scale:

- correctness;
- faithfulness;
- relevance;
- source grounding.

Average results across the evaluation set:

| Metric | Score |
|---|---:|
| Correctness | **1.80 / 2.00** |
| Faithfulness | **1.95 / 2.00** |
| Relevance | **1.95 / 2.00** |
| Source grounding | **1.85 / 2.00** |

**14 of 20 answers (70%) achieved perfect scores across all four criteria.**

The evaluation indicates that the system generally remains grounded in retrieved context and answers questions directly. Remaining errors are useful signals for improving retrieval specificity and source attribution rather than simply increasing pipeline complexity.

---

## Repository Structure

```text
certflow-rag-assistant/
│
├── data/
│   └── raw/
│       ├── pdf/                         # 10 PDF knowledge-base documents
│       ├── source_markdown/             # 10 Markdown source documents
│       └── processed/
│           └── chunks.json              # 81 structured chunks
│
├── notebooks/
│   └── 01_domain_knowledge_base_design.ipynb
│
├── src/
│   ├── ingestion/
│   │   └── chunker.ipynb
│   │
│   ├── retrieval/
│   │   ├── 01_embeddings.ipynb
│   │   ├── 02_bm25_hybrid_retrieval.ipynb
│   │   └── 03_reranking.ipynb
│   │
│   └── rag/
│       ├── 01_end_to_end_rag_baseline.ipynb
│       ├── 02_generation_evaluation.ipynb
│       └── rag_pipeline.py
│
└── README.md
```

---

## Technology Stack

- **Python**
- **Sentence Transformers**
- **FAISS**
- **BM25 / rank-bm25**
- **CrossEncoder reranking**
- **OpenAI API**
- **NumPy**
- **Markdown + YAML / PyYAML**
- **JSON**
- **Jupyter Notebook / Google Colab**
- **Git / GitHub**

### Why no LangChain?

The current pipeline is implemented directly with Python, Sentence Transformers, FAISS, and the OpenAI SDK. This keeps retrieval, context construction, prompting, and evaluation explicit and easy to inspect.

LangChain is not required for the current scope. It could be introduced later if the application needs more complex orchestration, reusable chains, agents, tool calling, or integrations, but adding it now would not improve the measured retrieval quality by itself.

---

## Running the Core Pipeline

Install the main dependencies used by `rag_pipeline.py`:

```bash
pip install sentence-transformers faiss-cpu openai numpy
```

Set the OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key"
```

Run:

```bash
python src/rag/rag_pipeline.py
```

The script loads `chunks.json`, creates the dense FAISS index, retrieves relevant policy sections, and generates a grounded answer with sources.

---

## Project Roadmap

| Stage | Status |
|---|---|
| Domain analysis | ✅ Completed |
| Synthetic knowledge base | ✅ Completed |
| Metadata design | ✅ Completed |
| Structure-aware chunking | ✅ Completed |
| 81-chunk dataset | ✅ Completed |
| Embedding model comparison | ✅ Completed |
| Dense retrieval | ✅ Completed |
| BM25 baseline | ✅ Completed |
| Hybrid retrieval / RRF experiments | ✅ Completed |
| CrossEncoder reranking experiment | ✅ Completed |
| Retrieval evaluation | ✅ Completed |
| End-to-end RAG generation | ✅ Completed |
| Generation evaluation | ✅ Completed |
| Reusable Python RAG pipeline | ✅ Completed |
| User interface | ⏳ Planned |
| Deployment | ⏳ Planned |
| Production hardening / automated tests | ⏳ Planned |

---

## Key Engineering Decisions

1. **Structure-aware chunks instead of arbitrary text windows** to preserve policy section meaning.
2. **Metadata propagation** to retain document identity, version, status, and section traceability.
3. **Evaluation-driven retriever selection** rather than assuming hybrid search or reranking must be better.
4. **Dense FAISS retrieval retained as the final baseline** because it produced the strongest Hit@5 and MRR@5 results.
5. **Grounded generation prompt** that restricts answers to retrieved documentation and requires source references.
6. **Retrieval and generation evaluated separately** so errors can be attributed to the correct pipeline stage.

---

## Next Steps

The core experimental RAG workflow is complete. The next useful engineering steps are:

- build a lightweight Streamlit interface;
- add a reproducible dependency file (`requirements.txt` or `pyproject.toml`);
- add automated tests for ingestion, retrieval, and source formatting;
- persist/reload embeddings or the FAISS index instead of rebuilding it on every startup;
- add configuration for models and retrieval parameters;
- package the pipeline for deployment;
- optionally add observability and experiment tracking for retrieval/generation quality.

---

## Project Focus

This project is not only an LLM API demo. Its main focus is the complete RAG workflow around realistic enterprise documentation:

**knowledge-base design → metadata → chunking → embedding experiments → retrieval evaluation → reranking experiments → grounded generation → generation evaluation.**

The main lesson from the experiments is that **more complex retrieval architecture is not automatically better**. For the current CertFlow corpus and evaluation set, the simpler dense FAISS retriever produced the strongest measured results.