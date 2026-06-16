import streamlit as st
import requests

st.set_page_config(
    page_title="CGPSC Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API base URL (change if running on different port)
API_BASE = "http://localhost:8000/api"

st.title("🎯 CGPSC Intelligence Engine")
st.caption("Advanced RAG • Analytics • Smart Mocks • AI Tutor | Local & Private")

# Sidebar
with st.sidebar:
    st.header("Settings")
    persona = st.selectbox(
        "AI Tutor Persona",
        options=["mentor", "socratic", "examiner", "storyteller"],
        index=0,
        help="Choose your preferred teaching style",
    )
    model = st.selectbox(
        "LLM Model",
        ["llama3.1:8b", "qwen2.5:7b", "llama3.2:3b"],
        index=0,
    )
    k = st.slider("Number of sources to retrieve", 3, 10, 6)

    st.divider()
    st.caption("Make sure Ollama + FastAPI backend are running.")

# Main Tabs
tab_chat, tab_analytics, tab_mock, tab_explorer = st.tabs(
    ["🗨️ AI Tutor Chat", "📊 Analytics Dashboard", "📋 Generate Mock Paper", "🔍 PYQ Explorer"]
)

# ===================== CHAT TAB =====================
with tab_chat:
    st.subheader("Chat with your AI Tutor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("sources"):
                with st.expander("Sources"):
                    for src in message["sources"]:
                        st.caption(f"[{src['id']}] {src['year']} | {src['subject']} | Relevance: {src['relevance']}")

    if prompt := st.chat_input("Ask anything about CGPSC..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/chat",
                        json={
                            "query": prompt,
                            "persona": persona,
                            "k": k,
                            "model": model,
                        },
                        timeout=120,
                    )
                    data = resp.json()
                    answer = data.get("answer", "Sorry, something went wrong.")
                    sources = data.get("sources", [])

                    st.markdown(answer)

                    if sources:
                        with st.expander("📚 Sources from PYQs"):
                            for src in sources:
                                st.caption(f"[{src['id']}] {src['year']} | {src['subject']} | Relevance: {src.get('relevance', 0)}")

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# ===================== ANALYTICS TAB =====================
with tab_analytics:
    st.subheader("PYQ Analytics & Intelligence")

    if st.button("Compute / Refresh Analytics", type="primary"):
        with st.spinner("Analyzing your question bank..."):
            try:
                # For demo, we send empty. In real use, send your questions list
                resp = requests.post(f"{API_BASE}/analytics/compute", json={"questions": []}, timeout=30)
                data = resp.json()

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Questions", data.get("total_questions", 0))

                with st.expander("Subject Distribution"):
                    st.json(data.get("subject_distribution", {}))

                with st.expander("Top Priority Topics"):
                    st.json(data.get("priority_rankings", [])[:10])

                with st.expander("Topics Not Appeared Recently (Overdue)"):
                    st.json(data.get("top_overdue_topics", []))

            except Exception as e:
                st.error(str(e))

    st.info("Upload your normalized PYQ JSON in the future to get real analytics.")

# ===================== MOCK GENERATOR TAB =====================
with tab_mock:
    st.subheader("Smart Mock Paper Generator")

    col1, col2 = st.columns(2)
    with col1:
        count = st.number_input("Number of Questions", 20, 200, 100, step=10)
        subjects = st.text_input("Subjects (comma separated)", "Geography, History")
    with col2:
        year_from = st.number_input("Year From", 2015, 2025, 2018)
        year_to = st.number_input("Year To", 2018, 2025, 2025)

    if st.button("Generate Mock Paper", type="primary"):
        with st.spinner("Generating high-quality mock..."):
            try:
                resp = requests.post(
                    f"{API_BASE}/mock/generate",
                    json={
                        "count": count,
                        "subjects": [s.strip() for s in subjects.split(",")],
                        "year_from": year_from,
                        "year_to": year_to,
                    },
                )
                st.success("Mock generated successfully!")
                st.json(resp.json())
            except Exception as e:
                st.error(str(e))

# ===================== EXPLORER TAB =====================
with tab_explorer:
    st.subheader("PYQ Explorer")
    st.info("Coming soon: Search and browse your full PYQ database with filters.")

st.divider()
st.caption("CGPSC Intelligence v0.2 | Built with ❤️ for serious aspirants | Runs 100% locally")