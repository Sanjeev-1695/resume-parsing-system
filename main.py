import streamlit as st
import zipfile
import io
import os
import csv
from pdfminer.high_level import extract_text
from docx import Document
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define skill sets for different roles
roles_skills = {
    "Software Developer": ["Python", "JavaScript", "SQL", "Machine Learning", "Data Structures", "Algorithms"],
    "Data Scientist": ["Python", "R", "SQL", "Machine Learning", "Data Analysis", "Statistics", "Deep Learning"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "SQL", "API Development"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "Neural Networks", "TensorFlow", "PyTorch"],
    "Product Manager": ["Product Management", "Agile", "Roadmap", "Stakeholder Management", "User Research"],
}

# Set up Streamlit page title
st.title("Resume Parsing System with NLP")

# Dropdown for selecting the role
role = st.selectbox("Select Role", options=list(roles_skills.keys()))

# Display the selected role
st.write(f"Selected Role: {role}")

# Get the required skills for the selected role
required_skills = roles_skills[role]

# Upload a zip file containing multiple resumes
uploaded_file = st.file_uploader("Upload a Zip File containing Resumes", type=["zip"])

if uploaded_file is not None:
    # Extract the zip file
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        zip_ref.extractall("/tmp/resumes")

    # Get the list of resume files in the zip
    resume_files = [f for f in os.listdir("/tmp/resumes") if f.endswith(('.pdf', '.docx'))]

    st.write(f"Extracted {len(resume_files)} resumes from the zip file.")

    # Initialize a list to store match scores and file names
    resume_match_scores = []

    # Parse and process each resume in the zip file
    for resume_file in resume_files:
        file_path = os.path.join("/tmp/resumes", resume_file)

        # Extract text based on the file type
        if resume_file.endswith(".pdf"):
            text = extract_text(file_path)
        elif resume_file.endswith(".docx"):
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])

        # Text preprocessing: Lemmatization, stop word removal, and case normalization
        def preprocess_text(text):
            doc = nlp(text)
            # Lemmatize and remove stopwords, but keep important terms like skills
            return " ".join([token.lemma_.lower() for token in doc if not token.is_stop and len(token.text) > 2])

        processed_text = preprocess_text(text)

        # Function to match skills using Cosine Similarity
        def match_skills_with_cosine_similarity(text, required_skills):
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text] + required_skills)
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            return cosine_sim[0]

        cosine_similarities = match_skills_with_cosine_similarity(processed_text, required_skills)

        # Normalize the skills in the required skills set
        normalized_required_skills = [skill.lower() for skill in required_skills]

        # Match skills, considering lowercase and synonyms
        matched_skills = []
        for i, skill in enumerate(normalized_required_skills):
            # Check if the skill in resume text contains the required skill as a whole word
            if re.search(r'\b' + re.escape(skill) + r'\b', processed_text.lower()):
                matched_skills.append(required_skills[i])

        # Calculate match score for this resume
        def calculate_match_score(matched_skills, required_skills):
            return (len(matched_skills) / len(required_skills)) * 100

        match_score = calculate_match_score(matched_skills, required_skills)

        # Store the resume file name and match score
        resume_match_scores.append((resume_file, match_score))

    # Rank resumes based on match score in descending order
    ranked_resumes = sorted(resume_match_scores, key=lambda x: x[1], reverse=True)

    # Display the ranked resumes with their match scores
    st.write("Ranked Resumes Based on Match Score:")
    for rank, (resume, score) in enumerate(ranked_resumes, 1):
        st.write(f"Rank {rank}: {resume} - Match Score: {score:.2f}%")

    # Prepare data for download
    result_data = [["Rank", "Resume Name", "Match Score"]]
    for rank, (resume, score) in enumerate(ranked_resumes, 1):
        result_data.append([rank, resume, f"{score:.2f}%"])

    # Convert result data into CSV format
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(result_data)
    output.seek(0)

    # Provide download button for the result file
    st.download_button(
        label="Download Ranked Resumes as CSV",
        data=output.getvalue(),
        file_name="ranked_resumes.csv",
        mime="text/csv"
    )
