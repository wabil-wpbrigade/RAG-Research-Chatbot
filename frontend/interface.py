import sys, os
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from app.rag import answer_question, format_source
import streamlit as st

st.title("📘 Research RAG ChatBot")

question = st.text_input("What would you like to know about your documents?")

if question:
    answer, sources = answer_question(question)

    st.subheader("Answer:")
    st.write(answer)

    st.subheader("Sources:")
    if not sources:
        st.write("No relevant documents were used.")
    else:
        seen = set()
        for doc in sources:
            md = getattr(doc, "metadata", {}) or {}
            key = (md.get("source"), md.get("page"))

            if key in seen:
                continue  # skip duplicates
            seen.add(key)

            st.write("-", format_source(doc))

