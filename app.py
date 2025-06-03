import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from resume_parser import ResumeParser
from recommender import get_job_recommendations
import tempfile
import os

# Initialize Firebase Admin SDK
if not firebase_admin._apps:  # Prevent re-initialization
    cred = credentials.Certificate('jobclassifier-938cc-db76c37f1690.json')
    firebase_admin.initialize_app(cred)

# Firebase Web API Key
FIREBASE_API_KEY = "AIzaSyCYu1nD3lamQETKuRR1DxQSfF2-A9gk2fU"

# Firebase REST API - Signup and Login
def firebase_signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": {"message": f"Network error: {str(e)}"}}

def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {"error": {"message": f"Network error: {str(e)}"}}

# Streamlit page config and enhanced dark theme styles
st.set_page_config(
    page_title="Job Classifier", 
    page_icon="📝", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Global Dark Theme */
    .stApp {
        background-color: #000000 !important;
        color: #ffffff !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Enhanced Card Styling */
    .card { 
        background: linear-gradient(145deg, #1a1a1a, #2d2d2d);
        border-radius: 16px; 
        padding: 2rem; 
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 2rem; 
        border: 1px solid #333;
        backdrop-filter: blur(10px);
    }
    
    .auth-card {
        background: linear-gradient(145deg, #1a1a1a, #2d2d2d);
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        border: 1px solid #444;
        max-width: 450px;
        margin: 0 auto;
        backdrop-filter: blur(15px);
    }
    
    .card-title { 
        font-size: 2rem; 
        font-weight: 700; 
        margin-bottom: 0.5rem; 
        color: #ffffff;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .card-description { 
        color: #b0b0b0; 
        font-size: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Job Card Styling */
    .job-card { 
        background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
        border-left: 4px solid #667eea; 
        color: #ffffff; 
        padding: 1.5rem; 
        margin-bottom: 1rem; 
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .job-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .job-title { 
        font-weight: 700; 
        color: #ffffff; 
        font-size: 1.25rem; 
        margin-bottom: 0.5rem;
    }
    
    .job-match { 
        float: right; 
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.5rem 1rem; 
        border-radius: 20px; 
        font-size: 0.875rem; 
        font-weight: 600;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Header Styling */
    .header { 
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1.5rem 2rem; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.3); 
        margin-bottom: 2rem; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
        border-radius: 16px;
        border: 1px solid #333;
    }
    
    .logo { 
        font-weight: 800; 
        font-size: 1.75rem; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .welcome-text {
        color: #b0b0b0;
        font-size: 1rem;
    }
    
    /* Section Title */
    .section-title { 
        font-size: 2.5rem; 
        color: #ffffff; 
        font-weight: 700; 
        margin-bottom: 1rem;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-subtitle {
        color: #b0b0b0;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Error and Success Messages */
    .error { 
        color: #ff6b6b; 
        font-size: 0.875rem; 
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: rgba(255, 107, 107, 0.1);
        border-radius: 8px;
        border-left: 4px solid #ff6b6b;
    }
    
    .success {
        color: #51cf66;
        font-size: 0.875rem;
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: rgba(81, 207, 102, 0.1);
        border-radius: 8px;
        border-left: 4px solid #51cf66;
    }
    
    /* Progress Bar */
    .progress-bar { 
        background-color: #333; 
        border-radius: 10px; 
        height: 8px; 
        margin-top: 1rem;
        overflow: hidden;
    }
    
    .progress-fill { 
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 100%; 
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #1a1a1a;
        border-radius: 10px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #b0b0b0;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        background-color: #2a2a2a !important;
        border: 2px dashed #667eea !important;
        border-radius: 12px !important;
        padding: 2rem !important;
    }
    
    /* Form styling */
    .stForm {
        background: transparent !important;
        border: none !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Warning and info messages */
    .stAlert {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'auth'
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

# Navigation & Logout
def navigate_to(page):
    st.session_state.current_page = page
    st.rerun()

def logout():
    st.session_state.is_logged_in = False
    st.session_state.user_info = None
    st.session_state.current_page = 'auth'
    st.session_state.resume_data = None
    st.session_state.recommendations = None
    st.rerun()

def check_authentication():
    """Check if user is authenticated, redirect to auth if not"""
    if not st.session_state.is_logged_in or not st.session_state.user_info:
        st.warning("Please log in to access this page.")
        navigate_to('auth')
        return False
    return True

def display_header():
    st.markdown("""
        <style>
            .header-bar {
                background-color: white;
                padding: 10px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #ddd;
            }
            .header-logo {
                font-size: 24px;
                font-weight: bold;
                color: #374151;
            }
            .welcome-text {
                text-align: center;
                margin-top: 10px;
                font-size: 25px;
            }
        </style>
        <div class="header-bar">
            <div class="header-logo">📝 Job Classifier</div>
            <div>
                <form action="?logout=true" method="post">
                    <button style="background:none;border:none;color:#007bff;cursor:pointer;">🚪 Logout</button>
                </form>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="welcome-text">
            Welcome, {st.session_state.user_info.get('name', 'User')}
        </div>
    """, unsafe_allow_html=True)

    if st.query_params.get("logout") == "true":
        logout()



# Authentication Page
def auth_page():
    # Clear any existing authentication state when on auth page
    if st.session_state.is_logged_in:
        st.session_state.is_logged_in = False
        st.session_state.user_info = None
    
    # Center the authentication form
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 Login", "👤 Sign Up"])

        with tab1:
            st.markdown('''
            <div class="auth-card">
                <h2 class="card-title">Welcome Back</h2>
                <p class="card-description">Sign in to your account</p>
            </div>
            ''', unsafe_allow_html=True)
            
            email = st.text_input("📧 Email", key="login_email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", key="login_password", placeholder="Enter your password")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("🚀 Login", key="login_btn", use_container_width=True):
                    if not email or not password:
                        st.error("Please enter both email and password")
                        return
                    
                    if not email.strip() or not password.strip():
                        st.error("Email and password cannot be empty")
                        return
                    
                    with st.spinner("Logging in..."):
                        response = firebase_login(email.strip(), password)
                                        
                        # Check for successful authentication
                        if response and "idToken" in response and response["idToken"]:
                            st.session_state.is_logged_in = True
                            st.session_state.user_info = {
                                'uid': response.get('localId', ''),
                                'email': response.get('email', email),
                                'name': email.split('@')[0],
                                'token': response['idToken']
                            }
                            st.success("🎉 Login successful!")
                            navigate_to('upload')
                        else:
                            # Ensure login state is False on failure
                            st.session_state.is_logged_in = False
                            st.session_state.user_info = None
                            
                            # Extract error message
                            if response and "error" in response:
                                error_msg = response["error"].get("message", "Login failed")
                                st.error(f"❌ Authentication failed: {error_msg}")
                            else:
                                st.error("❌ Login failed. Please check your credentials.")

        with tab2:
            st.markdown('''
            <div class="auth-card">
                <h2 class="card-title">Join Us</h2>
                <p class="card-description">Create your account</p>
            </div>
            ''', unsafe_allow_html=True)
            
            name = st.text_input("👤 Name", key="signup_name", placeholder="Enter your full name")
            email = st.text_input("📧 Email", key="signup_email", placeholder="Enter your email")
            password = st.text_input("🔒 Password", type="password", key="signup_password", placeholder="Create a password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", key="signup_confirm_password", placeholder="Confirm your password")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("✨ Sign Up", key="signup_btn", use_container_width=True):
                    if not all([name, email, password, confirm_password]):
                        st.error("Please fill all fields!")
                        return
                    
                    if not all([x.strip() for x in [name, email, password, confirm_password]]):
                        st.error("All fields must contain valid data!")
                        return
                        
                    if password != confirm_password:
                        st.error("Passwords don't match!")
                        return
                    
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters long!")
                        return
                    
                    with st.spinner("Creating account..."):
                        response = firebase_signup(email.strip(), password)
                        
                        # Check for successful signup
                        if response and "idToken" in response and response["idToken"]:
                            st.session_state.is_logged_in = True
                            st.session_state.user_info = {
                                'uid': response.get('localId', ''),
                                'email': response.get('email', email),
                                'name': name.strip(),
                                'token': response['idToken']
                            }
                            st.success("🎉 Account created successfully!")
                            navigate_to('upload')
                        else:
                            # Ensure login state is False on failure
                            st.session_state.is_logged_in = False
                            st.session_state.user_info = None
                            
                            # Extract error message
                            if response and "error" in response:
                                error_msg = response["error"].get("message", "Signup failed")
                                st.error(f"❌ Account creation failed: {error_msg}")
                            else:
                                st.error("❌ Signup failed. Please try again.")
    

# Upload Page
def upload_page():
    if not check_authentication():
        return
        
    display_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<h1 class="section-title">📄 Upload Resume</h1>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Upload your PDF resume to get personalized job recommendations</p>', unsafe_allow_html=True)
        
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file", 
            type="pdf",
            help="Upload your resume in PDF format for analysis"
        )
        
        if uploaded_file:
            try:
                with st.spinner("🔍 Processing your resume..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        pdf_path = tmp_file.name
                    
                    parser = ResumeParser()
                    resume_data = parser.parse_resume(pdf_path)

                    if 'error' in resume_data:
                        st.error(f"❌ Error processing resume: {resume_data['error']}")
                        return
                    
                    st.session_state.resume_data = resume_data
                    os.remove(pdf_path)
                    st.success("✅ Resume processed successfully!")
                    navigate_to("review")
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def review_page():
    if not check_authentication():
        return
        
    display_header()
    if not st.session_state.resume_data:
        st.warning("⚠️ No resume data. Please upload a resume.")
        if st.button("📄 Upload Resume"):
            navigate_to("upload")
        return
    
    resume_data = st.session_state.resume_data
    st.markdown('<h1 class="section-title">✏️ Review Information</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Review and edit the extracted information from your resume</p>', unsafe_allow_html=True)
    
    with st.form("review_form"):
        
        st.markdown("### 👤 Personal Information")
        name = st.text_input("Full Name", value=resume_data['name'] if resume_data['name'] != "Not Found" else "")
        if not resume_data['name'] or resume_data['name'] == "Not Found":
            if not name:
                st.markdown('<p class="error">⚠️ Unable to extract name. Please enter manually.</p>', unsafe_allow_html=True)
        
        st.markdown("### 🛠️ Skills")
        skills = st.text_area("Skills (comma-separated)", value=", ".join(resume_data['skills']) if resume_data['skills'] else "", height=100)
        if not resume_data['skills']:
            if not skills:
                st.markdown('<p class="error">⚠️ No skills found. Please enter manually.</p>', unsafe_allow_html=True)
        
        st.markdown("### 🎓 Education")
        education_value = "\n".join([f"{edu['degree']}, {edu['institution']}, {edu['year']}" for edu in resume_data['education']]) if resume_data['education'] else ""
        education = st.text_area("Education (degree, institution, year - one per line)", value=education_value, height=100)
        if not resume_data['education']:
            if not education:
                st.markdown('<p class="error">⚠️ No education found. Please enter manually.</p>', unsafe_allow_html=True)
        
        st.markdown("### 💼 Work Experience")
        experience_value = "\n".join([f"{exp['title']}, {exp['company']}, {exp['duration']}, {exp['description']}" for exp in resume_data['experience']]) if resume_data['experience'] else ""
        experience = st.text_area("Work Experience (title, company, duration, description - one per line)", value=experience_value, height=150)
        if not resume_data['experience']:
            if not experience:
                st.markdown('<p class="error">⚠️ No work experience found. Please enter manually.</p>', unsafe_allow_html=True)
        
        st.markdown("### 🎯 Additional Information")
        job_title = st.text_input("Desired Job Title", value=resume_data.get('job_title', ""))
        description = st.text_area("About Yourself", value=resume_data.get('description', ""), height=100)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.form_submit_button("🚀 Get Recommendations", use_container_width=True):
                if not name or not skills:
                    st.error("❌ Name and Skills are required fields!")
                    return
                
                try:
                    st.session_state.resume_data['name'] = name
                    st.session_state.resume_data['skills'] = [s.strip() for s in skills.split(",") if s.strip()]
                    
                    education_list = []
                    if education:
                        for e in education.split("\n"):
                            if e.strip():
                                parts = [p.strip() for p in e.split(",")]
                                if len(parts) >= 3:
                                    education_list.append({"degree": parts[0], "institution": parts[1], "year": parts[2]})
                                elif len(parts) >= 2:
                                    education_list.append({"degree": parts[0], "institution": parts[1], "year": ""})
                                else:
                                    st.warning(f"⚠️ Invalid education entry: {e}. Use: degree, institution, year")
                    
                    experience_list = []
                    if experience:
                        for x in experience.split("\n"):
                            if x.strip():
                                parts = [p.strip() for p in x.split(",")]
                                if len(parts) >= 3:
                                    exp_dict = {"title": parts[0], "company": parts[1], "duration": parts[2]}
                                    if len(parts) > 3:
                                        exp_dict["description"] = parts[3]
                                    else:
                                        exp_dict["description"] = ""
                                    experience_list.append(exp_dict)
                                else:
                                    st.warning(f"⚠️ Invalid experience entry: {x}. Use: title, company, duration, description")
                    
                    st.session_state.resume_data['education'] = education_list
                    st.session_state.resume_data['experience'] = experience_list
                    st.session_state.resume_data['job_title'] = job_title
                    st.session_state.resume_data['description'] = description
                    
                    with st.spinner("🔍 Getting job recommendations..."):
                        recommendations = get_job_recommendations(st.session_state.resume_data)
                        st.session_state.recommendations = recommendations
                        navigate_to("results")
                except Exception as e:
                    st.error(f"❌ Error processing recommendations: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def results_page():
    if not check_authentication():
        return
        
    display_header()
    if not st.session_state.recommendations or 'recommendedRoles' not in st.session_state.recommendations:
        st.warning("⚠️ No recommendations available. Please review your resume.")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📝 Go Back to Review", use_container_width=True):
                navigate_to("review")
        return
    
    recommendations = st.session_state.recommendations
    st.markdown('<h1 class="section-title">🎯 Job Recommendations</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Your personalized job matches based on your profile</p>', unsafe_allow_html=True)
    
    # Category display
    st.markdown(f"""
    <div class="card" style="text-align: center; margin-bottom: 2rem;">
        <h3 style="color: #667eea; margin-bottom: 0.5rem;">📊 Predicted Category</h3>
        <h2 style="color: #ffffff; font-size: 1.5rem;">{recommendations['category']}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    top_recommendations = recommendations['recommendedRoles'][:5]
    
    if not top_recommendations:
        st.warning("⚠️ No suitable job matches found. Try updating your skills or experience.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Update Resume", use_container_width=True):
                navigate_to("review")
        with col2:
            if st.button("📄 Upload New Resume", use_container_width=True):
                navigate_to("upload")
        return
    
    st.markdown(f"### 🏆 Top {len(top_recommendations)} Matches")
    
    for i, job in enumerate(top_recommendations, 1):
        percentage = int(float(job['match'].strip('%')))
        
        # Color coding based on match percentage
        if percentage >= 80:
            border_color = "#51cf66"  # Green
        elif percentage >= 60:
            border_color = "#ffd43b"  # Yellow
        else:
            border_color = "#ff6b6b"  # Red
            
        st.markdown(f"""
        <div class="job-card" style="border-left-color: {border_color};">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div style="flex: 1;">
                    <h4 class="job-title">#{i} {job['title']}</h4>
                </div>
                <span class="job-match">{job['match']} Match</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("### 🔄 Next Steps")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Upload New Resume", use_container_width=True):
            navigate_to("upload")
    with col2:
        if st.button("✏️ Edit Current Resume", use_container_width=True):
            navigate_to("review")

def main():
    # Force authentication check on protected pages
    if st.session_state.current_page != 'auth' and not st.session_state.is_logged_in:
        st.session_state.current_page = 'auth'
    
    if not st.session_state.is_logged_in or st.session_state.current_page == 'auth':
        auth_page()
    elif st.session_state.current_page == 'upload':
        upload_page()
    elif st.session_state.current_page == 'review':
        review_page()
    elif st.session_state.current_page == 'results':
        results_page()
    else:
        upload_page()

if __name__ == "__main__":
    main()

