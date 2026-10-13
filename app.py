import streamlit as st
from answer import ask


@st.cache_resource
def warm():
    from search import V
    return V.shape


with st.spinner("Loading the search index…"):
    warm()

st.title("CaseCrate")
st.caption("Legal information drawn from published judgments. "
           "Not legal advice.")

if "history" not in st.session_state:
    st.session_state.history = []

for q, a in st.session_state.history:
    st.chat_message("user").write(q)
    with st.chat_message("assistant"):
        st.write(a["answer"])
        for p in a["passages"]:
            with st.expander(f"{p['case_no']}  ·  {p['distance']:.2f}"):
                st.write(p["text"])

question = st.chat_input("Ask about these judgments")

if question:
    with st.spinner("Searching the judgments…"):
        result = ask(question)
    st.session_state.history.append((question, result))
    st.rerun()