import streamlit as st
import subprocess
import os
import json
from PIL import Image
import ollama

# Paths for saving and loading files
preprocessed_image_path = "/teamspace/studios/this_studio/Result/preprocessed_image.png"
json_file_path = "/teamspace/studios/this_studio/Result/invoice_data.json"

st.set_page_config(
    page_title="Invoice Processing and Query",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

def run_preprocessing(image_path):
    """Run the external preprocessing script."""
    try:
        result = subprocess.run(
            ['python3', '/teamspace/studios/this_studio/Main/preprocess.py', image_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        st.success(f"Image has been preprocessed and saved to {preprocessed_image_path}")
        st.text_area("Preprocessing Output", result.stdout.decode(), height=200)
    except subprocess.CalledProcessError as e:
        st.error(f"Preprocessing failed: {e.stderr.decode()}")

def run_analysis():
    """Run the external analysis script."""
    try:
        result = subprocess.run(
            ['python3', '/teamspace/studios/this_studio/Main/analysis_test.py'],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        st.success("Invoice data extracted and saved to JSON file.")
        st.text_area("Analysis Output", result.stdout.decode(), height=200)
    except subprocess.CalledProcessError as e:
        st.error(f"Analysis failed: {e.stderr.decode()}")

def load_invoice_data(file_path):
    """Load invoice data from JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def query_ollama(prompt, model, context=''):
    """Query the Ollama model."""
    try:
        response = ollama.generate(
            model=model,
            prompt=context + prompt
        )
        return response['response'].strip()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("Invoice Processing and Query")

    # Upload the image for preprocessing
    uploaded_image = st.file_uploader("Choose an invoice image for preprocessing", type=["png", "jpg", "jpeg"])
    
    if uploaded_image:
        # Save uploaded image to a temporary path
        temp_image_path = "/teamspace/studios/this_studio/help_comp/uploade.png"
        with open(temp_image_path, 'wb') as f:
            f.write(uploaded_image.read())
        
        # Show the uploaded image
        image = Image.open(temp_image_path)
        st.image(image, caption="Uploaded Invoice", use_column_width=True)

        # Preprocessing button
        if st.button("Preprocess Image"):
            run_preprocessing(temp_image_path)

    # Analysis button
    if st.button("Run Invoice Analysis"):
        if os.path.exists(preprocessed_image_path):
            st.image(preprocessed_image_path, caption="Preprocessed Image for Analysis", use_column_width=True)
            run_analysis()
        else:
            st.error(f"Preprocessed image not found at {preprocessed_image_path}. Please preprocess the image first.")

    # Query functionality
    if os.path.exists(json_file_path):
        st.subheader("LLM Query Assistant")
        
        # Load the invoice data
        data = load_invoice_data(json_file_path)

        # Prompt input
        prompt_text = st.text_area("Enter your query here (e.g., 'Fetch the email from the invoice data'):")
        models_info = ollama.list()
        available_models = tuple(model["name"] for model in models_info["models"])

        if available_models:
            selected_model = st.selectbox(
                "Select a model to process your query ↓", available_models
            )
        else:
            st.warning("No models available locally. Please ensure the models are installed.", icon="⚠️")
            return

        if st.button("Run Query"):
            if prompt_text:
                with st.spinner("Processing your query..."):
                    # Formulate the query to Ollama model
                    response = query_ollama(prompt_text, model=selected_model, context=json.dumps(data))

                    # Display the result
                    if response:
                        st.write("### Response:")
                        st.write(response)
                    else:
                        st.error("No response received.")
    else:
        st.warning(f"JSON file not found at {json_file_path}. Please run the analysis first.")

if __name__ == "__main__":
    main()
