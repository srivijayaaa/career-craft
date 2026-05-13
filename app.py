from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import PyPDF2
from PIL import Image


# PAGE CONFIG

st.set_page_config(
    page_title="Resume ATS Tracker",
    layout="wide"
)


# CUSTOM CSS

st.markdown(
"""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #e7f8f1, #f5f7ff);
    color: #1f1f1f;
    font-family: 'Arial', sans-serif;
}

/* HEADINGS */
h1 {
    color: #0f3d3e !important;
    font-weight: 800;
    letter-spacing: 0.5px;
}

h2, h3 {
    color: #145a43 !important;
    font-weight: 700;
}

/* TEXT */
p, div {
    color: #2b2b2b !important;
    line-height: 1.6;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(135deg, #1f7a5c, #2bb673);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
    border: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    transition: 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(135deg, #145a43, #1f7a5c);
}

/* TEXT AREA */
.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid #cfe8df;
    background-color: #ffffff;
}

/* FILE UPLOADER */
.stFileUploader {
    background-color: white;
    padding: 10px;
    border-radius: 12px;
    border: 1px dashed #1f7a5c;
}

/* SUCCESS BOX */
.stSuccess {
    background-color: #d1f5e0 !important;
    border-radius: 10px;
}

/* WARNING BOX */
.stWarning {
    background-color: #fff3cd !important;
    border-radius: 10px;
}

/* SPACING IMPROVEMENT */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

</style>
""",
unsafe_allow_html=True
)


# LOAD ENV VARIABLES

load_dotenv()


# GEMINI CONFIGURATION

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MODEL
model = genai.GenerativeModel("gemini-1.5-pro")


# GEMINI RESPONSE FUNCTION

def get_gemini_response(input_text):
    try:
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        return f"Error: {e}"


# PDF TEXT EXTRACTION

def input_pdf_text(uploaded_file):

    text = ""

    try:
        reader = PyPDF2.PdfReader(uploaded_file)

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text

    except Exception as e:
        return f"Error reading PDF: {e}"

    return text


# ATS PROMPT

input_prompt = """
You are an ATS Resume Analyzer.

Compare the resume with the job description.

Resume:
{text}

Job Description:
{jd}

Provide:
1. ATS Match Percentage
2. Missing Keywords
3. Profile Summary
"""


# HEADER SECTION

col1, col2 = st.columns([3, 2])

with col1:

    st.title("CareerCraft")

    st.header("Navigate the Job Market with Confidence!")

    st.markdown(
        """
        <p style='text-align: justify;'>

        CareerCraft is an ATS-Optimized Resume Analyzer designed to help
        job seekers improve their resumes and increase their chances of
        getting shortlisted.

        The platform compares resumes with job descriptions using AI-powered
        analysis and provides:
        <br><br>
        ✔ ATS Match Percentage<br>
        ✔ Missing Keywords<br>
        ✔ Resume Insights<br>
        ✔ Profile Summary

        </p>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.image(
        "https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif",
        use_container_width=True
    )

st.space(3)


# FEATURES SECTION

col1, col2 = st.columns([3, 2])

with col2:

    st.header("Wide Range of Offerings")

    st.write("✔️ ATS Resume Analysis")
    st.write("✔️ Resume Optimization")
    st.write("✔️ Missing Keyword Detection")
    st.write("✔️ Career Guidance")
    st.write("✔️ AI-Powered Suggestions")
    st.write("✔️ Personalized Insights")

with col1:

    try:
        img1 = Image.open("images/career image 1.png")
        #img1 = Image.open(r"C:\Users\SHANMUKH\OneDrive\Desktop\ATS RESUME CHECKER\images\images\career image 1.png")
        #st.image(img1, use_container_width=True)
        st.image(img1, width=750)

    except:
        st.warning("Image 1 not found.")

st.space(3)


# MAIN SECTION

col1, col2 = st.columns([3, 2])

with col1:

    st.markdown(
        "<h1 style='text-align: center;'>Embark on Your Career Adventure</h1>",
        unsafe_allow_html=True
    )

    jd = st.text_area(
        "📄 Paste the Job Description",
        height=200
    )

    uploaded_file = st.file_uploader(
        "📎 Upload Your Resume (PDF only)",
        type=["pdf"]
    )

    submit = st.button("🔍 Analyze Resume")

    if submit:

        if uploaded_file is not None and jd:

            with st.spinner("Analyzing Resume..."):

                resume_text = input_pdf_text(uploaded_file)

                prompt = input_prompt.format(
                    text=resume_text,
                    jd=jd
                )

                response = get_gemini_response(prompt)

                st.success("Analysis Complete!")

                st.markdown(response)

        else:

            st.warning(
                "⚠️ Please upload a resume and enter a job description."
            )

with col2:

    try:
        img2 = Image.open("images/career image 2.png")
        #img2 = Image.open(r"C:\Users\SHANMUKH\OneDrive\Desktop\ATS RESUME CHECKER\images\images\career image 2.png")
        st.image(img2, use_container_width=True)

    except:
        st.warning("Image 2 not found.")

st.space(3)


# FAQ SECTION

col1, col2 = st.columns([2, 3])

with col2:

    st.markdown(
        "<h1 style='text-align: center;'>❓ FAQ</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "**Q: How does CareerCraft analyze resumes and job descriptions?**"
    )

    st.write(
        "A: CareerCraft uses AI-powered analysis to compare resumes "
        "with job descriptions and identify matching skills and keywords."
    )

    st.space(1)

    st.write(
        "**Q: Can CareerCraft suggest resume improvements?**"
    )

    st.write(
        "A: Yes. It identifies missing keywords and provides suggestions "
        "to improve ATS compatibility."
    )

    st.space(1)

    st.write(
        "**Q: Is it suitable for freshers and experienced professionals?**"
    )

    st.write(
        "A: Absolutely! It provides useful insights for all career levels."
    )

with col1:

    try:
        img3 = Image.open("images/career image 3 - Copy.png")
        #img3 = Image.open(r"C:\Users\SHANMUKH\OneDrive\Desktop\ATS RESUME CHECKER\images\images\career image 3 - Copy.png")
        st.image(img3, use_container_width=True)

    except:
        st.warning("Image 3 not found.")