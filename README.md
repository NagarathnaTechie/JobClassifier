# 🔍 Job Classifier - AI-Powered Resume Matcher 🚀

**Job Classifier** is a smart Streamlit web app that analyzes your resume and matches you with the perfect job opportunities using NLP. Say goodbye to manual job hunting!  

✨ **Live Demo**: [Try it now!](https://jobclassifier-24.streamlit.app/)  

---

## 📌 Table of Contents
- [🌟 Key Features](#-key-features)
- [🛠️ Technical Stack](#️-technical-stack)
- [⚙️ How It Works](#️-how-it-works)
- [📸 Screenshots](#-screenshots)
- [🚀 Deployment](#-deployment)

---

## 🌟 Key Features

<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-top: 20px;">

<div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border-left: 4px solid #4285F4; flex: 1 1 300px;">
<h3>🔒 Secure Authentication</h3>
<ul>
<li>Firebase email/password login</li>
<li>Session management with Streamlit</li>
<li>Encrypted API keys</li>
</ul>
</div>

<div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border-left: 4px solid #34A853; flex: 1 1 300px;">
<h3>📄 Smart Resume Parsing</h3>
<ul>
<li>Extracts skills/experience from PDFs</li>
<li>PyPDF2 + spaCy NLP processing</li>
<li>Editable data review</li>
</ul>
</div>

<div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border-left: 4px solid #EA4335; flex: 1 1 300px;">
<h3>💼 AI Job Matching</h3>
<ul>
<li>Role-based recommendations</li>
<li>Match percentage scoring</li>
<li>Custom dataset integration</li>
</ul>
</div>

</div>

---

## 🛠️ Technical Stack

| Category        | Technologies |
|----------------|-------------|
| **Frontend**   | Streamlit, Custom CSS |
| **Backend**    | Python 3.11, Firebase Admin SDK |
| **NLP**        | spaCy (en_core_web_sm), PyPDF2 |
| **Data**       | Pandas, NumPy |
| **Deployment** | Streamlit Community Cloud |

---

## ⚙️ How It Works

1. **User Authentication**  
   ```python
   # Firebase Auth Example
   auth = firebase_admin.auth()
   user = auth.get_user_by_email(email)
   Here's the continuation of your Job Classifier README in the same style:


2. **Resume Processing**  
   ```python
   # PDF Text Extraction
   reader = PyPDF2.PdfReader(uploaded_file)
   text = "".join([page.extract_text() for page in reader.pages])
   
   # NLP Processing
   nlp = spacy.load("en_core_web_sm")
   doc = nlp(text)
   skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
   ```

3. **Job Matching Algorithm**  
   ```python
   def calculate_match(resume_skills, job_requirements):
       # Cosine similarity implementation
       vectorizer = TfidfVectorizer()
       tfidf_matrix = vectorizer.fit_transform([resume_skills, job_requirements])
       return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
   ```

4. **Recommendation Engine**  
   ```python
   # Load job dataset
   jobs_df = pd.read_csv("Job_Roles.csv")
   
   # Get top 3 matches
   jobs_df["match_score"] = jobs_df["requirements"].apply(lambda x: calculate_match(resume_text, x))
   top_jobs = jobs_df.sort_values("match_score", ascending=False).head(3)
   ```

---

## 📸 Screenshots

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px;">

<div style="border: 1px solid #e1e4e8; border-radius: 6px; overflow: hidden;">
<img src="https://github.com/user-attachments/assets/45e4f71f-6d23-4b00-ad1d-d1c1bb431578" alt="Login Page" style="width: 100%;">
<p style="padding: 8px 12px; background: #f6f8fa; margin: 0;">🔐 <strong>Login Page</strong>: Secure Firebase authentication</p>
</div>

<div style="border: 1px solid #e1e4e8; border-radius: 6px; overflow: hidden;">
<img src="https://github.com/user-attachments/assets/e8d67493-627f-4bcb-86ab-8b68c1e5e8a1" alt="Resume Upload" style="width: 100%;">
<p style="padding: 8px 12px; background: #f6f8fa; margin: 0;">📤 <strong>Resume Upload</strong>: PDF parsing interface</p>
</div>

<div style="border: 1px solid #e1e4e8; border-radius: 6px; overflow: hidden;">
<img src="https://github.com/user-attachments/assets/12b22d07-b5de-4316-8c27-e29ccaa5722f" alt="Job Matches" style="width: 100%;">
<p style="padding: 8px 12px; background: #f6f8fa; margin: 0;">💼 <strong>Job Matches</strong>: AI-generated recommendations</p>
</div>

</div>

---

## 🚀 Deployment

### Local Setup
```bash
# 1. Clone repository
git clone https://github.com/yourusername/job-classifier.git
cd job-classifier

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
echo "FIREBASE_API_KEY=your_key" > .env

# 5. Run application
streamlit run app.py
```

### Cloud Deployment
1. Create `secrets.toml` with Firebase credentials
2. Push to GitHub
3. Deploy via Streamlit Community Cloud

---

<div style="background: #e3f2fd; padding: 16px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #2196F3;">
💡 <strong>Pro Tip:</strong> For better results, structure your resume with clear sections for <strong>Skills</strong>, <strong>Experience</strong>, and <strong>Education</strong>. The NLP model extracts information best from well-formatted PDFs!
</div>

<hr style="border: 0.5px solid #e1e4e8; margin: 24px 0;">

## 📞 Contact
Have questions or suggestions?

📧 [Email](nagarathnashenoy123@gmail.com)

🔗 [LinkedIn](https://www.linkedin.com/in/nagarathna-shenoy-457751218).

<h3 align="center">🚀 Ready to revolutionize your job search?</h3>
<p align="center">
<a href="https://jobclassifier-24.streamlit.app/" style="background: #4285F4; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none;">Try Live Demo</a>
</p>


