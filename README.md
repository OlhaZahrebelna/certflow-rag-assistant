# CertFlow RAG Assistant

**CertFlow RAG Assistant** is an end-to-end Retrieval-Augmented Generation (RAG) application for answering questions about synthetic enterprise **Account Data Certification** documentation.

The system retrieves relevant policy sections, builds grounded context, sends that context to an OpenAI model, and returns an answer with source references. It is designed as an analyst decision-support tool and does **not** make certification decisions autonomously.

## Live Demo

**Streamlit app:** https://certflow-rag-assistant.streamlit.app

The deployed application supports two access modes:

- **Use your own OpenAI API key (BYOK)** — users can provide their own key in the sidebar.
- **Recruiter demo access** — password-protected access that uses the project owner's API key stored securely in Streamlit Secrets.

> Demo credentials are not stored in the repository. A recruiter/demo password can be shared separately when needed.

---

## Project Status

The core RAG workflow, evaluation, user interface, dependency setup, and cloud deployment are complete.

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
| Streamlit interface | ✅ Completed |
| `requirements.txt` | ✅ Completed |
| Streamlit Cloud deployment | ✅ Completed |
| Production hardening / automated tests | ⏳ Planned |

---

## Business Problem

Enterprise data-governance teams often work with policies, validation rules, evidence requirements, source hierarchies, exception procedures, change-management rules, and escalation guidance distributed across multiple documents.

Manually locating the correct rule can be slow and can lead to inconsistent interpretation. CertFlow demonstrates how a RAG system can make policy information easier to retrieve while preserving **document and section traceability**.

Example questions:

- What evidence is required before an account can be certified?
- Which source should be used when systems contain conflicting information?
- When should a certification case be escalated?
- How should potential duplicate accounts be handled?
- What rules apply when an account legal name changes?

---

## Architecture

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
Top-5 policy sections
        ↓
Context construction
        ↓
OpenAI Responses API
        ↓
Grounded answer + source references
        ↓
Streamlit UI
```

The project also evaluates alternative retrieval strategies including **BGE embeddings, BM25, Reciprocal Rank Fusion (RRF), weighted RRF, and CrossEncoder reranking**. The final retrieval strategy was selected using measured retrieval performance rather than architecture complexity.

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

Synthetic documentation is used to reproduce a realistic enterprise RAG use case without exposing confidential company information.

---

## Metadata and Chunking

Each Markdown document contains YAML metadata such as:

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

The ingestion workflow preserves document structure rather than using arbitrary fixed-length windows. Markdown sections are converted into section-level chunks and document metadata is propagated to each chunk.

The chunking notebook also uses `RecursiveCharacterTextSplitter` from `langchain-text-splitters` where additional splitting is needed. LangChain is **not** used as the orchestration framework for the RAG pipeline.

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

The reranker reduced retrieval coverage and ranking quality by sometimes promoting broadly related passages over more specific policy sections. It was therefore **not selected** for the final pipeline.

### Final retrieval choice

```text
multi-qa-MiniLM-L6-cos-v1
        ↓
normalized embeddings
        ↓
FAISS IndexFlatIP
        ↓
Top-5 dense retrieval
```

This simpler architecture achieved the strongest measured retrieval results on the current evaluation set.

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
Top-5 chunks
     ↓
build_context()
     ↓
OpenAI Responses API
     ↓
Grounded answer
     ↓
Document + section sources
```

The implementation uses:

- `SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")`
- normalized dense embeddings
- `faiss.IndexFlatIP`
- default `top_k=5`
- controlled prompting that restricts the answer to retrieved context
- an explicit fallback when available documentation is insufficient
- source references using document and section metadata

---

## Generation Evaluation

Generation quality is evaluated separately from retrieval quality in:

```text
src/rag/02_generation_evaluation.ipynb
```

The evaluation measures four dimensions on a 0–2 scale:

- correctness
- faithfulness
- relevance
- source grounding

Average results:

| Metric | Score |
|---|---:|
| Correctness | **1.80 / 2.00** |
| Faithfulness | **1.95 / 2.00** |
| Relevance | **1.95 / 2.00** |
| Source grounding | **1.85 / 2.00** |

**14 of 20 answers (70%) achieved perfect scores across all four criteria.**

The strongest dimensions were faithfulness and relevance, indicating that the generation layer generally stays within the retrieved evidence.

---

## Live Testing Findings

Testing the deployed application revealed an important distinction between **generation quality** and **retrieval coverage**.

For several questions, the LLM generated a faithful answer from the supplied context, but the most specific policy section was not present in the Top-5 retrieved chunks.

Examples:

- **Escalation query:** the retriever returned general certification and FAQ sections but missed the authoritative `Quality Review, Exceptions, and Escalations → Escalation levels` section.
- **Legal-name change query:** the core legal-name rule was retrieved correctly, but the Top-5 did not include the downstream `Synchronization and closure` section or the full audit-record requirements.

This means the main remaining quality opportunity is **retrieval specificity and multi-section coverage**, not simply using a larger or more complex LLM.

Possible next experiments include:

- retrieving a larger candidate pool (for example Top-10) and selecting the final context afterward;
- metadata-aware retrieval using titles, section names, tags, and document type;
- query expansion for multi-part questions;
- policy-aware routing to authoritative documents;
- evaluation-set expansion using the newly discovered failure cases.

---

## Streamlit Application

The UI is implemented in:

```text
app.py
```

The application provides:

- example policy questions;
- free-text user questions;
- generated answers;
- cited source sections;
- expandable Top-5 retrieved chunks;
- similarity scores for retrieved chunks;
- two access modes.

### Access modes

**1. BYOK — Bring Your Own Key**

A user can enter their own OpenAI API key in the Streamlit sidebar. The key is used for that app session and is not stored in the GitHub repository.

**2. Recruiter demo access**

A recruiter can enter a demo password. After password verification, the app uses the project owner's API key from Streamlit Secrets.

The following secrets are configured only in Streamlit Cloud and are intentionally excluded from GitHub:

```toml
OPENAI_API_KEY = "..."
DEMO_PASSWORD = "..."
```

`.gitignore` excludes local `.env` and `.streamlit/secrets.toml` files.

---

## Repository Structure

```text
certflow-rag-assistant/
│
├── app.py                              # Streamlit application
├── requirements.txt                    # Python dependencies
├── .gitignore                          # Secrets/local files excluded
│
├── data/
│   └── raw/
│       ├── pdf/                        # 10 PDF documents
│       ├── source_markdown/            # 10 Markdown documents
│       └── processed/
│           └── chunks.json             # 81 structured chunks
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
- **Streamlit**
- **Sentence Transformers**
- **FAISS**
- **BM25 / rank-bm25**
- **CrossEncoder**
- **OpenAI API**
- **NumPy**
- **PyYAML**
- **langchain-text-splitters**
- **JSON / Markdown / YAML**
- **Jupyter Notebook / Google Colab**
- **Git / GitHub**
- **Streamlit Community Cloud**

### Why not use LangChain for the full RAG pipeline?

The main RAG pipeline is implemented directly with Python, Sentence Transformers, FAISS, and the OpenAI SDK. This keeps retrieval, context construction, prompting, and evaluation explicit and easy to inspect.

`langchain-text-splitters` is used as a focused ingestion utility, but the full LangChain orchestration framework is not required for the current architecture. It could be introduced later for more complex chains, agents, tool calling, or integrations.

---

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The public BYOK mode does not require a local environment variable because a user can enter an API key directly in the UI.

For local recruiter-demo mode, create:

```text
.streamlit/secrets.toml
```

with:

```toml
OPENAI_API_KEY = "your_openai_api_key"
DEMO_PASSWORD = "your_demo_password"
```

Do not commit this file.

---

## Key Engineering Decisions

1. **Structure-aware chunking** instead of arbitrary text windows to preserve policy meaning.
2. **Metadata propagation** for document identity, version, status, and section traceability.
3. **Evaluation-driven retriever selection** instead of assuming hybrid search or reranking must be better.
4. **Dense FAISS retrieval retained as the final baseline** because it achieved the strongest Hit@5 and MRR@5 results.
5. **Grounded generation** restricted to retrieved documentation.
6. **Retrieval and generation evaluated separately** so failures can be attributed to the correct pipeline stage.
7. **BYOK + password-protected demo access** to provide a public portfolio experience without exposing API credentials.
8. **Live failure cases retained as evaluation signals** instead of hiding known retrieval limitations.

---

## Next Steps

The application is deployed and usable. The most valuable next engineering work is now focused on quality and production hardening:

- improve retrieval specificity for multi-part and policy-owner questions;
- expand the retrieval evaluation set with live failure cases;
- test larger candidate retrieval pools and metadata-aware retrieval;
- persist/reload embeddings or the FAISS index instead of rebuilding on startup;
- add automated tests for ingestion, retrieval, access logic, and source formatting;
- add structured configuration for models and retrieval parameters;
- optionally add observability and experiment tracking.

---

## Project Focus

CertFlow is not only an LLM API demo. It demonstrates the complete RAG workflow around realistic enterprise documentation:

**knowledge-base design → metadata → chunking → embedding experiments → retrieval evaluation → hybrid/reranking experiments → grounded generation → generation evaluation → Streamlit application → cloud deployment.**

A key lesson from the project is that **more complex retrieval architecture is not automatically better**. The dense FAISS baseline performed best in the original evaluation, while live testing also showed where further retrieval improvements are needed for more specific, multi-section questions.
