"""
Full-Stack HR Resume Analyzer - Database Models
Includes user authentication, job management, and candidate tracking
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # Profile info
    full_name = db.Column(db.String(150))
    company_name = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='HR')  # HR, Manager, Admin
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    jobs = db.relationship('JobRequirement', backref='creator', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'company_name': self.company_name,
            'role': self.role,
        }


class JobRequirement(db.Model):
    """Job opening model"""
    __tablename__ = 'job_requirements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    job_title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.Text)
    required_experience = db.Column(db.Integer)
    
    # Job metadata
    status = db.Column(db.String(50), default='active')  # active, closed, on-hold
    job_type = db.Column(db.String(50))  # Full-time, Part-time, Contract
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(200))
    
    best_candidate_id = db.Column(db.Integer)
    total_applications = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidates = db.relationship('Candidate', backref='job_requirement', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<JobRequirement {self.job_title}>"


class Candidate(db.Model):
    """Candidate resume data and analysis"""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    job_requirement_id = db.Column(db.Integer, db.ForeignKey('job_requirements.id'), nullable=False)
    
    # Resume info
    name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(200), index=True)
    phone = db.Column(db.String(20))
    resume_filename = db.Column(db.String(255))
    resume_text = db.Column(db.Text)
    
    # Analysis results
    overall_score = db.Column(db.Float)
    suitability = db.Column(db.String(50))
    verdict_phrase = db.Column(db.String(500))
    
    # Skill analysis
    matched_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    all_skills_found = db.Column(db.Text)
    
    # Experience
    years_experience = db.Column(db.Integer)
    
    # Scoring breakdown
    similarity_score = db.Column(db.Float)
    skill_match_score = db.Column(db.Float)
    experience_match_score = db.Column(db.Float)
    
    # Summary
    summary_text = db.Column(db.Text)
    key_highlights = db.Column(db.Text)
    
    # Best candidate prediction
    is_best_candidate = db.Column(db.Boolean, default=False)
    best_candidate_rank = db.Column(db.Integer)
    
    # Interview tracking
    interview_status = db.Column(db.String(50), default='none')
    interview_date = db.Column(db.DateTime)
    interview_notes = db.Column(db.Text)
    
    # Communication
    call_sent = db.Column(db.Boolean, default=False)
    call_sent_at = db.Column(db.DateTime)
    email_sent = db.Column(db.Boolean, default=False)
    email_sent_at = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(50), default='analyzed')
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    communication_logs = db.relationship('CommunicationLog', backref='candidate', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<Candidate {self.name}>"
    
    def to_dict(self):
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
            'is_best_candidate': self.is_best_candidate,
            'best_candidate_rank': self.best_candidate_rank,
            'status': self.status,
            'interview_status': self.interview_status,
            'call_sent': self.call_sent,
            'email_sent': self.email_sent,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None
        }


class CommunicationLog(db.Model):
    """Communication history"""
    __tablename__ = 'communication_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    
    communication_type = db.Column(db.String(50))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    recipient = db.Column(db.String(200))
    
    status = db.Column(db.String(50))
    response_received = db.Column(db.Boolean, default=False)
    response_text = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_for = db.Column(db.DateTime)
    
    def __repr__(self):
        return f"<CommunicationLog {self.communication_type}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'communication_type': self.communication_type,
            'subject': self.subject,
            'message': self.message,
            'recipient': self.recipient,
            'status': self.status,
            'response_received': self.response_received,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
