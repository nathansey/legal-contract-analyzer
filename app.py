import streamlit as st
import spacy
import pdfplumber


#Load NLP Model
nlp = spacy.load("en_core_web_lg")

st.title("Legal Contract Anlyzer")
uploaded_file = st.file_uploader("Upload a contract (PDF)")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)

        doc = nlp(text)

    st.subheader("Key Entities")
    st.table({"Text": [ent.text for ent in doc.ents], 
              "Type": [ent.label_ for ent in doc.ents]})
    
    st.subheader("Important Clauses")
    for sent in doc.sents:
        if any(keyword in sent.text.lower() for keyword in ["indemnity","governing law", "liability"]):
            st.write(f" - {sent.text.strip()}")

