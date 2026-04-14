import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

llm = ChatGroq(
    api_key="GROQ_API_KEY",
    model_name="llama-3.3-70b-versatile"
)

# ── State ──────────────────────────────────────────────
class DocumentState(TypedDict):
    document_text: str
    document_type: Optional[str]
    risk_analysis: Optional[str]
    plain_explanation: Optional[str]
    action_items: Optional[str]
    language: str

# ── Agents ─────────────────────────────────────────────
def classifier_agent(state: DocumentState) -> DocumentState:
    response = llm.invoke([
        SystemMessage(content="You are a legal document classifier. Identify the type of Indian legal document."),
        HumanMessage(content=f"Classify this document in 1 line:\n{state['document_text'][:1000]}")
    ])
    state["document_type"] = response.content
    return state

def risk_analyzer_agent(state: DocumentState) -> DocumentState:
    response = llm.invoke([
        SystemMessage(content="""You are an Indian legal risk analyzer. 
        Find risky clauses, unfair terms, and red flags in the document.
        Format your response with clear sections and bullet points.
        Always mention relevant Indian laws if applicable."""),
        HumanMessage(content=f"Analyze risks in:\n{state['document_text'][:3000]}")
    ])
    state["risk_analysis"] = response.content
    return state

def explainer_agent(state: DocumentState) -> DocumentState:
    lang_instruction = "Explain in both Hindi and English" if state["language"] == "Hindi + English" else f"Explain in {state['language']}"
    response = llm.invoke([
        SystemMessage(content=f"""You are a legal document explainer for common Indians.
        {lang_instruction}. Use very simple words.
        Break down complex legal jargon into easy language."""),
        HumanMessage(content=f"Explain this document simply:\n{state['document_text'][:3000]}")
    ])
    state["plain_explanation"] = response.content
    return state

def action_advisor_agent(state: DocumentState) -> DocumentState:
    response = llm.invoke([
        SystemMessage(content="""You are a legal action advisor for Indians.
        Based on the document, suggest practical next steps.
        Always add disclaimer that this is not legal advice.
        Suggest when to consult a lawyer."""),
        HumanMessage(content=f"What should the person do after reading this?\n{state['document_text'][:2000]}\nRisks found: {state['risk_analysis']}")
    ])
    state["action_items"] = response.content
    return state

# ── Graph ───────────────────────────────────────────────
def build_graph():
    graph = StateGraph(DocumentState)
    graph.add_node("classifier", classifier_agent)
    graph.add_node("risk_analyzer", risk_analyzer_agent)
    graph.add_node("explainer", explainer_agent)
    graph.add_node("action_advisor", action_advisor_agent)
    graph.set_entry_point("classifier")
    graph.add_edge("classifier", "risk_analyzer")
    graph.add_edge("risk_analyzer", "explainer")
    graph.add_edge("explainer", "action_advisor")
    graph.add_edge("action_advisor", END)
    return graph.compile()

# ── UI ──────────────────────────────────────────────────
st.set_page_config(page_title="NyayaMitra", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f5f7fa; color: #1a1a2e; }
    .stMarkdown { color: #1a1a2e; }
    h1, h2, h3, p, label { color: #1a1a2e !important; }
    section[data-testid="stSidebar"] { background-color: #f8f8f8; }
    .stButton>button { background-color: #4a90d9; color: white; border-radius: 8px; font-weight: 600; }
    .stTabs [data-baseweb="tab"] { color: #1a1a2e; font-weight: 600; }
    .stFileUploader { background-color: #ffffff !important; border-radius: 10px; padding: 10px; border: 1px solid #ddd; }
    .stFileUploader label { color: #1a1a2e !important; }
    [data-testid="stFileUploaderDropzone"] { background-color: #ffffff !important; border: 2px dashed #1a1a2e !important; }
    [data-testid="stFileUploaderDropzone"] * { color: #1a1a2e !important; }
    .stSelectbox label { color: #1a1a2e !important; }
    .stSelectbox div { background-color: #ffffff !important; color: #1a1a2e !important; }
    [data-testid="stTab"] { background-color: #ffffff; border-radius: 8px; padding: 10px; }
    .stSuccess { background-color: #e8f5e9 !important; color: #1a1a2e !important; }
    .stSpinner { color: #1a1a2e !important; }
    .stFileUploader * { color: #1a1a2e !important; }
    [data-testid="stFileUploaderDropzone"] span { color: #1a1a2e !important; background-color: #ffffff !important; }
    .stSelectbox [data-baseweb="select"] { background-color: #ffffff !important; }
    .stSelectbox [data-baseweb="select"] * { color: #1a1a2e !important; }
    div[data-baseweb="select"] > div { background-color: #ffffff !important; color: #1a1a2e !important; border: 1px solid #1a1a2e !important; }
    textarea, input { background-color: #ffffff !important; color: #1a1a2e !important; border: 1px solid #1a1a2e !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align:center; color:#1a1a2e;'>⚖️ NyayaMitra</h1>
    <p style='text-align:center; color:#555;'>Your AI-powered Indian Legal Document Analyzer</p>
    <hr style='border: 1px solid #ddd;'>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📁 Upload Document")
    uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
    language = st.selectbox("🌐 Explanation Language", ["English", "Hindi", "Hindi + English"])
    analyze_btn = st.button("🔍 Analyze Document", use_container_width=True)

    st.markdown("""
        <div style='background:#f0f0f0; padding:15px; border-radius:10px; margin-top:20px; color:#333;'>
        <b>⚠️ Disclaimer</b><br>
        <small>NyayaMitra is for educational purposes only. 
        Always consult a qualified lawyer before taking legal action.</small>
        </div>
    """, unsafe_allow_html=True)

with col2:
    if analyze_btn and uploaded_file:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            text = " ".join([page.extract_text() for page in reader.pages])
        else:
            text = uploaded_file.read().decode("utf-8")

        if not text.strip():
            st.error("Could not extract text from document.")
        else:
            with st.spinner("🤖 Multi-agent pipeline running..."):
                graph = build_graph()
                result = graph.invoke({
                    "document_text": text,
                    "document_type": None,
                    "risk_analysis": None,
                    "plain_explanation": None,
                    "action_items": None,
                    "language": language
                })

            st.success("✅ Analysis Complete!")

            tab1, tab2, tab3, tab4 = st.tabs(["📋 Document Type", "🚨 Risk Analysis", "💬 Plain Explanation", "✅ Action Items"])

            with tab1:
                st.markdown(result["document_type"])
            with tab2:
                st.markdown(result["risk_analysis"])
            with tab3:
                st.markdown(result["plain_explanation"])
            with tab4:
                st.markdown(result["action_items"])

    elif analyze_btn and not uploaded_file:
        st.warning("Please upload a document first!")
    else:
        st.markdown("""
            <div style='text-align:center; padding:80px; color:#888;'>
            <h3 style='color:#1a1a2e;'>⚖️ Upload a legal document to get started</h3>
            <p>Supports rent agreements, FIRs, contracts, affidavits & more</p>
            </div>
        """, unsafe_allow_html=True)