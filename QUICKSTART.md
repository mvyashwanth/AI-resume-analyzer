# 🚀 Quick Start Guide - HR Resume Analyzer

Get the HR Resume Analyzer running in 5 minutes!

## 1️⃣ Install Dependencies

```bash
# Navigate to project directory
cd resume_analyzer_hr

# Install required packages
pip install -r requirements.txt
```

**On Windows?** Use `pip` directly without `sudo`:
```bash
pip install -r requirements.txt
```

## 2️⃣ Start the Application

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

## 3️⃣ Open in Browser

Click the link or navigate to:
```
http://127.0.0.1:5000
```

## 4️⃣ Test with Sample Data

### Using Sample Resumes:
1. Click **"+ New Job Opening"**
2. Fill in the form with:
   - **Job Title**: "Senior Full-Stack Engineer"
   - **Company Name**: "Tech Corp"
   - **Years of Experience**: 5
   - **Job Description**: Copy-paste content from `sample_data/SAMPLE_JOB_DESCRIPTION.txt`
3. Click **"Create Job Opening"**
4. Click **"Upload & Analyze"**
5. Select files from `sample_data/` folder:
   - `sample_resume_1.txt` (John Smith)
   - `sample_resume_2.txt` (Sarah Johnson)
6. Click **"Upload & Analyze"**

### View Results:
- ✅ Both candidates will be ranked and analyzed
- 🎙️ Click any candidate → Click **"🔊 Play Summary"** to hear voice narration
- ⭐ Try marking candidates as shortlisted/reviewed

## 📁 Project Files

```
resume_analyzer_hr/
├── app.py                     ← Main application (run this)
├── models.py                  ← Database models
├── requirements.txt           ← Dependencies
├── README.md                  ← Full documentation
├── QUICKSTART.md             ← This file
├── templates/
│   └── index.html            ← Web interface
├── static/
│   ├── css/style.css         ← Styling
│   └── js/script.js          ← JavaScript functionality
├── uploads/                   ← Temporary resume storage
├── instance/                  ← Database location
└── sample_data/              ← Test files
    ├── sample_resume_1.txt
    ├── sample_resume_2.txt
    └── SAMPLE_JOB_DESCRIPTION.txt
```

## ⚡ Key Features to Try

### 🧠 AI Analysis
- Upload multiple resumes
- Watch real-time skill matching
- View candidate rankings by fit %

### 🔊 Voice Narration
- Click any candidate
- Click "🔊 Play Summary" button
- Listen to AI-generated candidate summary
- Voice uses browser's native Web Speech API (no API keys needed)

### 📊 Scoring Breakdown
- See text similarity %
- Check skill match score
- View experience alignment

### ⭐ Candidate Management
- Mark candidates as shortlisted
- Track review status
- Reject unsuitable candidates

## 🛑 Troubleshooting

### Port Already in Use?
If port 5000 is busy, change it in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Voice Not Working?
- Try Chrome, Firefox, or Safari (best voice support)
- Check if system volume is muted
- Some sites require HTTPS for voice (use Chrome for local testing)

### Database Issues?
The app creates database automatically on first run:
```bash
instance/resume_analyzer.db  # Created automatically
```

To reset, delete this file and restart:
```bash
rm instance/resume_analyzer.db
python app.py
```

### Dependencies Not Installing?
Try upgrading pip first:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 📚 Next Steps

1. **Read Full Documentation**: Check `README.md` for detailed info
2. **Customize Skills**: Add your company's specific skills in `app.py`
3. **Upload Real Resumes**: Test with actual applications
4. **Deploy**: See README.md for production deployment options

## 💡 Tips

- **Better Job Descriptions** = Better Matching
  - Be specific about required skills
  - Include both technical and soft requirements
  - Mention tools/platforms explicitly

- **Resume Quality** Matters
  - Text-based PDFs work best (not scanned images)
  - Clear formatting helps skill extraction
  - Include all relevant experience

- **Customize Skill Library**
  - Edit `SKILL_LIBRARY` in `app.py`
  - Add your industry-specific skills
  - Restart app to apply changes

## 🎓 Understanding Scores

- **80-100%**: Excellent Match ⭐⭐⭐⭐⭐
- **65-79%**: Good Match ⭐⭐⭐⭐
- **50-64%**: Fair Match ⭐⭐⭐
- **35-49%**: Weak Match ⭐⭐
- **0-34%**: Poor Match ⭐

Score is calculated from:
- 40% Text similarity to job description
- 45% Skill match percentage
- 15% Experience alignment

---

**🎉 That's it! You're ready to start screening resumes with AI.**

For more details, check README.md or run the app and explore!
