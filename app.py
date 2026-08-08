"""
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
"""

import os
import re
import json
from datetime import datetime
from functools import wraps

from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import PyPDF2
import docx2txt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models import db, JobRequirement, Candidate

# ============================================================================
# Flask App Setup
# ============================================================================
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "resume_analyzer.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

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
    'machine learning', 'deep learning', 'nlp', 'natural language processing',
    'computer vision', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
    'pandas', 'numpy', 'data analysis', 'data science', 'data engineering',
    'big data', 'artificial intelligence', 'ai', 'llm', 'generative ai',
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
# ============================================================================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    return ''


def clean_text(text):
    """Normalize and clean text"""
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ============================================================================
# Analysis Functions
# ============================================================================
def extract_email(text):
    """Find email address in text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_phone(text):
    """Find phone number in text"""
    pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?(?:\d{3})\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(pattern, text)
    return match.group(0) if match else None


def extract_name(text):
    """Intelligently guess candidate name from first lines"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    for line in lines[:10]:
        words = line.split()
        if 1 < len(words) <= 5 and all(w[0:1].isalpha() for w in words):
            if not any(k in line.lower() for k in ['resume', 'curriculum', 'cv', '@', 'http', 'mailto']):
                return line.title()
    return 'Candidate'


def find_skills(text, library=SKILL_LIBRARY):
    """Find all recognized skills in text (case-insensitive)"""
    text_lower = text.lower()
    found = set()
    for skill in library:
        pattern = r'(?<![a-zA-Z0-9])\b' + re.escape(skill.lower()) + r'\b(?![a-zA-Z0-9])'
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def detect_years_experience(text):
    """Extract years of experience from text"""
    matches = re.findall(r'(\d+)\+?\s*(?:-\s*\d+\s*)?years?', text.lower())
    years = [int(m) for m in matches if 0 < int(m) < 70]
    return max(years) if years else None


def tfidf_similarity(resume_text, jd_text):
    """Compute TF-IDF cosine similarity between resume and job description"""
    try:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except (ValueError, IndexError):
        return 0.0


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
    if jd_skills:
        matched = resume_skills & jd_skills
        skill_match = len(matched) / len(jd_skills)
        skill_match_score = round(skill_match * 100, 1)
    else:
        skill_match_score = 50.0
    
    # Experience matching (15%)
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
    
    # Weighted overall score
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
    """Convert score to suitability level and phrase"""
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
    return jsonify([{
        'id': j.id,
        'job_title': j.job_title,
        'company_name': j.company_name,
        'candidate_count': len(j.candidates),
        'created_at': j.created_at.isoformat()
    } for j in jobs])


@app.route('/api/job-requirements', methods=['POST'])
def create_job_requirement():
    """Create new job requirement"""
    data = request.get_json()
    
    if not data.get('job_title') or not data.get('description'):
        return jsonify({'error': 'Job title and description are required'}), 400
    
    job = JobRequirement(
        job_title=data['job_title'],
        company_name=data.get('company_name', 'Company'),
        description=data['description'],
        required_experience=data.get('required_experience')
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'id': job.id,
        'job_title': job.job_title,
        'company_name': job.company_name
    }), 201


@app.route('/api/job-requirements/<int:job_id>', methods=['GET'])
def get_job_requirement(job_id):
    """Get specific job requirement with all candidates"""
    job = JobRequirement.query.get_or_404(job_id)
    
    candidates = [c.to_dict() for c in job.candidates]
    candidates_sorted = sorted(candidates, key=lambda x: x['overall_score'], reverse=True)
    
    return jsonify({
        'id': job.id,
        'job_title': job.job_title,
        'company_name': job.company_name,
        'description': job.description,
        'required_experience': job.required_experience,
        'created_at': job.created_at.isoformat(),
        'candidates': candidates_sorted,
        'candidate_count': len(candidates_sorted)
    })


@app.route('/api/candidates/upload', methods=['POST'])
def upload_resumes():
    """Bulk upload resumes and analyze against job requirements"""
    
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    job_requirement_id = request.form.get('job_requirement_id')
    if not job_requirement_id:
        return jsonify({'error': 'Job requirement ID is required'}), 400
    
    job = JobRequirement.query.get_or_404(job_requirement_id)
    files = request.files.getlist('files')
    
    if not files:
        return jsonify({'error': 'No files selected'}), 400
    
    results = []
    errors = []
    
    for file in files:
        if not file or file.filename == '':
            continue
        
        if not allowed_file(file.filename):
            errors.append(f"{file.filename}: Unsupported file type")
            continue
        
        try:
            # Save file
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            unique_filename = f"{timestamp}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path)
            
            # Extract text
            ext = filename.rsplit('.', 1)[1].lower()
            resume_text = extract_text(save_path, ext)
            resume_text_clean = clean_text(resume_text)
            
            if len(resume_text_clean) < 50:
                errors.append(f"{filename}: Could not extract sufficient text")
                os.remove(save_path)
                continue
            
            # Extract candidate info
            candidate_name = extract_name(resume_text)
            email = extract_email(resume_text)
            phone = extract_phone(resume_text)
            
            # Perform analysis
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
            
            # Extract talents
            talents = extract_top_talents(resume_text_clean, matched_skills)
            
            # Generate summary
            summary_text = generate_summary(
                candidate_name, overall_score, years_exp, job.required_experience,
                matched_skills, missing_skills, verdict_phrase
            )
            
            # Create candidate record
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
            os.remove(save_path)  # Clean up temp file
            
        except Exception as e:
            errors.append(f"{filename}: {str(e)}")
            continue
    
    return jsonify({
        'success': len(results),
        'errors': errors,
        'candidates': sorted(results, key=lambda x: x['overall_score'], reverse=True)
    })


@app.route('/api/candidates/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get detailed candidate information"""
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify(candidate.to_dict())


@app.route('/api/candidates/<int:candidate_id>/status', methods=['PATCH'])
def update_candidate_status(candidate_id):
    """Update candidate status (shortlisted, rejected, etc)"""
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()
    
    if 'status' in data:
        candidate.status = data['status']
        db.session.commit()
    
    return jsonify(candidate.to_dict())


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


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
