import os

import streamlit as st

from src.rag.rag_pipeline import CertFlowRAG


st.set_page_config(
    page_title="CertFlow RAG Assistant",
    page_icon="📚",
    layout="wide",
)


@st.cache_resource(show_spinner="Loading retrieval model and knowledge base...")
def load_rag(api_key: str) -> CertFlowRAG:
    """Initialize the RAG pipeline once per Streamlit session/cache."""
    return CertFlowRAG(openai_api_key=api_key)


def get_api_key() -> str | None:
    """Read the OpenAI API key from Streamlit secrets or environment."""
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        secret_key = None

    return secret_key or os.getenv("OPENAI_API_KEY")


st.title("CertFlow RAG Assistant")
st.caption(
    "Source-grounded Q&A over synthetic Account Data Certification documentation"
)

with st.sidebar:
    st.header("About")
    st.write(
        "CertFlow retrieves relevant policy sections from a synthetic enterprise "
        "knowledge base and generates an answer using only the retrieved context."
    )
    st.markdown(
        "**Retrieval:** `multi-qa-MiniLM-L6-cos-v1` + FAISS  \n"
        "**Knowledge base:** 10 documents / 81 chunks  \n"
        "**Default retrieval:** Top 5 chunks"
    )
    st.info(
        "This assistant supports analysts. It does not make final certification decisions."
    )

api_key = get_api_key()

if not api_key:
    st.warning(
        "OPENAI_API_KEY is not configured. Add it to your environment or Streamlit secrets to run the assistant."
    )

example_questions = [
    "What evidence is required before an account can be certified?",
    "When should a certification case be escalated?",
    "How should potential duplicate accounts be handled?",
    "What rules apply when the legal name of an account is updated?",
]

selected_example = st.selectbox(
    "Example questions",
    ["Choose an example..."] + example_questions,
)

query = st.text_area(
    "Ask a question about Account Data Certification",
    value="" if selected_example == "Choose an example..." else selected_example,
    height=110,
    placeholder="Example: What evidence is required before an account can be certified?",
)

ask_clicked = st.button(
    "Ask CertFlow",
    type="primary",
    disabled=not bool(api_key),
)

if ask_clicked:
    if not query.strip():
        st.warning("Enter a question first.")
    else:
        try:
            rag = load_rag(api_key)

            with st.spinner("Retrieving relevant policy sections and generating an answer..."):
                result = rag.generate_answer(query.strip())

            st.subheader("Answer")
            st.markdown(result["answer"])

            st.subheader("Retrieved sources")
            st.caption(
                "These are the policy sections retrieved before answer generation."
            )

            for chunk in result["retrieved_chunks"]:
                label = (
                    f"#{chunk['rank']} · {chunk['document']} · "
                    f"{chunk['section']} · score {chunk['score']:.3f}"
                )

                with st.expander(label):
                    st.write(chunk["content"])

        except Exception as exc:
            st.error("The assistant could not complete the request.")
            st.exception(exc)

st.divider()
st.caption(
    "Portfolio project demonstrating knowledge-base design, structure-aware chunking, "
    "retrieval evaluation, FAISS dense search, grounded generation, and RAG evaluation."
)
