# Multi-Lingual Invoice Extraction App

This Streamlit app allows users to upload an invoice image and ask questions about it. The app leverages Google Gemini, a Large Language Model (LLM), to generate answers based on the content of the invoice. The app is useful for extracting multilingual insights from invoice images through preprocessing and analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Upload an invoice image in JPG, JPEG, or PNG format.
- Ask questions related to the invoice's contents.
- Uses Google Gemini LLM to provide responses.
- Suitable for multilingual invoice processing and analysis.

## Installation

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer)

### Steps

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/yourrepositoryname.git
    ```

2. Navigate to the project directory:

    ```bash
    cd yourrepositoryname
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

This will install the necessary libraries:
- `python-dotenv` for environment variable management.
- `streamlit` for building the user interface.
- `pillow` for image handling.
- `google-generativeai` for integration with Google Gemini.

## Configuration

### Setting Up Your API Key

1. Create a `.env` file in the root directory.
2. Add your Google Gemini API key:

    ```plaintext
    API_KEY=your_google_gemini_api_key
    ```

Replace `your_google_gemini_api_key` with your actual API key.

## Usage

1. Start the Streamlit app:

    ```bash
    streamlit run app.py
    ```

    Replace `app.py` with the name of your script if it differs.

2. Open the URL shown in your terminal (usually `http://localhost:8501`) in your web browser.

3. **Interacting with the App**:
   - **Ask a Question**: Type a question related to the invoice in the **Ask something here** text box.
   - **Upload an Image**: Click on **Upload an Image..** to upload an invoice image.
   - **Generate Output**: Press **Output** to receive an AI-generated response based on the uploaded invoice.

## Troubleshooting

- **No API Key Found**: Make sure your `.env` file is correctly set up with a valid Google Gemini API key.
- **Image Not Uploaded Error**: Ensure an image file is uploaded before pressing the **Output** button.
- **Installation Issues**: If library installation fails, try updating pip:

    ```bash
    pip install --upgrade pip
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy using the Multi-Lingual Invoice Extraction App! For any issues, please raise an issue in the repository or contact us.
