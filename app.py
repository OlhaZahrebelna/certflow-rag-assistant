import hashlib
import hmac

import streamlit as st

from src.rag.rag_pipeline import CertFlowRAG


st.set_page_config(
    page_title="CertFlow RAG Assistant",
    page_icon="📚",
    layout="wide",
)


def get_secret(name: str) -> str | None:
    """Safely read a value from Streamlit secrets."""
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    return value


def get_rag(api_key: str) -> CertFlowRAG:
    """Keep one RAG instance per browser session and API key."""
    key_fingerprint = hashlib.sha256(api_key.encode()).hexdigest()

    if st.session_state.get("rag_key_fingerprint") != key_fingerprint:
        st.session_state["rag"] = CertFlowRAG(openai_api_key=api_key)
        st.session_state["rag_key_fingerprint"] = key_fingerprint

    return st.session_state["rag"]


st.title("CertFlow RAG Assistant")
st.caption(
    "Source-grounded Q&A over synthetic Account Data Certification documentation"
)

api_key = None
access_ready = False

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

    st.divider()
    st.subheader("Access")

    access_mode = st.radio(
        "Choose how to run the demo",
        ["Use my own API key", "Recruiter demo access"],
    )

    if access_mode == "Use my own API key":
        api_key = st.text_input(
            "OpenAI API key",
            type="password",
            placeholder="sk-...",
            help="Used only for requests made during your current app session.",
        )
        access_ready = bool(api_key)
        st.caption(
            "Your API key is not stored in this GitHub repository."
        )

    else:
        demo_password = st.text_input(
            "Demo password",
            type="password",
            help="Use the password shared with you by the project owner.",
        )

        configured_password = get_secret("DEMO_PASSWORD")
        owner_api_key = get_secret("OPENAI_API_KEY")

        if demo_password:
            if not configured_password or not owner_api_key:
                st.error("Recruiter demo access is not configured yet.")
            elif hmac.compare_digest(demo_password, configured_password):
                api_key = owner_api_key
                access_ready = True
                st.success("Demo access enabled.")
            else:
                st.error("Incorrect demo password.")

        st.caption(
            "Recruiter mode uses the project owner's API key after password verification."
        )

if not access_ready:
    if access_mode == "Use my own API key":
        st.info("Enter your OpenAI API key in the sidebar to enable the assistant.")
    else:
        st.info("Enter the recruiter demo password in the sidebar to enable the assistant.")

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
    disabled=not access_ready,
)

if ask_clicked:
    if not query.strip():
        st.warning("Enter a question first.")
    else:
        try:
            with st.spinner("Loading retrieval model and knowledge base..."):
                rag = get_rag(api_key)

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
