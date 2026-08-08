"""
<<<<<<< HEAD
HR Resume Analyzer - Enterprise Edition
========================================
Real-time AI-powered resume analysis for HR departments
Features:
  • Bulk upload of resumes (PDF, DOCX, TXT)
  • Match against company job requirements
  • Automatic skill extraction and matching
  • Candidate ranking by suitability (0-100%)
  • Natural language summary with Web Speech API voice narration
  • Candidate profiles with detailed breakdown
  • Persistent database of all analyses
  
Run:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
=======
Full-Stack HR Resume Analyzer
Complete application with authentication, export, and advanced features
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
"""

import os
import re
import json
<<<<<<< HEAD
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, render_template
=======
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
from werkzeug.utils import secure_filename
import PyPDF2
import docx2txt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

<<<<<<< HEAD
from models import db, JobRequirement, Candidate
=======
from models import db, User, JobRequirement, Candidate, CommunicationLog
import io
import csv
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4

# ============================================================================
# Flask App Setup
# ============================================================================
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "resume_analyzer.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

db.init_app(app)

=======

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-12345'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "resume_analyzer.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Initialize extensions
db.init_app(app)
CORS(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

# Create database tables
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
<<<<<<< HEAD

# ============================================================================
# Skill Library & NLP Constants
# ============================================================================
SKILL_LIBRARY = [
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
    'r', 'kotlin', 'swift', 'php', 'ruby', 'perl', 'scala', 'matlab',
    
    # Web Technologies
    'html', 'css', 'react', 'angular', 'vue.js', 'next.js', 'svelte',
    'django', 'flask', 'fastapi', 'node.js', 'express', 'spring', 'spring boot',
    'asp.net', 'laravel', 'rails', 'gin', 'echo',
    
    # Mobile
    'ios', 'android', 'react native', 'flutter', 'xamarin', 'kotlin',
    
    # Data & AI/ML
=======
MAX_RESUMES_PER_UPLOAD = 10

# ============================================================================
# Skill Library
# ============================================================================
SKILL_LIBRARY = [
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
    'r', 'kotlin', 'swift', 'php', 'ruby', 'perl', 'scala', 'matlab',
    'html', 'css', 'react', 'angular', 'vue.js', 'next.js', 'svelte',
    'django', 'flask', 'fastapi', 'node.js', 'express', 'spring', 'spring boot',
    'asp.net', 'laravel', 'rails', 'gin', 'echo',
    'ios', 'android', 'react native', 'flutter', 'xamarin',
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    'machine learning', 'deep learning', 'nlp', 'natural language processing',
    'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
    'pandas', 'numpy', 'data analysis', 'data science', 'data engineering',
    'big data', 'artificial intelligence', 'ai', 'llm', 'generative ai',
<<<<<<< HEAD
    'huggingface', 'opencv', 'spark', 'hadoop',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s',
    'ci/cd', 'jenkins', 'gitlab', 'github actions', 'terraform', 'ansible',
    'cloudformation', 'pulumi', 'linux', 'git', 'github', 'gitlab',
    'container', 'microservices',
    
    # Databases
    'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'oracle',
    'elasticsearch', 'firebase', 'sqlite', 'cassandra', 'dynamodb',
    'cosmosdb', 'mariadb',
    
    # Testing & Quality
    'testing', 'unit testing', 'integration testing', 'cypress', 'jest',
    'junit', 'pytest', 'selenium', 'qa', 'quality assurance',
    
    # Soft Skills
    'leadership', 'management', 'communication', 'teamwork', 'collaboration',
    'problem solving', 'project management', 'agile', 'scrum', 'kanban',
    'time management', 'critical thinking', 'presentation', 'mentoring',
    'strategic thinking', 'analytical', 'creative', 'adaptable',
    
    # Tools & Platforms
    'excel', 'power bi', 'tableau', 'jira', 'confluence', 'salesforce',
    'sap', 'figma', 'photoshop', 'illustrator', 'sketch', 'xd',
    'slack', 'asana', 'monday.com', 'notion',
]

STOPWORDS = {
    'the', 'and', 'a', 'an', 'of', 'to', 'in', 'for', 'on', 'with', 'is',
    'are', 'as', 'at', 'by', 'or', 'be', 'this', 'that', 'will', 'we',
    'you', 'your', 'our', 'it', 'from', 'have', 'has', 'who', 'their',
    'job', 'role', 'work', 'years', 'year', 'experience', 'team', 'company',
}

# ============================================================================
# Text Extraction Functions
=======
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'k8s',
    'ci/cd', 'jenkins', 'gitlab', 'github actions', 'terraform', 'ansible',
    'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis', 'oracle',
    'elasticsearch', 'firebase', 'sqlite', 'cassandra', 'dynamodb',
    'testing', 'unit testing', 'integration testing', 'cypress', 'jest',
    'leadership', 'management', 'communication', 'teamwork', 'collaboration',
    'problem solving', 'project management', 'agile', 'scrum', 'kanban',
    'excel', 'power bi', 'tableau', 'jira', 'confluence', 'salesforce',
]

# ============================================================================
# Authentication Routes
# ============================================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        full_name = data.get('full_name')
        
        # Validation
        if not username or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful! Please log in.'}), 201
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('dashboard')}), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ============================================================================
# Dashboard & Main Routes
# ============================================================================
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    jobs = JobRequirement.query.filter_by(user_id=current_user.id).all()
    stats = {
        'total_jobs': len(jobs),
        'total_candidates': sum(len(j.candidates) for j in jobs),
        'active_jobs': len([j for j in jobs if j.status == 'active']),
    }
    return render_template('dashboard.html', jobs=jobs, stats=stats)


# ============================================================================
# Text Processing Functions
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
# ============================================================================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


<<<<<<< HEAD
def extract_text_from_pdf(path):
    """Extract all text from PDF"""
    text = ''
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ''
                text += page_text + '\n'
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text


def extract_text_from_docx(path):
    """Extract all text from DOCX"""
    try:
        return docx2txt.process(path) or ''
    except Exception as e:
        print(f"DOCX extraction error: {e}")
        return ''


def extract_text_from_txt(path):
    """Extract text from plain text file"""
    try:
        with open(path, 'r', errors='ignore', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"TXT extraction error: {e}")
        return ''


def extract_text(path, ext):
    """Route to correct extraction method based on file extension"""
    if ext == 'pdf':
        return extract_text_from_pdf(path)
    elif ext == 'docx':
        return extract_text_from_docx(path)
    elif ext == 'txt':
        return extract_text_from_txt(path)
=======
def extract_text(path, ext):
    try:
        if ext == 'pdf':
            text = ''
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text() or ''
                    text += page_text + '\n'
            return text
        elif ext == 'docx':
            return docx2txt.process(path) or ''
        elif ext == 'txt':
            with open(path, 'r', errors='ignore', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"Extraction error: {e}")
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    return ''


def clean_text(text):
<<<<<<< HEAD
    """Normalize and clean text"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


<<<<<<< HEAD
# ============================================================================
# Analysis Functions
# ============================================================================
def extract_email(text):
    """Find email address in text"""
=======
def extract_email(text):
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text):
<<<<<<< HEAD
    """Find phone number in text"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?(?:\d{3})\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_name(text):
<<<<<<< HEAD
    """Intelligently guess candidate name from first lines"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:10]:
        words = line.split()
        if 1 < len(words) <= 5 and all(w[0:1].isalpha() for w in words):
<<<<<<< HEAD
            if not any(k in line.lower() for k in ['resume', 'curriculum', 'cv', '@', 'http', 'mailto']):
=======
            if not any(k in line.lower() for k in ['resume', 'curriculum', 'cv', '@', 'http']):
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
                return line.title()
    return 'Candidate'


def find_skills(text, library=SKILL_LIBRARY):
<<<<<<< HEAD
    """Find all recognized skills in text (case-insensitive)"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    text_lower = text.lower()
    found = set()
    for skill in library:
        pattern = r'(?<![a-zA-Z0-9])\b' + re.escape(skill.lower()) + r'\b(?![a-zA-Z0-9])'
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def detect_years_experience(text):
<<<<<<< HEAD
    """Extract years of experience from text"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    matches = re.findall(r'(\d+)\+?\s*(?:-\s*\d+\s*)?years?', text.lower())
    years = [int(m) for m in matches if 0 < int(m) < 70]
    return max(years) if years else None


def tfidf_similarity(resume_text, jd_text):
<<<<<<< HEAD
    """Compute TF-IDF cosine similarity between resume and job description"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except (ValueError, IndexError):
        return 0.0


<<<<<<< HEAD
def extract_top_talents(resume_text, matched_skills, max_count=5):
    """Extract top 5 talents/unique strengths from resume"""
    talents = []
    
    # Look for certifications
    cert_pattern = r'(?:certification|certified|credential)[:\s]+([^,.\n]+)'
    certs = re.findall(cert_pattern, resume_text, re.IGNORECASE)
    talents.extend([c.strip().title() for c in certs[:2]])
    
    # Look for awards/achievements
    achievement_pattern = r'(?:award|achievement|recognized)[:\s]+([^,.\n]+)'
    achievements = re.findall(achievement_pattern, resume_text, re.IGNORECASE)
    talents.extend([a.strip().title() for a in achievements[:2]])
    
    # Add top matched skills
    talents.extend(sorted(matched_skills)[:5])
    
    # Remove duplicates and limit
    talents = list(dict.fromkeys(talents))[:max_count]
    return talents if talents else ['Professional', 'Dedicated', 'Capable']


def calculate_scores(resume_text, jd_text, resume_skills, jd_skills, years_exp, required_exp):
    """Calculate detailed scoring breakdown"""
    
    # Text similarity (40%)
    similarity = tfidf_similarity(resume_text, jd_text)
    similarity_score = round(similarity * 100, 1)
    
    # Skill matching (45%)
=======
def calculate_scores(resume_text, jd_text, resume_skills, jd_skills, years_exp, required_exp):
    similarity = tfidf_similarity(resume_text, jd_text)
    similarity_score = round(similarity * 100, 1)
    
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    if jd_skills:
        matched = resume_skills & jd_skills
        skill_match = len(matched) / len(jd_skills)
        skill_match_score = round(skill_match * 100, 1)
    else:
        skill_match_score = 50.0
    
<<<<<<< HEAD
    # Experience matching (15%)
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    experience_score = 50.0
    if required_exp and years_exp:
        if years_exp >= required_exp:
            experience_score = 100.0
        elif years_exp >= required_exp - 1:
            experience_score = 75.0
        elif years_exp >= required_exp - 2:
            experience_score = 50.0
        else:
            experience_score = max(20.0, (years_exp / required_exp) * 100)
    elif years_exp is not None:
        experience_score = min(100.0, years_exp * 10)
    
    experience_score = round(experience_score, 1)
<<<<<<< HEAD
    
    # Weighted overall score
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    overall = (0.40 * similarity_score + 0.45 * skill_match_score + 0.15 * experience_score) / 100
    overall = max(0.0, min(1.0, overall))
    overall_score = round(overall * 100)
    
    return {
        'overall': overall_score,
        'similarity': similarity_score,
        'skill_match': skill_match_score,
        'experience': experience_score
    }


def get_suitability_verdict(score):
<<<<<<< HEAD
    """Convert score to suitability level and phrase"""
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    if score >= 80:
        return 'Excellent', 'Excellent Match', 'This candidate is an excellent fit for the role. Highly recommended for interview.'
    elif score >= 65:
        return 'Good', 'Good Match', 'This candidate has strong qualifications and meets most requirements. Recommended for interview.'
    elif score >= 50:
        return 'Fair', 'Fair Match', 'This candidate has moderate qualifications. Could be considered for interview if other candidates are limited.'
    elif score >= 35:
        return 'Weak', 'Weak Match', 'This candidate has limited alignment with requirements. May benefit from training or further development.'
    else:
        return 'Poor', 'Poor Match', 'This candidate does not meet the key requirements for this role.'


<<<<<<< HEAD
def generate_summary(candidate_name, score, years_exp, required_exp, matched_skills, missing_skills, verdict_phrase):
    """Generate natural language summary for voice narration"""
    
    summary_parts = []
    
    # Opening
    summary_parts.append(f"Here is the resume analysis for {candidate_name}.")
    
    # Experience
    if years_exp is not None:
        exp_text = f"We detected approximately {years_exp} years of relevant experience in their background."
        if required_exp:
            if years_exp >= required_exp:
                exp_text += f" This meets the requirement of {required_exp} years."
            else:
                exp_text += f" The position requires {required_exp} years, so there is a gap of {required_exp - years_exp} years."
        summary_parts.append(exp_text)
    
    # Matched skills
    if matched_skills:
        matched_list = ', '.join(sorted(matched_skills)[:6])
        summary_parts.append(f"Key matching skills include: {matched_list}.")
    
    # Missing skills
    if missing_skills:
        missing_list = ', '.join(sorted(missing_skills)[:5])
        summary_parts.append(f"Skills mentioned in the job description not found in the resume: {missing_list}.")
    
    # Overall verdict
    summary_parts.append(f"The candidate's overall compatibility score is {score} percent out of 100. {verdict_phrase}")
    
    return ' '.join(summary_parts)


# ============================================================================
# Routes
# ============================================================================
@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')


@app.route('/api/job-requirements', methods=['GET'])
def get_job_requirements():
    """Get list of all job requirements"""
    jobs = JobRequirement.query.order_by(JobRequirement.created_at.desc()).all()
=======
def extract_top_talents(resume_text, matched_skills, max_count=5):
    talents = []
    
    cert_pattern = r'(?:certification|certified|credential)[:\s]+([^,.\n]+)'
    certs = re.findall(cert_pattern, resume_text, re.IGNORECASE)
    talents.extend([c.strip().title() for c in certs[:2]])
    
    achievement_pattern = r'(?:award|achievement|recognized)[:\s]+([^,.\n]+)'
    achievements = re.findall(achievement_pattern, resume_text, re.IGNORECASE)
    talents.extend([a.strip().title() for a in achievements[:2]])
    
    talents.extend(sorted(matched_skills)[:5])
    talents = list(dict.fromkeys(talents))[:max_count]
    return talents if talents else ['Professional', 'Dedicated', 'Capable']


# ============================================================================
# API Routes - Job Management
# ============================================================================
@app.route('/api/jobs', methods=['GET'])
@login_required
def get_jobs():
    jobs = JobRequirement.query.filter_by(user_id=current_user.id).all()
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    return jsonify([{
        'id': j.id,
        'job_title': j.job_title,
        'company_name': j.company_name,
        'candidate_count': len(j.candidates),
<<<<<<< HEAD
=======
        'status': j.status,
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
        'created_at': j.created_at.isoformat()
    } for j in jobs])


<<<<<<< HEAD
@app.route('/api/job-requirements', methods=['POST'])
def create_job_requirement():
    """Create new job requirement"""
=======
@app.route('/api/jobs', methods=['POST'])
@login_required
def create_job():
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    data = request.get_json()
    
    if not data.get('job_title') or not data.get('description'):
        return jsonify({'error': 'Job title and description are required'}), 400
    
    job = JobRequirement(
<<<<<<< HEAD
        job_title=data['job_title'],
        company_name=data.get('company_name', 'Company'),
        description=data['description'],
        required_experience=data.get('required_experience')
=======
        user_id=current_user.id,
        job_title=data['job_title'],
        company_name=data.get('company_name', 'Company'),
        description=data['description'],
        required_experience=data.get('required_experience'),
        job_type=data.get('job_type'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        location=data.get('location'),
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'id': job.id,
        'job_title': job.job_title,
<<<<<<< HEAD
        'company_name': job.company_name
    }), 201


@app.route('/api/job-requirements/<int:job_id>', methods=['GET'])
def get_job_requirement(job_id):
    """Get specific job requirement with all candidates"""
    job = JobRequirement.query.get_or_404(job_id)
    
=======
        'message': 'Job created successfully'
    }), 201


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
@login_required
def get_job(job_id):
    job = JobRequirement.query.get_or_404(job_id)
    
    if job.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    candidates = [c.to_dict() for c in job.candidates]
    candidates_sorted = sorted(candidates, key=lambda x: x['overall_score'], reverse=True)
    
    return jsonify({
        'id': job.id,
        'job_title': job.job_title,
        'company_name': job.company_name,
        'description': job.description,
        'required_experience': job.required_experience,
<<<<<<< HEAD
=======
        'job_type': job.job_type,
        'salary_min': job.salary_min,
        'salary_max': job.salary_max,
        'location': job.location,
        'status': job.status,
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
        'created_at': job.created_at.isoformat(),
        'candidates': candidates_sorted,
        'candidate_count': len(candidates_sorted)
    })


<<<<<<< HEAD
@app.route('/api/candidates/upload', methods=['POST'])
def upload_resumes():
    """Bulk upload resumes and analyze against job requirements"""
    
=======
# ============================================================================
# API Routes - Resume Upload & Analysis
# ============================================================================
@app.route('/api/candidates/upload', methods=['POST'])
@login_required
def upload_resumes():
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    job_requirement_id = request.form.get('job_requirement_id')
    if not job_requirement_id:
        return jsonify({'error': 'Job requirement ID is required'}), 400
    
    job = JobRequirement.query.get_or_404(job_requirement_id)
<<<<<<< HEAD
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({'error': 'No files selected'}), 400
=======
    
    if job.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    files = request.files.getlist('files')
    
    if not files or len(files) > MAX_RESUMES_PER_UPLOAD:
        return jsonify({'error': f'Please upload 1-{MAX_RESUMES_PER_UPLOAD} files'}), 400
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    
    results = []
    errors = []
    
    for file in files:
        if not file or file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            errors.append(f"{file.filename}: Unsupported file type")
            continue
        
        try:
<<<<<<< HEAD
            # Save file
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            unique_filename = f"{timestamp}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path)
            
<<<<<<< HEAD
            # Extract text
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
            ext = filename.rsplit('.', 1)[1].lower()
            resume_text = extract_text(save_path, ext)
            resume_text_clean = clean_text(resume_text)
            
            if len(resume_text_clean) < 50:
                errors.append(f"{filename}: Could not extract sufficient text")
                os.remove(save_path)
                continue
            
<<<<<<< HEAD
            # Extract candidate info
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
            candidate_name = extract_name(resume_text)
            email = extract_email(resume_text)
            phone = extract_phone(resume_text)
            
<<<<<<< HEAD
            # Perform analysis
=======
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
            jd_text = clean_text(job.description)
            resume_skills = find_skills(resume_text_clean)
            jd_skills = find_skills(jd_text)
            
            matched_skills = resume_skills & jd_skills
            missing_skills = jd_skills - resume_skills
            
            years_exp = detect_years_experience(resume_text_clean)
            
            scores = calculate_scores(
                resume_text_clean, jd_text, resume_skills, jd_skills,
                years_exp, job.required_experience
            )
            
            overall_score = scores['overall']
            suitability, verdict_label, verdict_phrase = get_suitability_verdict(overall_score)
            
<<<<<<< HEAD
            # Extract talents
            talents = extract_top_talents(resume_text_clean, matched_skills)
            
            # Generate summary
            summary_text = generate_summary(
                candidate_name, overall_score, years_exp, job.required_experience,
                matched_skills, missing_skills, verdict_phrase
            )
            
            # Create candidate record
=======
            talents = extract_top_talents(resume_text_clean, matched_skills)
            
            summary_text = f"Candidate {candidate_name} has {years_exp or 'unknown'} years of experience. " \
                          f"Match score: {overall_score}%. {verdict_phrase}"
            
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
            candidate = Candidate(
                job_requirement_id=job.id,
                name=candidate_name,
                email=email,
                phone=phone,
                resume_filename=filename,
                resume_text=resume_text_clean,
                overall_score=overall_score,
                suitability=suitability,
                verdict_phrase=verdict_phrase,
                matched_skills=json.dumps(sorted(matched_skills)),
                missing_skills=json.dumps(sorted(missing_skills)),
                all_skills_found=json.dumps(sorted(resume_skills)),
                years_experience=years_exp,
                similarity_score=scores['similarity'],
                skill_match_score=scores['skill_match'],
                experience_match_score=scores['experience'],
                summary_text=summary_text,
                key_highlights=json.dumps(talents)
            )
            
            db.session.add(candidate)
            db.session.commit()
            
            results.append(candidate.to_dict())
<<<<<<< HEAD
            os.remove(save_path)  # Clean up temp file
            
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")
            continue
    
=======
            os.remove(save_path)
            
        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")
            continue
    
    job.total_applications = len(job.candidates)
    db.session.commit()
    
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    return jsonify({
        'success': len(results),
        'errors': errors,
        'candidates': sorted(results, key=lambda x: x['overall_score'], reverse=True)
    })


@app.route('/api/candidates/<int:candidate_id>', methods=['GET'])
<<<<<<< HEAD
def get_candidate(candidate_id):
    """Get detailed candidate information"""
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify(candidate.to_dict())


@app.route('/api/candidates/<int:candidate_id>/status', methods=['PATCH'])
def update_candidate_status(candidate_id):
    """Update candidate status (shortlisted, rejected, etc)"""
    candidate = Candidate.query.get_or_404(candidate_id)
=======
@login_required
def get_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if candidate.job_requirement.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = candidate.to_dict()
    logs = CommunicationLog.query.filter_by(candidate_id=candidate_id).all()
    data['communication_logs'] = [l.to_dict() for l in logs]
    
    return jsonify(data)


@app.route('/api/candidates/<int:candidate_id>/call-interview', methods=['POST'])
@login_required
def call_for_interview(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if candidate.job_requirement.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    interview_type = data.get('type', 'phone')
    
    subject = "Interview Opportunity"
    message = f"Dear {candidate.name},\n\nWe are pleased to invite you for an interview.\n\nBest regards"
    recipient = candidate.phone if interview_type == 'phone' else candidate.email
    
    if not recipient:
        return jsonify({'error': 'No contact information available'}), 400
    
    comm_log = CommunicationLog(
        candidate_id=candidate_id,
        communication_type=interview_type,
        subject=subject,
        message=message,
        recipient=recipient,
        status='sent'
    )
    
    candidate.interview_status = 'called'
    if interview_type == 'phone':
        candidate.call_sent = True
        candidate.call_sent_at = datetime.utcnow()
    else:
        candidate.email_sent = True
        candidate.email_sent_at = datetime.utcnow()
    
    db.session.add(comm_log)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Interview {interview_type} sent to {candidate.name}',
        'recipient': recipient
    })


@app.route('/api/candidates/<int:candidate_id>/status', methods=['PATCH'])
@login_required
def update_candidate_status(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if candidate.job_requirement.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    data = request.get_json()
    
    if 'status' in data:
        candidate.status = data['status']
<<<<<<< HEAD
        db.session.commit()
=======
    
    if 'interview_status' in data:
        candidate.interview_status = data['interview_status']
    
    db.session.commit()
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
    
    return jsonify(candidate.to_dict())


<<<<<<< HEAD
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'HR Resume Analyzer'})


# ============================================================================
# Error handlers
# ============================================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error'}), 500
=======
# ============================================================================
# Export Functionality
# ============================================================================
@app.route('/api/export/candidates/<int:job_id>', methods=['GET'])
@login_required
def export_candidates(job_id):
    job = JobRequirement.query.get_or_404(job_id)
    
    if job.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    export_format = request.args.get('format', 'csv')
    candidates = job.candidates
    
    if export_format == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Name', 'Email', 'Phone', 'Score', 'Suitability', 'Experience',
            'Matched Skills', 'Missing Skills', 'Status', 'Interview Status', 'Call Sent', 'Email Sent'
        ])
        
        # Data
        for candidate in candidates:
            writer.writerow([
                candidate.name,
                candidate.email or '',
                candidate.phone or '',
                candidate.overall_score,
                candidate.suitability,
                candidate.years_experience or '',
                ', '.join(json.loads(candidate.matched_skills or '[]')),
                ', '.join(json.loads(candidate.missing_skills or '[]')),
                candidate.status,
                candidate.interview_status,
                'Yes' if candidate.call_sent else 'No',
                'Yes' if candidate.email_sent else 'No',
            ])
        
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{job.job_title}_candidates_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    
    elif export_format == 'json':
        data = {
            'job': {
                'title': job.job_title,
                'company': job.company_name,
                'description': job.description,
                'created_at': job.created_at.isoformat(),
            },
            'candidates': [c.to_dict() for c in candidates]
        }
        
        return send_file(
            io.BytesIO(json.dumps(data, indent=2).encode()),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'{job.job_title}_candidates_{datetime.now().strftime("%Y%m%d")}.json'
        )
    
    return jsonify({'error': 'Invalid export format'}), 400


@app.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'GET':
        return jsonify(current_user.to_dict())
    
    data = request.get_json()
    current_user.full_name = data.get('full_name', current_user.full_name)
    current_user.company_name = data.get('company_name', current_user.company_name)
    current_user.phone = data.get('phone', current_user.phone)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Profile updated'})


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'service': 'HR Resume Analyzer Full-Stack'})
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
