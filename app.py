import streamlit as st
import google.generativeai as genai
import os
import json
import requests
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
import time

# Load environment variables from a .env file
load_dotenv()

# Configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Set up the model configuration for text generation
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Define safety settings for content generation
safety_settings = [
    {"category": f"HARM_CATEGORY_{category}", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]


def generate_response_from_gemini(input_text):
     # Create a GenerativeModel instance with 'gemini-pro' as the model type
    llm = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    )
    # Generate content based on the input text
    output = llm.generate_content(input_text)
    # Return the generated text
    return output.text

def extract_text_from_pdf_file(uploaded_file):
    # Use PdfReader to read the text content from a PDF file
    pdf_reader = pdf.PdfReader(uploaded_file)
    text_content = ""
    for page in pdf_reader.pages:
        text_content += str(page.extract_text())
    return text_content

def extract_text_from_docx_file(uploaded_file):
    # Use docx2txt to extract text from a DOCX file
    return docx2txt.process(uploaded_file)




# Prompt Template
input_prompt_template = """
As an experienced Applicant Tracking System (ATS) analyst, with profound knowledge in technology,
 software engineering, data analyst,data science,ML engineer,python engineer,AI engineer, full stack web development,
  cloud engineering, cloud development, DevOps engineering, and big data engineering, your role involves evaluating
   resume against job description. Recognizing the competitive job market, provide top-notch assistance for resume
   improvement. Your goal is to analyze each resume against the given job description, assign a percentage match
    based on key criteria, and pinpoint missing keywords and give matched keywords and any expereince
    mentioned in resume accurately.

resume:{text}
description:{job_description}
I want the response in one single string having the structure
{{"Job Description Match":"%", "Missing Keywords":"", "Matched Keywords": "", "Candidate Summary":"", "Experience":""}}

"""


# # Prompt Template
# input_prompt_template = """
# As an experienced Applicant Tracking System (ATS) analyst,
# with profound knowledge in technology, software engineering, data science, full stack web development, cloud enginner, 
# cloud developers, devops engineer and big data engineering, your role involves evaluating resumes against job descriptions.
# Recognizing the competitive job market, provide top-notch assistance for resume improvement.
# Your goal is to analyze the resume against the given job description, 
# assign a percentage match based on key criteria, and pinpoint missing keywords accurately.
# resume:{text}
# description:{job_description}
# I want the response in one single string having the structure
# {{"Job Description Match":"%","Missing Keywords":"","Candidate Summary":"","Experience":""}}
# """

# Streamlit app
# Initialize Streamlit app

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: 
        return None
    return r.json() 
lottie_checking = load_lottiefile("assests/checking.json")
# lottie_checking = load_lottiefile("assets/checking.json")
# lottie_notmatched = load_lottiefile("assests/notmatched.json")
# lottie_matched = load_lottiefile("assests/matched.json")

st.set_page_config(page_title="FitScore: Resume & Job Description Match Analyzer")
st.title("Analyze. Score. Optimize. 💡")
st.markdown('<style>h1{color: yellow; text-align: center; font-family:POPPINS}</style>', unsafe_allow_html=True)
# st.title("Analyze. Score. Optimize." + ":sunglasses:")
# st.markdown('<style>h1{color: orange; text-align: center; font-family:POPPINS}</style>', unsafe_allow_html=True)

st.text(" \n")
st.text(" \n")
st.text(" \n")
st.text("\n" * 3)

#  job description input
st.subheader("Input Your Job Description")
job_description_text = st.text_area("Paste Job Description Here", height=300)
job_description_file = st.file_uploader("Or Upload Job Description File", type=["pdf", "docx"], help="Upload a PDF or DOCX file for the job description")

# Extract text from job description file if uploaded
if job_description_file is not None:
    if job_description_file.type == "application/pdf":
        job_description_text = extract_text_from_pdf_file(job_description_file)
    elif job_description_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        job_description_text = extract_text_from_docx_file(job_description_file)
    st.markdown('<h8 style="color: lightgreen;text-align: center;">Job description file uploaded successfully!</h8>', unsafe_allow_html=True)
elif not job_description_text:
    st.markdown('<h8 style="color: red;text-align: center;">Please provide the job description text or upload a file!</h8>', unsafe_allow_html=True)



# job_description = st.text_area("Input Your Job Description",height=300)
uploaded_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"], help="Upload a PDF or DOCX file Only")

if uploaded_file is not None:
    st.markdown('<h8 style="color: lightgreen;text-align: center;">File uploaded successfully!</h8>', unsafe_allow_html=True)
else:
    st.markdown('<h8 style="color: red;text-align: center;">Please upload your Resume!</h8>', unsafe_allow_html=True)
    
    
st.text(" \n")
st.text(" \n")
st.text(" \n")   


# import streamlit as st

# # Center the Streamlit button
# st.markdown("""
#     <div style="display: flex; justify-content: center;">
#         <h3>Check Score</h3>
#     </div>
# """, unsafe_allow_html=True)

# # Define the Streamlit button
# if st.button("Check Score"):
#     # Action to perform when button is clicked
#     st.write("Button clicked!")
# Center the button
# st.markdown("<h3 style='text-align: center;'>Check Score</h3>", unsafe_allow_html=True)
# check_score_button = st.button("Check Score")
# # Single button for checking score
# st.subheader("Actions")
# check_score_button = st.button("Check Score")


# col1, col2, col3 = st.columns([4,4,2])
# with col1:
#     submit_button = st.button("Check ATS Result")
# with col2:
#     submit_button1 = st.button("Check Score")
# with col3:
#     submit_button2 = st.button("How it Works?")
    

# Function to extract information from AI-generated responses
def extract_info(responses):
    list_of_dict = []
    
    for response in responses:
        match_percentage_str = response.split('"Job Description Match":"')[1].split('"')[0]
        Missing_Keywords = response.split('"Missing Keywords":"')[1].split('"')[0]
        try:
            matched_keywords = response.split('"Matched Keywords":"')[1].split('"')[0]
        except IndexError:
            matched_keywords = None  # or handle the error accordingly

        # matched_keywords = response.split('"Matched Keywords":"')[1].split('"')[0]
        Candidate_Summary = response.split('"Candidate Summary":"')[1].split('"')[0]
        Experience = response.split('"Experience":"')[1].split('"')[0]
        
        list_of_dict.append({
            "Matched Keywords": matched_keywords,
            "Missing Keywords": Missing_Keywords,
            "Match Percentage": match_percentage_str,
            "Candidate Summary": Candidate_Summary,
            "Experience": Experience
        })
    
    return list_of_dict

# Function to display results in Streamlit
def display_results(results):
    for result in results:
        st.markdown('<h3 style="color: yellow;text-align: left;">Analysis Result</h3>', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;'><strong>Match Percentage:</strong> {result['Match Percentage']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;'><strong>Matched Keywords:</strong> {result['Matched Keywords']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;'><strong>Missing Keywords:</strong> {result['Missing Keywords']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;'><strong>Candidate Summary:</strong> {result['Candidate Summary']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;'><strong>Experience:</strong> {result['Experience']}</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line between results for better readability

# Process the resume and job description
# if submit_button or submit_button1:
# if check_score_button:
# Center the button using HTML and CSS
# st.markdown("""
#     <div style="display: flex; justify-content: center; margin-top: 20px;">
#         <button id="check_score_button" style="padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;" onclick="document.getElementById('check_score_button').click()">
#             Check Score
#         </button>
#     </div>
#     <style>
#         #check_score_button:active {
#             background-color: #45a049;
#         }
#     </style>
# """, unsafe_allow_html=True)

# Define the Streamlit button and its action
# if st.button("Check Score", key="check_score_button"):
if st.button("Check Score"):
    if uploaded_file is not None and job_description_text:
    # if uploaded_file is not None:
        st.lottie(
            lottie_checking,
            speed=1,
            loop=True,
            quality="low",
            height="200px",
            width="200px",
            key=None,
        )
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx_file(uploaded_file)

        # Use the new prompt template
        response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description_text))

        # Assume that the response is a list of JSON strings for multiple resumes
        responses = [response_text]  # Replace with actual list if multiple responses
        results = extract_info(responses)

        # Display the results in Streamlit
        display_results(results)
    else:
        st.text("\n" * 2)
        st.markdown('<h6 style="color: red;text-align: center;">Please upload your Resume!</h6>', unsafe_allow_html=True)

# elif submit_button2:
#     st.lottie(
#         lottie_checking,
#         speed=1,
#         loop=True,
#         quality="low",
#         height="200px",
#         width="200px",
#         key=None,
#     )

st.text("\n" * 20)

footer = """<style>
a:link, a:visited {
    color: yellow;
    background-color: transparent;
    text-decoration: underline;
}

a:hover, a:active {
    color: red;
    background-color: transparent;
    text-decoration: underline;
}

.footer {
    position: Bottom;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: transparent;
    color: white;
    text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤  <a style='display: block; text-align: center;' href="https://github.com/" target="_blank">Want to check </a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)











# if submit_button:   
    
#     if uploaded_file is not None:
#         st.text(" \n")
#         st.text(" \n")
#         st.text(" \n")  
#         st.lottie(
#             lottie_checking,
#             speed=1,
#             loop=True,
#             quality="low",
#             height="200px",
#             width="200px",
#             key=None,
#         )
#         if uploaded_file.type == "application/pdf":
#             resume_text = extract_text_from_pdf_file(uploaded_file)
#         elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             resume_text = extract_text_from_docx_file(uploaded_file)
#         response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

#         # Extract Job Description Match percentage from the response
#         match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0]

#         # Remove percentage symbol and convert to float
#         match_percentage = float(match_percentage_str.rstrip('%'))
        
#         #st.subheader("ATS Evaluation Result:")
#         st.markdown('<h3 style="color: yellow;text-align: left;">ATS Evaluation Result</h3>', unsafe_allow_html=True)
        

#         # Display message based on Job Description Match percentage
#         if match_percentage >= 80:
#             st.markdown('<p style="color: green;font-size: 20px;text-align: left;">Move forward with hiring</p>', unsafe_allow_html=True)
        
            
#         else:
#             st.markdown('<p style="color: lightgreen;font-size: 20px;text-align: left;">Profile Matched!</p>', unsafe_allow_html=True)
            
#         #st.write(response_text)
#     else:
#         st.text(" \n")
#         st.text(" \n")
#         st.markdown('<h6 style="color: red;text-align: center;">Please upload your Resume!</h6>', unsafe_allow_html=True)
    
# elif submit_button1:  
#     if uploaded_file is not None:
#         st.lottie(
#             lottie_checking,
#             speed=1,
#             loop=True,
#             quality="low",
#             height="200px",
#             width="200px",
#             key=None,
#         ) 
#         if uploaded_file.type == "application/pdf":
#             resume_text = extract_text_from_pdf_file(uploaded_file)
#         elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
#             resume_text = extract_text_from_docx_file(uploaded_file)
#         response_text = generate_response_from_gemini(input_prompt_template.format(text=resume_text, job_description=job_description))

#         # Extract Job Description Match percentage from the response
#         match_percentage_str = response_text.split('"Job Description Match":"')[1].split('"')[0] 
        
#         st.markdown('<h3 style="color: yellow; text-align: left;">Your ATS Score</h3>', unsafe_allow_html=True)
        
#         st.write(f"<div style='text-align:left; font-family: sans-serif; font-size: 20px;'>{match_percentage_str}</div>", unsafe_allow_html=True)
#     else:
#         st.text(" \n")
#         st.text(" \n")
#         st.markdown('<h6 style="color: red;text-align: center;">Please upload your Resume!</h6>', unsafe_allow_html=True)        
    
# elif submit_button2:
#     st.lottie(
#             lottie_checking,
#             speed=1,
#             loop=True,
#             quality="low",
#             height="200px",
#             width="200px",
#             key=None,
#         ) 
    
    
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")
# st.text(" \n")

# footer="""<style>
# a:link , a:visited{
# color: yellow;
# background-color: transparent;
# text-decoration: underline;
# }

# a:hover,  a:active {
# color: red;
# background-color: transparent;
# text-decoration: underline;
# }

# .footer {
# position: Bottom;
# left: 0;
# bottom: 0;
# width: 100%;
# background-color: transparent;
# color: white;
# text-align: center;
# }
# </style>
# <div class="footer">
# <p>Developed with ❤ by<a style='display: block; text-align: center;' href="https://github.com/Gitesh08" target="_blank">Gitesh Mahadik</a></p>
# </div>
# """
# st.markdown(footer,unsafe_allow_html=True)
