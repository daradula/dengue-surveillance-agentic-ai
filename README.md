# 🦟 Dengue Surveillance Decision-Support System

Agentic AI system supporting district-level dengue surveillance decision-making 
in Sri Lanka, combining epidemiological and meteorological data reasoning with 
a RAG-based knowledge base of public health guidelines and research.

**🔗 Live Demo:** https://dengue-surveillance-agentic-ai-gzqbpqbumfqhtcbyg3wyrn.streamlit.app/

**📦 Repository:** https://github.com/daradula/dengue-surveillance-agentic-ai

---
## Project Description

District health officers currently assess dengue risk by manually reviewing 
weekly epidemiological bulletins and separate weather sources. This system 
automates that assessment — combining live weather data, epidemiological 
case data, and a RAG knowledge base of 20+ research/guideline documents — 
to generate district-level dengue risk reports.

---

## Architecture Diagram

User (District + Query)
│
▼
Synthesis Agent (Orchestrator)
├──▶ Data Agent (Tool-use): weather API + case data
└──▶ Knowledge Agent (RAG): vector store retrieval
│
▼
LLM Report Generation → Reflection/Self-check → Final Report → UI


**Patterns used:**
- **Tool-use** — Data Agent (`agents/data_agent.py`)
- **RAG/Retrieval** — Knowledge Agent (`agents/knowledge_agent.py`)
- **Orchestrator-worker** — Synthesis Agent (`agents/synthesis_agent.py`)
- **Reflection** — Synthesis Agent, Step 5 (`agents/synthesis_agent.py`)

---

## Agent-to-Agent Communication

Synthesis Agent calls Data Agent and Knowledge Agent directly, passing 
structured dict/JSON outputs between them:

Synthesis Agent → Data Agent.analyze_district(district)
→ {"district", "weather": {...}, "epidemiological": {...}}

Synthesis Agent → Knowledge Agent.retrieve(query, k=3)
→ [{"source": ..., "content": ...}, ...]

Both outputs → combined into LLM prompt → report → reflection → final report


---

## Setup Instructions

```bash
git clone https://github.com/daradula/dengue-surveillance-agentic-ai.git
cd dengue-surveillance-agentic-ai
pip install -r requirements.txt
# Add API keys to .env (see .env.example)
python rag/build_vectorstore.py
streamlit run streamlit_app.py
```

---

## Model Selection Strategy

| Sub-task | Model (Provider) | Why Chosen |
|---|---|---|
| Data/API testing | Llama 3.1 8B Instant (Groq) | Free, very low latency |
| Report synthesis + reflection | Nemotron 3 Ultra (OpenRouter, free) | Large context, strong reasoning for critical synthesis step |

---

## RAG Pipeline

- **Corpus:** 20+ documents (WHO/CDC guidelines, district-level dengue studies, forecasting research)
- **Chunking:** RecursiveCharacterTextSplitter, 500 chars, 50 overlap
- **Embedding model:** sentence-transformers/all-MiniLM-L6-v2
- **Vector store:** ChromaDB

### Retrieval Evaluation (5 Sample Queries)

| # | Query | Top Source Retrieved | Relevant? | Comment |
|---|---|---|---|---|
| 1 | What are the symptoms of severe dengue? | who_dengue_guidelines_2009.pdf | ✅ | Retrieved exact WHO presumptive diagnosis and warning-signs criteria |
| 2 | How does rainfall affect dengue transmission in Colombo? | Meteorological time-series.pdf | ✅ | Direct statistical association between rainfall and dengue incidence in Colombo |
| 3 | What vector control measures are recommended by WHO? | who_dengue_guidelines_2009.pdf | ✅ | Retrieved WHO's routine vector control operations (immature stage & adult control) |
| 4 | What is the relationship between ENSO and dengue outbreaks? | who_dengue_guidelines_2009.pdf | ⚠️ | Related to climate factors generally but not ENSO-specific; a more targeted ENSO document would improve this |
| 5 | How is dengue risk mapped spatially in Jaffna? | jaffna_spatial_risk_map.pdf | ✅ | Highly relevant — direct match with specific risk-area (Nallur MoH) detail |

---

## Known Limitations

- The Weekly Epidemiological Report's dense 25-column PDF table could not be reliably parsed by `pdfplumber`; a structured JSON reference was used instead.
- Retrieval occasionally surfaces near-duplicate chunks from similarly-named source documents.
- Query 4 (ENSO) shows the corpus would benefit from a dedicated ENSO/climate-index document for more targeted retrieval.