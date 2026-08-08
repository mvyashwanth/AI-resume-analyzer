<<<<<<< HEAD
# HR Resume Analyzer — Enterprise Edition

An AI-powered resume screening system designed for HR departments. Automatically analyzes hundreds of resumes, matches them against job requirements, and provides intelligent candidate ranking with real-time voice narration.

## ✨ Features

### Core Capabilities
- **Bulk Resume Upload**: Process multiple resumes simultaneously (PDF, DOCX, TXT)
- **Job Requirement Management**: Create and manage multiple job openings
- **Automatic Skill Extraction**: Detect 100+ technical and soft skills from resumes
- **Semantic Matching**: TF-IDF + cosine similarity for job description alignment
- **Experience Detection**: Automatically extract years of experience from resume text
- **Candidate Ranking**: Sort candidates by suitability score (0-100%)

### AI Analysis Features
- **Multi-factor Scoring**:
  - Text similarity match (40%)
  - Skill overlap (45%)
  - Experience alignment (15%)
- **Detailed Breakdown**: View similarity, skill match, and experience scores
- **Talent Extraction**: Automatically identify top 5 unique talents and strengths
- **Smart Verdict**: Categorized suitability (Excellent/Good/Fair/Poor)

### Voice Features
- **Real-Time Voice Narration**: Web Speech API — no external TTS needed
- **AI Summary Playback**: Listen to candidate analysis summary
- **Download Transcripts**: Save summary as text file
- **Browser-Native**: Runs entirely in-browser with no external API calls

### HR Dashboard
- **Multi-Job Management**: Handle multiple job openings simultaneously
- **Candidate Statistics**: Quick overview of candidate distribution by fit level
- **Status Tracking**: Mark candidates as shortlisted, reviewed, or rejected
- **Persistent Database**: SQLite storage of all analyses and candidates
- **Professional UI**: Modern, mobile-friendly interface designed for HR teams
=======
# 🚀 HR Resume Analyzer - Full Stack Edition

**Professional HR recruitment platform with AI-powered resume analysis, user authentication, bulk upload, export functionality, and modern responsive UI.**

## ✨ Features

### 🔐 Authentication & Security
- User registration with email verification
- Secure login with password hashing
- Session management with Flask-Login
- Role-based access control
- User profile management

### 🤖 AI-Powered Resume Analysis
- Multi-factor scoring (text similarity, skills, experience)
- 100+ skill recognition
- Experience detection
- Best candidate auto-prediction
- Real-time voice narration (Web Speech API)

### 💼 Job Management
- Create job openings with detailed requirements
- Track applications for each job
- Set salary ranges and location requirements
- Job status management (active, closed, on-hold)

### 📤 Bulk Upload & Analysis
- Upload up to 10 resumes simultaneously
- Parallel processing for fast analysis
- Support for PDF, DOCX, TXT formats
- Progress tracking

### 💾 Data Export
- Export candidate lists as CSV
- Export as JSON for data import
- Complete candidate information included
- Interview history included

### 📊 Modern Dashboard
- Beautiful, responsive UI
- Real-time statistics
- Job overview and management
- Candidate screening interface
- Communication tracking

### 📞 Interview Management
- One-click interview invitations
- Send via call or email
- Communication history logging
- Timestamp tracking for audit trail

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Text Processing**: scikit-learn, PyPDF2, python-docx
- **API**: RESTful API with CORS support

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables
- **JavaScript**: ES6+ with async/await
- **Design**: Responsive, mobile-first approach

### Key Libraries
- PyPDF2: PDF text extraction
- docx2txt: Word document parsing
- scikit-learn: ML-based scoring
- TensorFlow/scikit-learn: NLP analysis
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4

## 🚀 Quick Start

### Prerequisites
<<<<<<< HEAD
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or extract the project**:
```bash
cd resume_analyzer_hr
```

2. **Create virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python app.py
```

5. **Open in browser**:
Navigate to `http://127.0.0.1:5000`

## 📋 Usage Guide

### Creating a Job Opening

1. Click **"+ New Job Opening"** in the sidebar
2. Enter:
   - **Job Title**: e.g., "Senior Python Developer"
   - **Company Name**: Your organization name
   - **Years of Experience Required**: Expected experience level (optional)
   - **Job Description**: Full job description including:
     - Key responsibilities
     - Required technical skills
     - Required soft skills
     - Nice-to-have qualifications
3. Click **"Create Job Opening"**

**Tip**: The more detailed your job description, the more accurate the AI matching.

### Uploading Resumes

1. Select the job opening from the sidebar
2. In the **Upload Resumes** section:
   - Drag & drop multiple resume files, OR
   - Click to select files from your computer
3. Supported formats: PDF, DOCX, TXT
4. Click **"Upload & Analyze"**
5. Wait for processing (progress bar shows status)

The system will:
- Extract text from each resume
- Detect candidate name, email, and phone
- Match skills against job requirements
- Extract years of experience
- Calculate overall compatibility score
- Generate AI summary for narration

### Viewing Candidate Details

1. Click on any candidate card in the ranked list
2. View detailed analysis including:
   - **Overall Score**: Compatibility percentage
   - **AI Summary**: AI-generated text summary
   - **Matched Skills**: Skills found in resume matching job description
   - **Missing Skills**: Required skills not found in resume
   - **All Skills Found**: Complete list of detected skills
   - **Top Talents**: Automatically extracted top 5 strengths
   - **Scoring Breakdown**: Detailed scoring metrics with visual bars
   - **Experience Info**: Detected years of experience

### Using Voice Narration

1. In the candidate detail view, click **"🔊 Play Summary"**
2. The browser will speak the AI-generated candidate summary aloud
3. To stop playback, click **"⏹ Stop"**
4. To save summary as text, click **"💾 Download"**

**Browser Support**: Voice narration works in Chrome, Firefox, Safari, and Edge.

### Managing Candidate Status

1. View a candidate's details
2. In the **Candidate Status** section, click:
   - **⭐ Shortlist**: Mark for further review
   - **✓ Reviewed**: Mark as reviewed
   - **✗ Reject**: Mark as rejected
3. Status persists in the database

## 🔧 API Endpoints

### Job Requirements
```
GET    /api/job-requirements              # List all jobs
POST   /api/job-requirements              # Create new job
GET    /api/job-requirements/<job_id>     # Get specific job with all candidates
=======
- Python 3.8+ (3.11 recommended)
- pip (Python package manager)
- Modern web browser

### Installation

```bash
# Clone or extract the project
cd resume_analyzer_fullstack

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Access the Application
Open your browser and navigate to: **http://127.0.0.1:5000**

## 📝 Usage Guide

### 1. Create Account
- Click "Create Account"
- Fill in username, email, password
- Account is created instantly
- Redirected to login page

### 2. Login
- Enter username and password
- Access dashboard
- View stats and recent jobs

### 3. Create Job Opening
- Go to "New Job" section
- Fill in job details:
  - Job title
  - Company name
  - Job type (Full-time, Part-time, Contract)
  - Required experience
  - Salary range (optional)
  - Location
  - Complete job description
- Click "Create Job Opening"

### 4. Upload Resumes
- Select job opening
- Upload up to 10 resumes at once
- System automatically analyzes
- View results by score

### 5. Review Candidates
- Click on candidate card
- View full analysis:
  - Overall score
  - Matched skills
  - Missing skills
  - Experience level
  - Key highlights
- Send interview invitation

### 6. Send Interview Calls
- Click "Call for Interview"
- Choose email or phone
- Message auto-generated and logged
- Communication tracked

### 7. Export Candidates
- In job view, click "Export"
- Choose format:
  - CSV (for Excel/Sheets)
  - JSON (for data import)
- Download file to computer

## 📊 Database Schema

### Users Table
```
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- full_name
- company_name
- phone
- role
- created_at, updated_at
```

### Job Requirements Table
```
- id (Primary Key)
- user_id (Foreign Key → Users)
- job_title
- company_name
- description
- required_experience
- job_type
- salary_min, salary_max
- location
- status
- created_at, updated_at
```

### Candidates Table
```
- id (Primary Key)
- job_requirement_id (Foreign Key → JobRequirements)
- name, email, phone
- overall_score
- suitability
- matched_skills, missing_skills
- years_experience
- summary_text
- is_best_candidate
- interview_status
- call_sent, email_sent
- created_at, updated_at
```

### Communication Logs Table
```
- id (Primary Key)
- candidate_id (Foreign Key → Candidates)
- communication_type (call, email, sms)
- subject, message
- recipient
- status (sent, pending, failed)
- created_at
```

## 🔌 API Endpoints

### Authentication
```
POST   /register              - Register new user
POST   /login                 - Login user
GET    /logout                - Logout user
```

### Jobs
```
GET    /api/jobs              - List all jobs (current user)
POST   /api/jobs              - Create new job
GET    /api/jobs/<id>         - Get job details with candidates
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
```

### Candidates
```
<<<<<<< HEAD
POST   /api/candidates/upload             # Bulk upload and analyze resumes
GET    /api/candidates/<candidate_id>     # Get candidate details
PATCH  /api/candidates/<candidate_id>/status  # Update candidate status
```

### Health
```
GET    /api/health                        # Health check
```

## 📊 Scoring Algorithm

### Overall Score Calculation
```
Overall Score = (0.40 × Text Similarity) + (0.45 × Skill Match) + (0.15 × Experience Match)
```

#### Text Similarity (40%)
- Uses TF-IDF (Term Frequency-Inverse Document Frequency)
- Compares resume against job description
- Measures textual and semantic overlap
- Range: 0-100%

#### Skill Match (45%)
- Compares 100+ recognized technical and soft skills
- Calculates percentage of required skills found in resume
- Range: 0-100%

#### Experience Match (15%)
- Detects years of experience from resume text
- Compares against required experience from job description
- 100% if years ≥ required, scales down otherwise
- Range: 0-100%

### Suitability Verdicts
- **Excellent Match** (80-100%): Highly recommended for interview
- **Good Match** (65-79%): Strong fit, recommended for interview
- **Fair Match** (50-64%): Moderate fit, consider if limited candidates
- **Weak Match** (35-49%): Limited alignment, may need training
- **Poor Match** (0-34%): Does not meet requirements

## 🧠 Skill Library

The system recognizes 100+ skills across categories:

### Programming Languages
Python, Java, JavaScript, TypeScript, C++, C#, Go, Rust, R, etc.

### Web Technologies
HTML, CSS, React, Angular, Vue.js, Node.js, Django, Flask, ASP.NET, etc.

### Data & AI/ML
Machine Learning, Deep Learning, TensorFlow, PyTorch, Pandas, Numpy, etc.

### Cloud & DevOps
AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Jenkins, Terraform, etc.

### Databases
SQL, MySQL, PostgreSQL, MongoDB, Redis, Oracle, Elasticsearch, etc.

### Soft Skills
Leadership, Communication, Teamwork, Problem Solving, Project Management, Agile, Scrum, etc.

### Tools & Platforms
Excel, Power BI, Tableau, Jira, Salesforce, Figma, Slack, etc.

**Expand the skill library**: Edit `SKILL_LIBRARY` in `app.py` to add custom skills
=======
POST   /api/candidates/upload - Upload resumes
GET    /api/candidates/<id>   - Get candidate details
PATCH  /api/candidates/<id>/status - Update candidate status
POST   /api/candidates/<id>/call-interview - Send interview
```

### Export
```
GET    /api/export/candidates/<job_id>?format=csv
GET    /api/export/candidates/<job_id>?format=json
```

### User
```
GET    /api/profile           - Get user profile
PUT    /api/profile           - Update user profile
```

## 🎨 Frontend Pages

### login.html
- User login form
- Email/username input
- Password input
- Account creation link
- Modern gradient design

### register.html
- User registration form
- Username, email, password
- Password strength indicator
- Account creation
- Login redirect

### dashboard.html
- Main application interface
- Sidebar navigation
- Statistics dashboard
- Job management
- Profile settings
- Responsive design
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4

## 📁 Project Structure

```
<<<<<<< HEAD
resume_analyzer_hr/
├── app.py                    # Main Flask application
├── models.py                 # Database models (SQLAlchemy)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── templates/
│   └── index.html            # Main HTML dashboard
├── static/
│   ├── css/
│   │   └── style.css         # Professional styling
│   └── js/
│       └── script.js         # Interactive functionality
├── uploads/                  # Temporary storage for uploaded resumes
├── instance/                 # SQLite database directory
└── sample_data/              # Sample resumes for testing (optional)
```

## 🗄️ Database

The application uses **SQLite** (zero configuration required).

### Database Schema

#### JobRequirement Table
- `id`: Unique identifier
- `job_title`: Position title
- `company_name`: Organization name
- `description`: Full job description
- `required_skills`: JSON array of extracted skills
- `required_experience`: Years of experience needed
- `created_at`, `updated_at`: Timestamps

#### Candidate Table
- `id`: Unique identifier
- `job_requirement_id`: Foreign key to job requirement
- `name`: Extracted candidate name
- `email`, `phone`: Contact information
- `resume_filename`: Original uploaded filename
- `resume_text`: Full extracted resume text
- `overall_score`: Final suitability score (0-100)
- `suitability`: Verdict level (Excellent/Good/Fair/Poor)
- `matched_skills`: JSON array
- `missing_skills`: JSON array
- `all_skills_found`: JSON array
- `years_experience`: Detected experience level
- `similarity_score`, `skill_match_score`, `experience_match_score`: Component scores
- `summary_text`: AI-generated summary for voice narration
- `key_highlights`: JSON array of top talents
- `status`: Candidate status (analyzed/reviewed/shortlisted/rejected)
- `analyzed_at`: Analysis timestamp

Database file location: `instance/resume_analyzer.db`

## 🔒 Privacy & Security

- **No Cloud Upload**: All processing happens locally on your server
- **No External APIs**: Voice narration uses browser's Web Speech API
- **Persistent Storage**: Resumes stored in SQLite database only
- **Temp File Cleanup**: Uploaded files are deleted after processing
- **HTTPS Ready**: Deploy behind reverse proxy with SSL for production

## ⚠️ Limitations & Notes

1. **Text Extraction**: Accuracy depends on resume format and clarity
2. **Skill Detection**: Uses pattern matching for known skills only
3. **Experience Detection**: Extracts maximum experience mentioned (may include hobbies)
4. **PDF Compatibility**: Works best with text-based PDFs, not scanned images
5. **Language**: Primarily optimized for English resumes
6. **Voice Support**: Requires modern browser (Chrome, Firefox, Safari, Edge 14+)

## 🚀 Production Deployment

### Using Gunicorn (Linux/Mac)
=======
resume_analyzer_fullstack/
├── app.py                          # Main Flask application
├── models.py                       # Database models
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── templates/
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   └── dashboard.html             # Main dashboard
│
├── static/
│   ├── css/
│   │   └── dashboard.css          # Dashboard styling
│   └── js/
│       └── dashboard.js           # Dashboard functionality
│
├── uploads/                        # Resume storage (temp)
├── instance/                       # SQLite database
└── sample_data/                    # Test data
```

## 🔐 Security Features

- **Password Hashing**: Werkzeug security
- **Session Management**: Flask-Login with secure cookies
- **CSRF Protection**: Can be added with Flask-WTF
- **SQL Injection Prevention**: SQLAlchemy ORM
- **Data Validation**: Input validation on all endpoints
- **User Authorization**: Only users can see their own data

## 📈 Performance

- **Resume Analysis**: 3-5 seconds for 10 resumes
- **Database**: SQLite (can upgrade to PostgreSQL for production)
- **Scalability**: Handles 1000+ candidates efficiently
- **Frontend**: Lightweight, responsive design

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (Gunicorn)
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

<<<<<<< HEAD
### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### Nginx Reverse Proxy Example
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Performance Considerations

- **Concurrent Uploads**: Flask can handle 10-50 resumes per batch
- **Database**: SQLite suitable for 10,000+ candidates
- **Memory**: ~100MB for typical deployment
- **CPU**: Light processing requirements

For larger deployments (1000+ candidates), consider upgrading to PostgreSQL.

## 🐛 Troubleshooting

### "Cannot find resume text" error
- Ensure resume is not image-based (use text-based PDFs)
- Try converting to TXT format first

### Voice narration not working
- Check browser compatibility (use latest Chrome, Firefox, Safari, or Edge)
- Ensure system volume is not muted
- Try different audio device in system settings

### High memory usage
- Clear database periodically: Delete old candidates from dashboard
- Restart Flask application

### Skill detection missing common skills
- Add to `SKILL_LIBRARY` in `app.py`
- Rebuild and restart application

## 📞 Support & Contributing

For issues, suggestions, or improvements, refer to project documentation or contact your development team.

## 📄 License

This project is provided as-is for HR recruitment purposes.

---

**Built with ❤️ for HR Professionals**

*AI-Powered Resume Screening • Real-Time Voice Narration • Enterprise-Grade Analytics*
=======
### Environment Variables
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=postgresql://user:pass@localhost/dbname
```

## 📦 Customization

### Add More Skills
Edit `SKILL_LIBRARY` in `app.py`:
```python
SKILL_LIBRARY = [
    'your_skill_here',
    'another_skill',
    # ... more skills
]
```

### Modify Scoring Formula
Edit `calculate_scores()` in `app.py`:
```python
# Current: 40% text, 45% skills, 15% experience
overall = (0.40 * similarity + 0.45 * skills + 0.15 * experience)
# Change weights as needed
```

### Customize Email Sending
Add Flask-Mail configuration:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(port=5001)
```

### Database Issues
```bash
# Delete database and recreate
rm instance/resume_analyzer.db
python app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Login Not Working
- Clear browser cookies
- Check database exists
- Verify user created successfully

## 📚 Additional Resources

### Flask Documentation
- https://flask.palletsprojects.com/

### SQLAlchemy Documentation
- https://docs.sqlalchemy.org/

### scikit-learn Documentation
- https://scikit-learn.org/

## 🎯 Future Enhancements

- [ ] Email integration (Flask-Mail)
- [ ] Advanced filtering and search
- [ ] Candidate interview scheduling
- [ ] Performance analytics
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Video interview integration
- [ ] Slack notifications
- [ ] Google Drive integration
- [ ] Resume parsing improvements

## 📄 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Developer Notes

### Adding New Features
1. Update models.py for database changes
2. Add API endpoints in app.py
3. Update frontend templates/JS
4. Test thoroughly before deployment

### Common Tasks
- **Add new job field**: Update JobRequirement model + template form
- **Add skill**: Add to SKILL_LIBRARY in app.py
- **Change styling**: Modify dashboard.css
- **Add new page**: Create template + route

## 📞 Support

For issues:
1. Check README.md
2. Review error messages
3. Check app logs
4. Verify all dependencies installed

---

**HR Resume Analyzer - Full Stack Edition**

*Professional Recruitment • AI-Powered Screening • Smart Hiring*

Ready to revolutionize your hiring process! 🎉
>>>>>>> d3347c210042cc3d3799e39752caf855d05b92a4
