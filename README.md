# ⚖️ NyayaMitra — AI-Powered Indian Legal Document Analyzer

🚀 **Live Demo:** https://nyayamitra-pfn7si7kprwdascnkt373t.streamlit.app/

> Your intelligent legal companion — upload any Indian legal document and instantly understand it in plain language.

---

## 🌟 What is NyayaMitra?

Most Indians struggle to understand complex legal documents like rent agreements, FIRs, and contracts. NyayaMitra solves this using a **multi-agent AI pipeline** built with LangChain + LangGraph that analyzes, explains, and advises — all in seconds.

---

## 🤖 Multi-Agent Architecture

NyayaMitra uses a **4-agent LangGraph pipeline:**

| Agent | Role |
|-------|------|
| 🔍 Classifier Agent | Identifies the type of legal document |
| 🚨 Risk Analyzer Agent | Flags risky clauses & unfair terms with Indian law references |
| 💬 Explainer Agent | Explains document in simple Hindi / English / Both |
| ✅ Action Advisor Agent | Suggests practical next steps |

---

## ✨ Features

- 📄 Upload PDF or TXT legal documents
- 🔍 Auto-identifies document type
- 🚨 Flags risky and unfair clauses with relevant Indian laws
- 💬 Plain language explanation in Hindi, English, or both
- ✅ Actionable next steps
- 🌐 Supports rent agreements, FIRs, contracts, affidavits & more

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Multi-Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| AI Model | Groq API — LLaMA 3.3 70B |
| UI | Streamlit |
| PDF Parsing | PyPDF2 |
| Environment | Python 3.12 |

---

## 🚀 Run Locally

```bash
git clone https://github.com/Nirvigna21/NyayaMitra.git
cd NyayaMitra
pip install -r requirements.txt
```

Create a `.env` file:
Run:
```bash
streamlit run app.py
```

---

## ⚠️ Disclaimer

NyayaMitra is for **educational purposes only**. Always consult a qualified lawyer before taking any legal action.

---

Made with ❤️ by **Nirvigna**
