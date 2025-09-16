import streamlit as st
from pdfextractor import text_extractor
import google.generativeai as genai
import os

# Configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

resume_text = job_desc = None

# Upload resume
st.sidebar.title(':blue[UPLOAD YOUR RESUME (PDF Only)]')
file = st.sidebar.file_uploader('Resume',type=['pdf'])
if file:
    resume_text = text_extractor(file)

# Lest define the main page
st.title(':orange[SKILLMATCH] : :blue[AI Assisted Skill Matching Tool]')
st.markdown('##### This application will match your resume and the job description. It will create a detailed report on the match.')
tips = '''Follow these steps to proceed:
* Upload your resume in sidebar (PDF Only)
* Copy and paste the job description below for which you are applying
* Click the button and see the magic.'''
st.write(tips)

job_desc = st.text_area('Copy and paste Job Description here (press ctrl+enter to run)',max_chars=10000)

prompt = f'''Assume you are an expert in skill matching and creating profiles.
Match the following resume with the job description provided by the user
resume = {resume_text}
job description = {job_desc}

Your output should be as follows:
* Give a brief description of the applicant in 3 to 5 lines.
* Give a range expeceted ATS score along with the matching and non matching keywords.
* Give the chances of getting shotlisted for this position in percentage.
* Perform SWOT analysis and discuss each and everything in bullet points.
* Suggest what all imporvements can be made in resume in order get better ATS and increase percentage of getting shortlisted.
* Also create two customised resumes as per the job description provided to get better ATS and increase percentage of getting shortlisted.
* Above resumes must be of one page and in such a format that can be copied and pasted in word and converted to PDF.
* Use bullet points and tables where ever required.'''

if job_desc:
    if resume_text:
        response = model.generate_content(prompt)
        st.write(response.text)
    else:
        st.write('Please upload resume')