import streamlit as st
import time


st.set_page_config(
    page_title="RAG Demo",
    layout="wide"
)

st.title("RAG Demo")


# Mock KB

documents = [
    {
        "title": "Refund Policy",
        "content": """
Customers may request a refund within 30 days of purchase.

Refunds are not allowed after 30 days unless the product
is defective.

Premium members may request store credit after 30 days.
"""
    },

    {
        "title": "Shipping Policy",
        "content": """
Standard shipping takes 3-5 business days.

Express shipping takes 1-2 business days.
"""
    },

    {
        "title": "Store Hours",
        "content": """
Monday-Friday: 9 AM - 8 PM

Saturday-Sunday: 10 AM - 6 PM
"""
    }
]

# Retrieval

def retrieve(question):

    question_lower = question.lower()

    if "refund" in question_lower:
        return documents[0]

    elif "shipping" in question_lower:
        return documents[1]

    elif "hour" in question_lower or "open" in question_lower:
        return documents[2]

    else:
        return None

# Without RAG

def ask_without_rag(question):

    question_lower = question.lower()

    if "refund" in question_lower:

        return """
Refund policies vary by company.

Many companies allow refunds within 60-90 days,
depending on the condition of the product.

Please contact customer support for details.
"""

    elif "shipping" in question_lower:

        return """
Shipping usually takes a few business days,
depending on the shipping method selected.
"""

    elif "open" in question_lower:

        return """
Most stores operate during standard business hours, i.e. 9 AM - 5 PM.
"""

    else:

        return """
I am not sure, but customer support may be able to help.
"""

# With RAG

def ask_with_rag(question):

    retrieved_doc = retrieve(question)

    if retrieved_doc is None:

        return (
            "I could not find relevant company information.",
            "No document retrieved."
        )

    question_lower = question.lower()

    if "refund" in question_lower:

        answer = """
According to our refund policy:

Customers may request a refund within 30 days of purchase.

Refunds after 30 days are only allowed if the product is defective.

Premium members may request store credit after 30 days.
"""

    elif "shipping" in question_lower:

        answer = """
According to our shipping policy:

Standard shipping takes 3-5 business days.

Express shipping takes 1-2 business days.
"""

    elif "open" in question_lower:

        answer = """
Our opening hours are as follows:

Monday-Friday: 9 AM - 8 PM

Saturday-Sunday: 10 AM - 6 PM
"""

    else:

        answer = "I could not answer using company information."

    return answer, retrieved_doc["content"]

# Session State

if "no_rag_answer" not in st.session_state:
    st.session_state.no_rag_answer = None

if "rag_answer" not in st.session_state:
    st.session_state.rag_answer = None

if "retrieved_context" not in st.session_state:
    st.session_state.retrieved_context = None

if "show_retrieved" not in st.session_state:
    st.session_state.show_retrieved = False

if "show_all_knowledge" not in st.session_state:
    st.session_state.show_all_knowledge = False

# User Input

question = st.text_input(
    "Ask a customer-service question",
    value="Can I get a refund after using the product for 3 months?"
)

st.divider()

# COL

col1, col2 = st.columns(2)

# W/O RAG COL

with col1:

    st.subheader("WITHOUT RAG")

    if st.button("Get Response (W/O RAG)"):

        with st.spinner("Thinking..."):

            time.sleep(1.5)

            st.session_state.no_rag_answer = ask_without_rag(question)

    if st.session_state.no_rag_answer:

        st.info(st.session_state.no_rag_answer)

# W/ RAG

with col2:

    st.subheader("WITH RAG")

    if st.button("Get Response (W/ RAG)"):

        with st.spinner("Thinking..."):

            time.sleep(1.5)

            answer, context = ask_with_rag(question)

            st.session_state.rag_answer = answer
            st.session_state.retrieved_context = context

    if st.session_state.rag_answer:

        st.success(st.session_state.rag_answer)

# KB

st.divider()

col3, col4 = st.columns(2)

# RETRIEVED KNOWLEDGE

with col3:

    if st.button("Show Retrieved Knowledge"):

        st.session_state.show_retrieved = True

# ENTIRE KB

with col4:

    if st.button("Show Entire Knowledge Base"):

        st.session_state.show_all_knowledge = True

# RK DISPLAY

if st.session_state.show_retrieved:

    st.divider()

    st.subheader("Retrieved Knowledge")

    if st.session_state.retrieved_context:

        with st.spinner("Opening retrieved document..."):

            time.sleep(1)

        st.code(st.session_state.retrieved_context)

    else:

        st.warning("No knowledge retrieved yet.")

# KB DISPLAY

if st.session_state.show_all_knowledge:

    st.divider()

    st.subheader("Entire Enterprise Knowledge Base")

    with st.spinner("Loading enterprise knowledge base..."):

        time.sleep(1)

    for doc in documents:

        st.markdown(f"### {doc['title']}")

        st.code(doc["content"])