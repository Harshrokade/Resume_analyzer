from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Properly implement CSS using st.markdown with unsafe_allow_html
def local_css():
    # Using triple quotes for multi-line string and proper indentation
    st.markdown("""
    <style>
        /* Main container styling */
        .main {
            background-color: #0e1117;
            color: white;
        }
        
        /* Header styling */
        .main-header {
            font-size: 2.5rem !important;
            color: #4c9aff !important;
            font-weight: 700 !important;
            margin-bottom: 1rem !important;
        }
        
        /* Sub-header styling */
        .sub-header {
            font-size: 1.5rem !important;
            color: #e0e0e0 !important;
            font-weight: 600 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 0.75rem !important;
        }
        
        /* Info box styling */
        .info-box {
            background-color: rgba(76, 154, 255, 0.1);
            border: 1px solid rgba(76, 154, 255, 0.2);
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
            color: #e0e0e0;
        }
        
        /* Card styling */
        .card {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Success text styling */
        .success-text {
            color: #4CAF50 !important;
            font-weight: 600 !important;
        }
        
        /* Warning text styling */
        .warning-text {
            color: #FFC107 !important;
            font-weight: 600 !important;
        }
        
        /* Override Streamlit's default button styling */
        .stButton > button {
            background-color: #4c9aff !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 5px !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: #3a75c4 !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Styling for text areas and inputs */
        .stTextArea > div > div > textarea {
            background-color: #1e2130 !important;
            color: #e0e0e0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .stFileUploader > div > button {
            background-color: #4c9aff !important;
            color: white !important;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            color: #666;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Make sure radio buttons are visible */
        .stRadio > div {
            background-color: transparent !important;
        }
        
        .stRadio > div > div > label {
            color: #e0e0e0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Configure page
st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply CSS
local_css()

# App header - using HTML with classes that match our CSS
st.markdown('<h1 class="main-header">ATS Resume Expert</h1>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
    <p>This tool helps you analyze how well your resume matches a job description using AI. Upload your resume and paste the job description to get started.</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<h2 class="sub-header">Job Description</h2>', unsafe_allow_html=True)
    input_text = st.text_area(
        "Paste the job description here:",
        height=300,
        key="input",
        help="Copy and paste the full job description from the job posting"
    )

with col2:
    st.markdown('<h2 class="sub-header">Your Resume</h2>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF format):",
        type=["pdf"],
        help="Make sure your resume is in PDF format"
    )
    
    if uploaded_file is not None:
        st.markdown('<p class="success-text">✅ Resume uploaded successfully!</p>', unsafe_allow_html=True)
        
        # Display PDF preview
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            uploaded_file.seek(0)  # Reset file pointer after reading
            
            pdf_preview = images[0].resize((400, int(400 * images[0].height / images[0].width)))
            st.image(pdf_preview, caption="Resume Preview", use_column_width=True)
        except Exception as e:
            st.error(f"Error previewing PDF: {e}")

# Analysis options
st.markdown('<h2 class="sub-header">Analysis Options</h2>', unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

analysis_type = st.radio(
    "Select analysis type:",
    ["Detailed Resume Review", "Match Percentage Analysis"],
    horizontal=True
)

analyze_button = st.button("Analyze Resume", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input prompts
input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
Structure your response with clear headings and bullet points for better readability.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. 

Please structure your response in the following format:
1. MATCH PERCENTAGE: Provide a clear percentage of how well the resume matches the job description
2. KEY MATCHES: List the key skills and qualifications that match the job requirements
3. MISSING KEYWORDS: List important keywords from the job description that are missing in the resume
4. RECOMMENDATIONS: Provide specific suggestions to improve the resume for this particular job
5. FINAL THOUGHTS: Give a brief overall assessment

Make your response visually organized with clear sections and bullet points.
"""

# Process and display results
if analyze_button:
    if not input_text.strip():
        st.warning("⚠️ Please enter a job description.")
    elif uploaded_file is None:
        st.warning("⚠️ Please upload your resume.")
    else:
        with st.spinner("Analyzing your resume... This may take a moment."):
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                
                if analysis_type == "Detailed Resume Review":
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                    prompt_used = "Detailed Resume Review"
                else:
                    response = get_gemini_response(input_prompt3, pdf_content, input_text)
                    prompt_used = "Match Percentage Analysis"
                
                # Display results
                st.markdown(f'<h2 class="sub-header">Results: {prompt_used}</h2>', unsafe_allow_html=True)
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add download option for the analysis
                result_text = f"# {prompt_used}\n\n{response}"
                st.download_button(
                    label="Download Analysis",
                    data=result_text,
                    file_name=f"resume_analysis_{analysis_type.lower().replace(' ', '_')}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")

# Footer
st.markdown('<div class="footer">', unsafe_allow_html=True)
st.markdown('ATS Resume Expert | Powered by Google Gemini AI', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)