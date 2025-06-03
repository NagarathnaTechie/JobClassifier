**Job Classifier**

**Overview**

Job Classifier is a Streamlit-based web application designed to streamline job searching by analyzing user resumes and providing personalized job recommendations. Leveraging natural language processing (NLP) and Firebase authentication, the app extracts key information from PDF resumes, matches skills and experience to job roles, and delivers tailored job suggestions. The intuitive dark-themed interface ensures a seamless user experience, from authentication to job discovery.

**Features**

Firebase Authentication
Secure User Management: Integrated with Firebase Authentication for robust signup and login functionality.
REST API Integration: Utilizes Firebase's Identity Toolkit API for seamless email/password authentication.
Session Management: Maintains user sessions using Streamlit's session_state, ensuring secure navigation across pages (authentication, resume upload, review, and results).
Secrets Management: Stores Firebase configuration securely in Streamlit secrets, protecting sensitive API keys.

**Core Functionalities**

Resume Parsing:
* Extracts key details (name, skills, education, work experience) from PDF resumes using PyPDF2 and spaCy with the en_core_web_sm model.
* Allows users to review and edit extracted data for accuracy.
Job Recommendations:
* Matches resume data against a predefined dataset (Job_Roles.csv) using a recommendation algorithm.
* Displays top job matches with match percentages and predicted job categories.
* Features interactive job cards with hover effects and color-coded match indicators (green for ≥80%, yellow for ≥60%, red for <60%).
User Interface:
Dark-themed, responsive design with custom CSS for enhanced aesthetics (gradient buttons, cards, progress bars).
Multi-page navigation (authentication, upload, review, results) with a collapsible sidebar.



Error handling for invalid inputs, failed uploads, or processing errors.



File Handling:





Temporarily stores uploaded PDFs using tempfile for processing, ensuring data security by deleting files after use.

Technical Stack





Frontend: Streamlit (1.29.0) for UI, enhanced with custom CSS.



Backend:





Python libraries: PyPDF2 (3.0.1), spaCy (3.7.5), pandas (2.0.3), numpy (1.26.4).



Firebase Admin SDK (6.2.0) for authentication.



Deployment: Streamlit Community Cloud with Python 3.11.



Data Processing: Uses Job_Roles.csv for job matching (assumed to contain job titles, required skills, and descriptions).
