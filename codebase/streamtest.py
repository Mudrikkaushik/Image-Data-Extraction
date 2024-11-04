import streamlit as st
import pandas as pd
import os
st.title("Invoice Extractor")
st.write("A simple app for uploading, processing, and saving Image data files.")
SAVE_DIR = "./uploaded_files"
os.makedirs(SAVE_DIR, exist_ok=True)
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("File Uploaded Successfully!")
    st.write("File Preview:")
    st.dataframe(df.head())
    st.write("Columns in the uploaded file:")
    st.write(df.columns.tolist())
    file_path = os.path.join(SAVE_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File saved successfully at {file_path}")
st.write("---")
st.write("Mudrik Kaushik's App © 2024")
