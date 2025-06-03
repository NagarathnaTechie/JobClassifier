import PyPDF2
import re
import spacy
import sys
from typing import Dict, List

# Load spaCy model
nlp = spacy.load("en_core_web_sm")



class ResumeParser:
    def __init__(self):
        self.skills_patterns = [
            r'(?:skills?|technical skills?|core competencies|expertise|proficiencies)[:]*\s*\n?(.*?)(?:\n\n|\n[A-Z][a-z]+\s*[:]*|$)',
            r'(?:technologies?|programming languages?|tools?)[:]*\s*\n?(.*?)(?:\n\n|\n[A-Z][a-z]+\s*[:]*|$)'
        ]
        
        self.education_patterns = [
            r'(?:education|academic|qualification|degree)[:]*\s*\n?(.*?)(?:\n\n|\n[A-Z][a-z]+\s*[:]*|$)',
            r'(?:university|college|institute|school)[:]*\s*\n?(.*?)(?:\n\n|\n[A-Z][a-z]+\s*[:]*|$)'
        ]
        
        self.experience_patterns = [
            r'(?:experience|employment|work history|professional experience|career)[:]*\s*\n?(.*?)(?:\n\n|\n[A-Z][a-z]+\s*[:]*|$)',
            r'(?:worked at|employed at|position at)[:]*\s*\n?(.*?)(?:\n\n|\n[A-Z][a-z]+\s*[:]*|$)'
        ]

    def extract_pdf_text(self, pdf_path: str) -> str:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def extract_name(self, text: str) -> str:
        lines = text.split('\n')
        
        # Try first few lines for name
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 2 and len(line) < 50:
                if re.match(r'^[A-Za-z\s\.]+$', line) and len(line.split()) <= 4:
                    avoid_words = ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'contact', 'email', 'phone']
                    if not any(word in line.lower() for word in avoid_words):
                        return line.strip()
        
        # Use NLP to find person names
        doc = nlp(text[:500])
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text.strip()
        
        return "Not Found"

    def extract_skills(self, text: str) -> List[str]:
        skills = set()
        
        skill_keywords = [
            'python', 'java', 'javascript', 'js', 'react', 'angular', 'vue', 'node', 'nodejs',
            'html', 'css', 'sql', 'mysql', 'postgresql', 'mongodb', 'oracle', 'php', 'ruby',
            'c++', 'c#', 'go', 'rust', 'swift', 'kotlin', 'r', 'matlab', 'scala', 'perl',
            'django', 'flask', 'spring', 'express', 'laravel', 'rails', 'asp.net',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'linux', 'unix',
            'machine learning', 'ml', 'deep learning', 'ai', 'artificial intelligence',
            'data science', 'data analysis', 'statistics', 'tableau', 'power bi', 'excel',
            'photoshop', 'illustrator', 'figma', 'sketch', 'ui', 'ux', 'design',
            'project management', 'agile', 'scrum', 'jira', 'confluence',
            'marketing', 'seo', 'sem', 'social media', 'content writing', 'copywriting',
            'sales', 'crm', 'salesforce', 'hubspot', 'communication', 'leadership',
            'testing', 'qa', 'selenium', 'junit', 'cypress', 'postman',
            'devops', 'ci/cd', 'terraform', 'ansible', 'monitoring'
        ]
        
        text_lower = text.lower()
        
        # Extract using patterns
        for pattern in self.skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                skill_list = re.split(r'[,;\n\|•\-\*]', match)
                for skill in skill_list:
                    skill = skill.strip()
                    if len(skill) > 1 and len(skill) < 30:
                        skills.add(skill)
        
        # Find skills from keyword list
        for skill in skill_keywords:
            if skill in text_lower:
                skills.add(skill.title())
        
        # Clean and validate skills
        cleaned_skills = []
        for skill in skills:
            skill = re.sub(r'[^\w\s\+\#\.]', '', skill).strip()
            if len(skill) > 1 and not skill.isdigit():
                cleaned_skills.append(skill)
        
        return list(set(cleaned_skills))[:20]

    def extract_education(self, text: str) -> List[Dict[str, str]]:
        education = []
        
        degree_patterns = [
            r'(?:bachelor|b\.?[aes]\.?|bs|be|btech|b\.tech)',
            r'(?:master|m\.?[aes]\.?|ms|me|mtech|m\.tech|mba)',
            r'(?:phd|ph\.d|doctorate|doctor)',
            r'(?:diploma|certificate|associate)'
        ]
        
        institution_patterns = [
            r'(?:university|college|institute|school|academy)',
            r'(?:iit|nit|bits|vit|srm|amity|mit|stanford|harvard|berkeley)'
        ]
        
        for pattern in self.education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                lines = match.split('\n')
                for line in lines:
                    line = line.strip()
                    if len(line) > 10:
                        degree = ""
                        for deg_pattern in degree_patterns:
                            deg_match = re.search(deg_pattern, line, re.IGNORECASE)
                            if deg_match:
                                degree = deg_match.group()
                                break
                        
                        institution = ""
                        for inst_pattern in institution_patterns:
                            inst_match = re.search(f'.*{inst_pattern}.*', line, re.IGNORECASE)
                            if inst_match:
                                institution = inst_match.group().strip()
                                break
                        
                        year_match = re.search(r'(19|20)\d{2}', line)
                        year = year_match.group() if year_match else ""
                        
                        if degree or institution:
                            education.append({
                                "degree": degree.title() if degree else line[:50],
                                "institution": institution.title() if institution else "Not specified",
                                "year": year
                            })
        
        return education[:5]

    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        experience = []
        
        company_patterns = [
            r'(?:at|@)\s+([A-Z][a-zA-Z\s&,\.]+(?:Inc|LLC|Ltd|Corp|Corporation|Company|Technologies|Systems|Solutions|Services)?)',
            r'([A-Z][a-zA-Z\s&,\.]+(?:Inc|LLC|Ltd|Corp|Corporation|Company|Technologies|Systems|Solutions|Services))'
        ]
        
        title_patterns = [
            r'(?:software|senior|junior|lead|principal|sr|jr)?\s*(?:engineer|developer|analyst|manager|consultant|specialist|executive|associate|intern)',
            r'(?:data scientist|product manager|project manager|business analyst|ui designer|ux designer|devops engineer)'
        ]
        
        for pattern in self.experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                lines = match.split('\n')
                current_exp = {"title": "", "company": "", "duration": "", "description": ""}
                
                for line in lines:
                    line = line.strip()
                    if len(line) > 5:
                        for title_pattern in title_patterns:
                            title_match = re.search(title_pattern, line, re.IGNORECASE)
                            if title_match and not current_exp["title"]:
                                current_exp["title"] = title_match.group().strip().title()
                                break
                        
                        for comp_pattern in company_patterns:
                            comp_match = re.search(comp_pattern, line, re.IGNORECASE)
                            if comp_match and not current_exp["company"]:
                                current_exp["company"] = comp_match.group(1).strip() if comp_match.groups() else comp_match.group().strip()
                                break
                        
                        duration_match = re.search(r'((?:19|20)\d{2}.*?(?:19|20)\d{2}|(?:\d+)?\s*(?:years?|months?|yrs?))', line, re.IGNORECASE)
                        if duration_match and not current_exp["duration"]:
                            current_exp["duration"] = duration_match.group().strip()
                        
                        if len(line) > 30 and not current_exp["description"]:
                            current_exp["description"] = line[:200]
                
                if current_exp["title"] or current_exp["company"]:
                    experience.append(current_exp)
        
        return experience[:5]

    def parse_resume(self, pdf_path: str) -> Dict:
        try:
            text = self.extract_pdf_text(pdf_path)
            
            parsed_data = {
                "name": self.extract_name(text),
                "skills": self.extract_skills(text),
                "education": self.extract_education(text),
                "experience": self.extract_experience(text)
            }
            
            return parsed_data
            
        except Exception as e:
            return {
                "error": str(e),
                "name": "Error parsing resume",
                "skills": [],
                "education": [],
                "experience": []
            }

def parse_resume_file(pdf_path: str) -> Dict:
    parser = ResumeParser()
    return parser.parse_resume(pdf_path)
