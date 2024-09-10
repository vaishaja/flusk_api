set PYTHONPATH=C:\GenAI\Git Repo\model_interface
import streamlit as st
from gyan_interface import evaluate_code

# Set page config for better aesthetics
st.set_page_config(
    page_title="Code Quality Evaluator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Add the logo
st.image("code_harbour_logo.png", width=200)  # Local file path
# Streamlit app title with emoji
st.markdown("<h3 style='text-align: center;'>📝 Code Quality Evaluator</h3>", unsafe_allow_html=True)


# Instructions with Markdown for better formatting
st.markdown("""
    <style>
    .instructions {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    </style>
    <div class="instructions">
        **Instructions:**
        1. Upload a code file (e.g., .py, .java, .js, .c) to evaluate its quality.
        2. The system will analyze the code and provide feedback based on various quality metrics.
    </div>
""", unsafe_allow_html=True)

# File uploader with a file drop zone style
st.markdown("""
    <style>
    .file-upload {
        background-color: #f1f1f1;
        padding: 20px;
        border-radius: 5px;
        border: 1px dashed #ccc;
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose a file", type=["py", "java", "js", "c"], label_visibility="collapsed")

if uploaded_file is not None:
    # Read the file content
    file_content = uploaded_file.read().decode("utf-8")

    # Display the uploaded file name with a nice heading
    st.markdown(f"**Uploaded file:** `{uploaded_file.name}`")

    # Placeholder for spinner while evaluating
    with st.spinner("Evaluating code..."):
        # Evaluate the code by calling the function in helper.py
        response_text = evaluate_code(file_content)

    # Display the response in a code block for better readability
    st.subheader("Review Evaluation Report..:")
    #st.code(response_text, language="python")
    st.markdown(response_text['Result'])
else:
    st.info("Please upload a file to get started.")

# Footer with custom style
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f9f9f9;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #ddd;
    }
    </style>
    <div class="footer">
        Developed by [Your Name]
    </div>
""", unsafe_allow_html=True)
