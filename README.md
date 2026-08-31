# CertFlow RAG Assistant

A **Retrieval-Augmented Generation (RAG) knowledge assistant** designed to help analysts quickly find and interpret internal Account Data Certification policies, validation rules, evidence requirements, exception procedures, and escalation guidance.

The project simulates a realistic enterprise knowledge-management use case where operational rules are distributed across multiple documents and need to be retrieved accurately with their original context and metadata.

> 🚧 **Project status: In active development**
> Knowledge-base design, document preparation, metadata structure, and document chunking are completed. Retrieval, generation, and evaluation layers are the next stages.

---

## 🎯 Business Problem

In enterprise data-governance workflows, analysts may need to work with multiple policy documents covering:

* account certification;
* data validation rules;
* source hierarchy;
* evidence requirements;
* duplicate prevention;
* change management;
* quality review;
* exceptions and escalations.

Finding the correct rule manually can be slow and may lead to inconsistent interpretation.

The goal of **CertFlow RAG Assistant** is to provide a source-grounded interface where analysts can ask natural-language questions and retrieve the most relevant internal guidance.

Example questions:

* Which source should be used when two systems contain conflicting account information?
* What evidence is required before an account can be certified?
* When should a case be escalated?
* How should potential duplicate accounts be handled?
* Which validation rules apply to a specific account field?
* What changed between different policy versions?

The assistant is designed to **support analysts rather than make final certification decisions**.

---

## 🧠 Planned RAG Architecture

```text
Internal Documentation
        │
        ▼
Document Loading
        │
        ▼
Metadata Extraction
        │
        ▼
Structure-aware Chunking
        │
        ▼
Embeddings
        │
        ▼
Vector / Hybrid Retrieval
        │
        ▼
Relevant Context
        │
        ▼
LLM
        │
        ▼
Grounded Answer + Sources
```

A key design objective is to preserve metadata throughout the pipeline so retrieval can eventually consider not only semantic similarity but also document attributes such as version, status, document type, and effective date.

---

# ✅ Current Progress

## 1. Domain & Knowledge Base Design — Completed

The business domain and assistant boundaries were defined before implementing retrieval.

The project models an internal enterprise documentation environment with:

* structured policies;
* operational procedures;
* validation guidance;
* governance rules;
* escalation scenarios;
* document versioning;
* metadata-driven retrieval requirements.

The assistant is intentionally designed as a **decision-support system**, not an autonomous decision maker.

---

## 2. Synthetic Enterprise Knowledge Base — Completed

A realistic synthetic documentation set has been created specifically for the project.

The current knowledge base contains **10 documents**:

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

Documents are stored in both:

```text
data/raw/source_markdown/
data/raw/pdf/
```

Using synthetic documentation makes it possible to reproduce realistic enterprise RAG challenges without exposing confidential company information.

---

## 3. Document Metadata — Completed

Each Markdown document contains structured YAML metadata.

Example:

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
tags:
  - account_certification
  - master_data
  - data_quality
```

Metadata is preserved during ingestion and attached to individual chunks.

This structure is intended to support future:

* metadata filtering;
* version-aware retrieval;
* document traceability;
* source attribution;
* policy prioritization.

---

## 4. Structure-Aware Document Chunking — Completed

Instead of splitting documents only by a fixed number of characters or tokens, the current pipeline uses the semantic structure of the Markdown documents.

Documents are split using `##` section headings.

For example:

```text
Document
 ├── Purpose
 ├── Systems and ownership
 ├── Certification scope
 ├── Certification outcomes
 ├── Business principles
 ├── Certification validity
 └── Service targets
```

Each resulting chunk contains:

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

This approach keeps logically related policy information together while preserving document and section context.

---

## 5. Chunk Dataset — Completed

The ingestion pipeline currently produces:

**10 documents → 76 structured chunks**

The processed chunks are serialized to JSON and can be reused by the retrieval pipeline without repeatedly preprocessing the source documents.

Current pipeline:

```text
Markdown documents
        ↓
YAML metadata parsing
        ↓
Markdown section detection
        ↓
Section-level chunk generation
        ↓
Metadata propagation
        ↓
76 structured chunks
        ↓
chunks.json
```

---

# 🔨 Next Development Stages

## 6. Embeddings & Vector Store — Planned

The next stage will transform chunks into dense vector representations using a sentence embedding model.

Planned workflow:

```text
Chunks
   ↓
Embedding Model
   ↓
Vector Representations
   ↓
Vector Store
```

The goal is to enable semantic retrieval where queries do not need to contain the exact wording used in policy documents.

---

## 7. Retrieval — Planned

The project will initially establish a semantic-search baseline and then evaluate more advanced retrieval strategies.

Planned experiments include:

* dense vector search;
* lexical/BM25 retrieval;
* metadata filtering;
* hybrid retrieval;
* result fusion;
* reranking.

A possible advanced pipeline is:

```text
Query
 ├── Dense Retrieval
 └── BM25 Retrieval
         ↓
    Result Fusion
         ↓
      Reranker
         ↓
     Top Context
```

The final retrieval strategy will be selected based on evaluation results rather than architecture complexity alone.

---

## 8. RAG Generation — Planned

Retrieved chunks will be passed to an LLM together with a controlled system prompt.

The generation layer will be designed to:

* answer only from retrieved documentation;
* identify insufficient evidence;
* avoid unsupported policy claims;
* preserve source traceability;
* return references to supporting documents.

Conceptually:

```text
User Question
      ↓
Retriever
      ↓
Relevant Chunks
      ↓
Prompt + Context
      ↓
LLM
      ↓
Grounded Answer
```

---

## 9. RAG Evaluation — Planned

Evaluation will be implemented as a dedicated project stage rather than relying only on manual testing.

A test set of representative business questions will be created to evaluate both **retrieval** and **answer generation**.

Planned retrieval metrics may include:

* Recall@K;
* Precision@K;
* MRR;
* Hit Rate.

Generation quality will be evaluated for dimensions such as:

* answer correctness;
* faithfulness to retrieved context;
* relevance;
* source grounding.

LLM-based evaluation may also be compared with manually labelled expected answers.

---

## 10. User Interface — Planned

A lightweight interface is planned to demonstrate the complete system.

The application should allow a user to:

1. enter a certification-related question;
2. retrieve relevant documentation;
3. receive a grounded answer;
4. inspect the source documents/sections used to generate it.

A future interface may be implemented using **Streamlit**, with the RAG pipeline separated from the UI layer.

---

# 📁 Current Repository Structure

```text
certflow-rag-assistant/
│
├── data/
│   └── raw/
│       ├── pdf/
│       │   ├── 01_account_certification_overview.pdf
│       │   ├── ...
│       │   └── 10_policy_change_log.pdf
│       │
│       ├── source_markdown/
│       │   ├── 01_account_certification_overview.md
│       │   ├── ...
│       │   └── 10_policy_change_log.md
│       │
│       └── processed/
│           └── chunks.json
│
├── notebooks/
│   └── 01_domain_knowledge_base_design.ipynb
│
├── src/
│   └── ingestion/
│       └── chunker.ipynb
│
└── README.md
```

The structure will expand as retrieval, evaluation, application, and configuration components are added.

---

# 🛠️ Technology

### Currently used

* **Python**
* **Markdown**
* **YAML / PyYAML**
* **JSON**
* **Regular Expressions**
* **Jupyter Notebook / Google Colab**
* **Git / GitHub**

### Planned

* Sentence Transformers / embedding models
* Vector database
* BM25
* Hybrid Search
* Reranking
* LLM integration
* RAG evaluation
* Streamlit

---

# 🗺️ Project Roadmap

| Stage                              | Status      |
| ---------------------------------- | ----------- |
| Domain analysis                    | ✅ Completed |
| Knowledge-base design              | ✅ Completed |
| Synthetic enterprise documentation | ✅ Completed |
| Document metadata                  | ✅ Completed |
| Document ingestion                 | ✅ Completed |
| Structure-aware chunking           | ✅ Completed |
| Chunk serialization                | ✅ Completed |
| Embedding generation               | ⏳ Next      |
| Vector search                      | ⏳ Planned   |
| Hybrid retrieval                   | ⏳ Planned   |
| Reranking                          | ⏳ Planned   |
| RAG generation                     | ⏳ Planned   |
| Evaluation framework               | ⏳ Planned   |
| User interface                     | ⏳ Planned   |
| Deployment                         | ⏳ Planned   |

---

# 💡 Key Project Focus

This project is not intended only as a demonstration of calling an LLM API.

The main focus is on building the complete **RAG pipeline around realistic enterprise documentation**, including:

* knowledge-base design;
* document structure;
* metadata;
* chunking strategy;
* retrieval quality;
* version-aware information retrieval;
* grounded generation;
* measurable evaluation.

The architecture will be developed incrementally, with retrieval and generation strategies selected based on experiments and evaluation results.

---

## Project Status

🚧 **Active development**

Current milestone:

```text
Knowledge Base
      ✅
Metadata
      ✅
Chunking
      ✅
76 Chunks
      ✅
       ↓
Embeddings   ← NEXT
       ↓
Retrieval
       ↓
Reranking
       ↓
LLM
       ↓
Evaluation
       ↓
Application
```
