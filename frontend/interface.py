import os
import sys

import streamlit as st

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from app.rag import answer_question, format_source  # noqa: E402

st.title("📘 Research RAG ChatBot")

question = st.text_input("What would you like to know about your documents?")

if question:
    answer, sources = answer_question(question)

    st.subheader("Answer:")
    st.write(answer)
    if answer=="I couldn't find information about that in the documents you provided.":
        st.write("No relevant documents were used.")
    else:
        st.subheader("Sources:")
        if not sources:
            st.write("No relevant documents were used.")
        else:
            seen_titles = set()
            for doc in sources:
                title = format_source(doc)
                if title in seen_titles:
                    continue  # skip duplicates
                seen_titles.add(title)
                st.write("-", title)

