"""
Database models for the HR Resume Analyzer
Stores candidate info, analysis results, and job requirements
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class JobRequirement(db.Model):
    """Stores job description and company requirements"""
    __tablename__ = 'job_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text)  # JSON string
    required_experience = db.Column(db.Integer)  # years
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    candidates = db.relationship('Candidate', backref='job_requirement', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<JobRequirement {self.job_title} at {self.company_name}>"


class Candidate(db.Model):
    """Stores candidate information and analysis results"""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    job_requirement_id = db.Column(db.Integer, db.ForeignKey('job_requirements.id'), nullable=False)
    
    # Resume info
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    resume_filename = db.Column(db.String(255))
    resume_text = db.Column(db.Text)  # Full extracted resume text
    
    # Analysis results
    overall_score = db.Column(db.Float)  # 0-100
    suitability = db.Column(db.String(50))  # "Excellent", "Good", "Fair", "Poor"
    verdict_phrase = db.Column(db.String(500))
    
    # Skill analysis
    matched_skills = db.Column(db.Text)  # JSON array
    missing_skills = db.Column(db.Text)  # JSON array
    all_skills_found = db.Column(db.Text)  # JSON array - all skills detected
    
    # Experience
    years_experience = db.Column(db.Integer)
    
    # Scoring breakdown
    similarity_score = db.Column(db.Float)  # Text similarity
    skill_match_score = db.Column(db.Float)  # Skill match %
    experience_match_score = db.Column(db.Float)  # Experience match %
    
    # Summary and voice content
    summary_text = db.Column(db.Text)  # Full AI summary for narration
    key_highlights = db.Column(db.Text)  # JSON array - top 5 talents/skills
    
    # Meta
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='analyzed')  # analyzed, reviewed, rejected, shortlisted
    
    def __repr__(self):
        return f"<Candidate {self.name} - {self.overall_score}%>"
    
    def to_dict(self):
        """Serialize candidate to dict for JSON response"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'overall_score': self.overall_score,
            'suitability': self.suitability,
            'verdict_phrase': self.verdict_phrase,
            'matched_skills': json.loads(self.matched_skills or '[]'),
            'missing_skills': json.loads(self.missing_skills or '[]'),
            'all_skills_found': json.loads(self.all_skills_found or '[]'),
            'years_experience': self.years_experience,
            'similarity_score': self.similarity_score,
            'skill_match_score': self.skill_match_score,
            'experience_match_score': self.experience_match_score,
            'summary_text': self.summary_text,
            'key_highlights': json.loads(self.key_highlights or '[]'),
            'status': self.status,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None
        }
