# 📝Job Classifier

🚀 **Live Demo**: [Click here to try the app](https://jobclassifier-24.streamlit.app/)


# Overview

Job Classifier is a Streamlit-based web application designed to streamline job searching by analyzing user resumes and providing personalized job recommendations. Leveraging natural language processing (NLP) and Firebase authentication, the app extracts key information from PDF resumes, matches skills and experience to job roles, and delivers tailored job suggestions. The intuitive dark-themed interface ensures a seamless user experience, from authentication to job discovery.



# Features

**Firebase Authentication**
**Secure User Management:** Integrated with Firebase Authentication for robust signup and login functionality.

**REST API Integration:** Utilizes Firebase's Identity Toolkit API for seamless email/password authentication.

**Session Management**: Maintains user sessions using Streamlit's session_state, ensuring secure navigation across pages (authentication, resume upload, review, and results).

**Secrets Management:** Stores Firebase configuration securely in Streamlit secrets, protecting sensitive API keys.

# Core Functionalities

**Resume Parsing:**
* Extracts key details (name, skills, education, work experience) from PDF resumes using PyPDF2 and spaCy with the en_core_web_sm model.
* Allows users to review and edit extracted data for accuracy.
  
**Job Recommendations:**
* Matches resume data against a predefined dataset (Job_Roles.csv) using a recommendation algorithm.
* Displays top job matches with match percentages and predicted job categories.

**User Interface:**
* Dark-themed, responsive design with custom CSS for enhanced aesthetics (gradient buttons, cards, progress bars).
* Multi-page navigation (authentication, upload, review, results) with a collapsible sidebar.

# Technical Stack


**Frontend**: Streamlit (1.29.0) for UI, enhanced with custom CSS.


**Python libraries**: PyPDF2 (3.0.1), spaCy (3.7.5), pandas (2.0.3), numpy (1.26.4).



**Firebase Admin SDK** (6.2.0) for authentication.



**Deployment**: Streamlit Community Cloud with Python 3.11.



**Data Processing:** Uses Job_Roles.csv for job matching (assumed to contain job titles, required skills, and descriptions).

# Here are some of snapshot of Job Classifier website

![WhatsApp Image 2025-06-07 at 11 38 17_edc28984](https://github.com/user-attachments/assets/45e4f71f-6d23-4b00-ad1d-d1c1bb431578)

![WhatsApp Image 2025-06-07 at 11 39 10_f30c48fb](https://github.com/user-attachments/assets/e8d67493-627f-4bcb-86ab-8b68c1e5e8a1)

![WhatsApp Image 2025-06-07 at 11 39 46_70c954db](https://github.com/user-attachments/assets/12b22d07-b5de-4316-8c27-e29ccaa5722f)

![WhatsApp Image 2025-06-07 at 11 40 09_ab22cd43](https://github.com/user-attachments/assets/990146d0-05da-4d05-8ffb-9e6fe3301b0a)

![WhatsApp Image 2025-06-07 at 11 40 37_c8020815](https://github.com/user-attachments/assets/cdbc1ddb-66dd-42b0-97d6-e6a218c4e546)

![WhatsApp Image 2025-06-07 at 11 37 13_bf50a3dc](https://github.com/user-attachments/assets/d939fde0-1d8b-4c7e-8f57-16559000cdcb)

![WhatsApp Image 2025-06-07 at 11 37 28_f22d83e4](https://github.com/user-attachments/assets/d3ecd4b3-af19-4aac-a195-314b5ace007c)

![WhatsApp Image 2025-06-07 at 11 38 04_cac2ae54](https://github.com/user-attachments/assets/d37c3278-c5ea-4e6c-adab-a808729243df)







