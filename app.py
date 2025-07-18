import streamlit as st
import spacy
import pdfplumber
import pandas as pd


#Load NLP Model
nlp = spacy.load("en_core_web_lg")
#try:
#    nlp = spacy.load("en_core_web_lg")
#except OSError:
#    os.system("python -m spacy download en_core_web_lg")
#    nlp = spacy.load("en_core_web_lg")

st.title("Legal Contract Anlyzer")
uploaded_file = st.file_uploader("Upload a contract (PDF)")

#File upload validation
if uploaded_file and not uploaded_file.name.endswith(".pdf"):
    st.error("Please upload a PDF file.")

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



#Results export (let users download extracted clauses as CSV):

results = {"Clause": ["Indemnity", "Governing Law"], "Text": ["...", "..."]}
st.download_button("Download CSV", pd.DataFrame(results).to_csv(), "contract_analysis.csv")

#Better UI (add a sidebar, progress bar, and logo):
#with st.sidebar:
#    st.image("C:\Users\SENYO\images.jpeg", width=100)
#    st.selectbox("Analysis Mode", ["Basic", "Advanced"])