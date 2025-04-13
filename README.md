# 📝 ATS Resume Expert

**ATS Resume Expert** is a powerful web application that analyzes your resume against a given job description using **Google Gemini AI**. It provides both a **Detailed Resume Review** and a **Match Percentage Analysis** to help candidates improve their resumes and increase their chances of getting shortlisted by Applicant Tracking Systems (ATS).

## 🚀 Features

- 🧠 AI-powered resume analysis using Google Gemini
- 📄 Upload resume in PDF format
- 📋 Paste job descriptions for comparison
- ✅ Match percentage calculation
- 🔍 Key skills match and missing keyword identification
- 💡 Smart resume improvement suggestions
- 🎨 Beautiful dark-themed user interface with custom CSS
- 📥 Option to download the analysis report

## 🖼️ Screenshot

![screenshot](https://user-images.githubusercontent.com/your-username/your-screenshot.png)

## 📦 Requirements

Before running the app, ensure you have the following installed:

- Python 3.8 or above
- [Google API Key](https://makersuite.google.com/app/apikey)
- The following Python libraries:
  - `streamlit`
  - `python-dotenv`
  - `pdf2image`
  - `Pillow`
  - `google-generativeai`

Install dependencies using:

```bash
pip install -r requirements.txt

ats_resume_expert/
│
├── app.py                  # Main Streamlit app
├── .env                    # Contains API keys
├── requirements.txt        # Dependencies
└── README.md               # (Optional) Project overview

## 📦 TO run 
streamlit run app.py


