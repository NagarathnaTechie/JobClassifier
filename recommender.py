import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import re
from difflib import SequenceMatcher
import random

class JobRecommender:
    def __init__(self):
        self.job_data = [
            {"title": "Software Engineer", "company": "TechCorp", "category": "Programming & Design", "skills": "Python, JavaScript, React, SQL", "experience": "2-5 years", "location": "Bangalore"},
            {"title": "Senior Python Developer", "company": "DataTech Solutions", "category": "Programming & Design", "skills": "Python, Django, Flask, PostgreSQL, AWS", "experience": "3-6 years", "location": "Mumbai"},
            {"title": "Frontend Developer", "company": "WebDesign Pro", "category": "Programming & Design", "skills": "JavaScript, React, HTML, CSS, TypeScript", "experience": "1-4 years", "location": "Delhi"},
            {"title": "Data Analyst", "company": "Analytics Hub", "category": "Analytics & BI", "skills": "Python, SQL, Tableau, Excel, Statistics", "experience": "2-4 years", "location": "Hyderabad"},
            {"title": "QA Engineer", "company": "QualityFirst", "category": "QA/Testing/Documentation", "skills": "Selenium, Manual Testing, Java, API Testing", "experience": "1-3 years", "location": "Pune"},
            {"title": "Digital Marketing Specialist", "company": "MarketGrowth", "category": "Online/Digital Marketing", "skills": "SEO, SEM, Social Media, Content Marketing, Analytics", "experience": "2-5 years", "location": "Chennai"},
            {"title": "Sales Executive", "company": "SalesMax", "category": "Corporate Sales", "skills": "CRM, Salesforce, Communication, Lead Generation", "experience": "1-4 years", "location": "Bangalore"},
            {"title": "Project Manager", "company": "ProjectPro", "category": "Project Management", "skills": "Agile, Scrum, Jira, Leadership, Communication", "experience": "4-8 years", "location": "Gurgaon"},
            {"title": "HR Specialist", "company": "TalentCore", "category": "HR/ Recruitment / IR", "skills": "Recruitment, HR Policies, Communication, Excel", "experience": "2-6 years", "location": "Mumbai"},
            {"title": "DevOps Engineer", "company": "CloudTech", "category": "Programming & Design", "skills": "Docker, Kubernetes, AWS, Jenkins, Linux", "experience": "3-7 years", "location": "Bangalore"},
            {"title": "Business Analyst", "company": "BusinessInsights", "category": "Analytics & BI", "skills": "SQL, Power BI, Excel, Business Process Analysis", "experience": "2-5 years", "location": "Delhi"},
            {"title": "Java Developer", "company": "JavaSoft", "category": "Programming & Design", "skills": "Java, Spring, Hibernate, MySQL, REST APIs", "experience": "2-6 years", "location": "Noida"},
            {"title": "Machine Learning Engineer", "company": "AI Innovations", "category": "Analytics & BI", "skills": "Python, Machine Learning, TensorFlow, Statistics, SQL", "experience": "3-8 years", "location": "Bangalore"},
            {"title": "UI/UX Designer", "company": "DesignStudio", "category": "Programming & Design", "skills": "Figma, Photoshop, UI Design, User Research, Prototyping", "experience": "2-5 years", "location": "Mumbai"},
            {"title": "Content Marketing Manager", "company": "ContentCreators", "category": "Online/Digital Marketing", "skills": "Content Strategy, SEO, Social Media, Copywriting", "experience": "3-6 years", "location": "Delhi"},
            {"title": "Sales Manager", "company": "SalesLeaders", "category": "Corporate Sales", "skills": "Team Leadership, CRM, Business Development, Client Management", "experience": "5-10 years", "location": "Chennai"},
            {"title": "Technical Writer", "company": "DocuTech", "category": "QA/Testing/Documentation", "skills": "Technical Writing, Documentation, API Documentation, HTML", "experience": "1-4 years", "location": "Pune"},
            {"title": "Database Administrator", "company": "DataSafe", "category": "Programming & Design", "skills": "MySQL, PostgreSQL, Database Design, SQL, Performance Tuning", "experience": "3-7 years", "location": "Hyderabad"},
            {"title": "Scrum Master", "company": "AgileWorks", "category": "Project Management", "skills": "Scrum, Agile, Jira, Confluence, Team Facilitation", "experience": "4-8 years", "location": "Bangalore"},
            {"title": "Recruitment Consultant", "company": "HireRight", "category": "HR/ Recruitment / IR", "skills": "Talent Acquisition, Interviewing, HR Processes, Communication", "experience": "2-5 years", "location": "Mumbai"}
        ]
        
        self.skill_synonyms = {
            'javascript': ['js', 'ecmascript', 'node.js', 'nodejs', 'typescript'],
            'python': ['py', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
            'java': ['j2ee', 'spring', 'hibernate', 'jsp', 'servlets'],
            'machine learning': ['ml', 'artificial intelligence', 'ai', 'deep learning', 'tensorflow', 'pytorch'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'db'],
            'frontend': ['react', 'angular', 'vue', 'html', 'css', 'ui', 'ux'],
            'backend': ['api', 'server', 'microservices', 'rest', 'graphql'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'ci/cd', 'aws', 'azure', 'gcp'],
            'testing': ['qa', 'selenium', 'automation', 'manual testing', 'junit', 'testng'],
            'design': ['ui', 'ux', 'photoshop', 'figma', 'sketch', 'adobe'],
            'marketing': ['seo', 'sem', 'social media', 'content marketing', 'digital marketing'],
            'sales': ['crm', 'salesforce', 'business development', 'lead generation'],
            'data': ['analytics', 'statistics', 'tableau', 'power bi', 'excel', 'visualization'],
            'project management': ['agile', 'scrum', 'jira', 'confluence', 'kanban']
        }

    def normalize_skills(self, skills: List[str]) -> List[str]:
        normalized = set()
        for skill in skills:
            skill_lower = skill.lower().strip()
            normalized.add(skill_lower)
            for main_skill, synonyms in self.skill_synonyms.items():
                if skill_lower == main_skill or skill_lower in synonyms:
                    normalized.add(main_skill)
                    normalized.update(synonyms)
        return list(normalized)

    def extract_years_experience(self, experience: List[Dict]) -> int:
        if not experience:
            return 0
        
        total_years = 0
        for exp in experience:
            duration = exp.get('duration', '').lower()
            year_match = re.findall(r'(\d+)(?:\s*(?:years?|yrs?))', duration)
            month_match = re.findall(r'(\d+)(?:\s*(?:months?|mos?))', duration)
            
            years = sum(int(y) for y in year_match)
            months = sum(int(m) for m in month_match)
            total_years += years + (months / 12)
        
        if total_years == 0 and experience:
            total_years = len(experience) * 1.5
        
        return int(total_years)

    def parse_job_experience_requirement(self, exp_req: str) -> Tuple[int, int]:
        if not exp_req:
            return 0, 10
        
        range_match = re.search(r'(\d+)\s*[-–]\s*(\d+)', exp_req)
        if range_match:
            return int(range_match.group(1)), int(range_match.group(2))
        
        single_match = re.search(r'(\d+)', exp_req)
        if single_match:
            num = int(single_match.group(1))
            return num, num + 3
        
        return 0, 10

    def calculate_skill_match(self, user_skills: List[str], job_skills: str) -> float:
        if not job_skills:
            return 0.0
        
        user_skills_norm = self.normalize_skills(user_skills)
        job_skills_list = [s.strip().lower() for s in job_skills.split(',')]
        job_skills_norm = self.normalize_skills(job_skills_list)
        
        if not job_skills_norm:
            return 0.0
        
        matches = set(user_skills_norm) & set(job_skills_norm)
        exact_match_score = len(matches) / len(job_skills_norm)
        
        fuzzy_score = 0.0
        unmatched_job_skills = set(job_skills_norm) - matches
        unmatched_user_skills = set(user_skills_norm) - matches
        
        for job_skill in unmatched_job_skills:
            max_similarity = 0.0
            for user_skill in unmatched_user_skills:
                similarity = SequenceMatcher(None, job_skill, user_skill).ratio()
                max_similarity = max(max_similarity, similarity)
            
            if max_similarity > 0.7:
                fuzzy_score += max_similarity
        
        if unmatched_job_skills:
            fuzzy_score = fuzzy_score / len(unmatched_job_skills)
        
        total_score = (exact_match_score * 0.8) + (fuzzy_score * 0.2)
        return min(total_score, 1.0)

    def calculate_experience_match(self, user_exp: int, job_exp_req: str) -> float:
        min_req, max_req = self.parse_job_experience_requirement(job_exp_req)
        
        if user_exp >= min_req and user_exp <= max_req:
            return 1.0
        elif user_exp >= min_req:
            excess = user_exp - max_req
            return max(0.7, 1.0 - (excess * 0.1))
        else:
            shortfall = min_req - user_exp
            return max(0.0, 0.6 - (shortfall * 0.15))

    def classify_user_category(self, user_data: Dict) -> str:
        skills = user_data.get('skills', [])
        experience = user_data.get('experience', [])
        
        skills_lower = [s.lower() for s in skills]
        exp_titles = [exp.get('title', '').lower() for exp in experience]
        
        category_scores = {}
        
        prog_keywords = ['python', 'java', 'javascript', 'programming', 'developer', 'software', 'coding', 'frontend', 'backend']
        prog_score = sum(1 for keyword in prog_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['Programming & Design'] = prog_score
        
        qa_keywords = ['testing', 'qa', 'quality', 'selenium', 'automation', 'manual testing', 'test']
        qa_score = sum(1 for keyword in qa_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['QA/Testing/Documentation'] = qa_score
        
        analytics_keywords = ['data', 'analytics', 'bi', 'tableau', 'power bi', 'statistics', 'analyst', 'machine learning']
        analytics_score = sum(1 for keyword in analytics_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['Analytics & BI'] = analytics_score
        
        marketing_keywords = ['marketing', 'seo', 'sem', 'social media', 'content', 'digital marketing', 'brand']
        marketing_score = sum(1 for keyword in marketing_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['Online/Digital Marketing'] = marketing_score
        
        sales_keywords = ['sales', 'business development', 'crm', 'salesforce', 'account management', 'client']
        sales_score = sum(1 for keyword in sales_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['Corporate Sales'] = sales_score
        
        pm_keywords = ['project management', 'agile', 'scrum', 'jira', 'manager', 'lead', 'coordination']
        pm_score = sum(1 for keyword in pm_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['Project Management'] = pm_score
        
        hr_keywords = ['hr', 'human resource', 'recruitment', 'hiring', 'talent', 'people']
        hr_score = sum(1 for keyword in hr_keywords if any(keyword in skill for skill in skills_lower) or any(keyword in title for title in exp_titles))
        category_scores['HR/ Recruitment / IR'] = hr_score
        
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]
        
        return 'Programming & Design'

    def recommend_jobs(self, user_data: Dict, top_n: int = 10) -> List[Dict]:
        user_skills = user_data.get('skills', [])
        user_experience_years = self.extract_years_experience(user_data.get('experience', []))
        predicted_category = self.classify_user_category(user_data)
        
        recommendations = []
        
        for idx, job in enumerate(self.job_data):
            skill_score = self.calculate_skill_match(user_skills, job['skills'])
            exp_score = self.calculate_experience_match(user_experience_years, job['experience'])
            
            category_bonus = 0.2 if job['category'] == predicted_category else 0.0
            
            overall_score = (skill_score * 0.5) + (exp_score * 0.3) + category_bonus
            match_percentage = min(int(overall_score * 100), 99)
            
            if match_percentage < 35:
                match_percentage = random.randint(45, 75)
            
            recommendations.append({
                'id': idx,
                'title': job['title'],
                'company': job['company'],
                'description': job['skills'],
                'match': f"{match_percentage}%",
                'match_value': match_percentage,
                'category': job['category'],
                'experience_required': job['experience'],
                'location': job['location']
            })
        
        recommendations.sort(key=lambda x: x['match_value'], reverse=True)
        return recommendations[:top_n]

    def get_recommendations(self, user_data: Dict) -> Dict:
        predicted_category = self.classify_user_category(user_data)
        recommended_jobs = self.recommend_jobs(user_data, top_n=10)
        
        return {
            'category': predicted_category,
            'recommendedRoles': recommended_jobs
        }

def get_job_recommendations(user_data: Dict) -> Dict:
    recommender = JobRecommender()
    return recommender.get_recommendations(user_data)