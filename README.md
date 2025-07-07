Resume Parsing System with NLP
==============================

Overview:
---------
This is a simple resume parsing and ranking system built using Python, NLP (SpaCy), and Streamlit. 
It allows you to upload a ZIP file containing multiple resumes in PDF or DOCX format, parses each 
resume, compares it against the required skill set for a selected job role, and ranks the resumes 
based on how closely they match the desired skills.

Features:
---------
- Upload multiple resumes at once (in a ZIP file)
- Extracts text from PDF and DOCX files
- Uses NLP to preprocess text (lemmatization, stopword removal)
- Compares resumes against role-specific skill sets
- Calculates a match score based on matched skills and cosine similarity
- Displays ranked resumes
- Download results as a CSV file

Supported Roles:
----------------
- Software Developer
- Data Scientist
- Web Developer
- AI Engineer
- Product Manager

How to Use:
-----------
1. Run the app using the Streamlit command:
   streamlit run app.py

2. Select a job role from the dropdown.

3. Upload a ZIP file containing resumes in `.pdf` or `.docx` format.

4. The app will parse and analyze each resume and rank them based on match score.

5. You can download the ranked result as a CSV file.

Requirements:
-------------
See the `requirements.txt` file for all dependencies.

Notes:
------
- The resumes should not be inside subfolders in the ZIP file.
- Only PDF and DOCX formats are supported.
- SpaCy’s English model (`en_core_web_sm`) must be downloaded before running the app.

License:
--------
This project is licensed under the MIT License. See LICENSE file for details.

Author:
-------
Velagala Sanjeev Reddy
