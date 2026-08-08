/**
 * HR Resume Analyzer - Main JavaScript
 * Handles UI interactions, API calls, and Web Speech API voice synthesis
 */

// ============================================================================
// STATE MANAGEMENT
// ============================================================================
const state = {
    jobs: [],
    currentJobId: null,
    candidates: [],
    currentCandidate: null,
    isSpeaking: false,
    selectedFiles: [],
};

// ============================================================================
// DOM ELEMENTS
// ============================================================================
const elements = {
    // Sidebar
    jobList: document.getElementById('jobList'),
    newJobBtn: document.getElementById('newJobBtn'),

    // Views
    newJobView: document.getElementById('newJobView'),
    jobDashboardView: document.getElementById('jobDashboardView'),
    candidateDetailView: document.getElementById('candidateDetailView'),

    // Forms
    jobForm: document.getElementById('jobForm'),
    cancelJobBtn: document.getElementById('cancelJobBtn'),

    // Job Dashboard
    currentJobTitle: document.getElementById('currentJobTitle'),
    currentCompanyName: document.getElementById('currentCompanyName'),
    totalCandidates: document.getElementById('totalCandidates'),
    excellentCount: document.getElementById('excellentCount'),
    goodCount: document.getElementById('goodCount'),

    // Upload
    dropzone: document.getElementById('dropzone'),
    resumeFileInput: document.getElementById('resumeFileInput'),
    uploadBtn: document.getElementById('uploadBtn'),
    uploadProgress: document.getElementById('uploadProgress'),
    uploadStatus: document.getElementById('uploadStatus'),
    progressFill: document.getElementById('progressFill'),

    // Candidate List
    candidatesSection: document.getElementById('candidatesSection'),
    candidateList: document.getElementById('candidateList'),

    // Candidate Detail
    backToDashboardBtn: document.getElementById('backToDashboardBtn'),
    detailName: document.getElementById('detailName'),
    detailEmail: document.getElementById('detailEmail'),
    detailPhone: document.getElementById('detailPhone'),
    detailScore: document.getElementById('detailScore'),
    detailSuitability: document.getElementById('detailSuitability'),
    detailSummary: document.getElementById('detailSummary'),
    detailMatchedSkills: document.getElementById('detailMatchedSkills'),
    detailMissingSkills: document.getElementById('detailMissingSkills'),
    detailAllSkills: document.getElementById('detailAllSkills'),
    detailHighlights: document.getElementById('detailHighlights'),

    // Voice
    playSummaryBtn: document.getElementById('playSummaryBtn'),
    stopSummaryBtn: document.getElementById('stopSummaryBtn'),
    downloadSummaryBtn: document.getElementById('downloadSummaryBtn'),
    voiceIndicator: document.getElementById('voiceIndicator'),

    // Scoring
    similarityBar: document.getElementById('similarityBar'),
    skillBar: document.getElementById('skillBar'),
    experienceBar: document.getElementById('experienceBar'),
    similarityValue: document.getElementById('similarityValue'),
    skillValue: document.getElementById('skillValue'),
    experienceValue: document.getElementById('experienceValue'),

    // Status
    statusButtons: document.querySelectorAll('.status-btn'),
    statusMessage: document.getElementById('statusMessage'),
};

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    setupEventListeners();
    await loadJobs();
});

// ============================================================================
// EVENT LISTENERS
// ============================================================================
function setupEventListeners() {
    // New Job
    elements.newJobBtn.addEventListener('click', showNewJobView);
    elements.cancelJobBtn.addEventListener('click', showJobsView);
    elements.jobForm.addEventListener('submit', handleCreateJob);

    // Upload
    elements.dropzone.addEventListener('dragover', handleDragOver);
    elements.dropzone.addEventListener('dragleave', handleDragLeave);
    elements.dropzone.addEventListener('drop', handleDrop);
    elements.dropzone.addEventListener('click', () => elements.resumeFileInput.click());
    elements.resumeFileInput.addEventListener('change', handleFileSelect);
    elements.uploadBtn.addEventListener('click', handleUpload);

    // Candidate List
    elements.candidateList.addEventListener('click', handleCandidateClick);

    // Back Button
    elements.backToDashboardBtn.addEventListener('click', showJobDashboard);

    // Voice
    elements.playSummaryBtn.addEventListener('click', speakSummary);
    elements.stopSummaryBtn.addEventListener('click', stopSpeaking);
    elements.downloadSummaryBtn.addEventListener('click', downloadSummary);

    // Status buttons
    elements.statusButtons.forEach(btn => {
        btn.addEventListener('click', () => handleStatusChange(btn.dataset.status));
    });
}

// ============================================================================
// VIEW MANAGEMENT
// ============================================================================
function showView(view) {
    document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
    view.classList.remove('hidden');
}

function showNewJobView() {
    showView(elements.newJobView);
    elements.jobForm.reset();
}

function showJobsView() {
    showView(elements.newJobView);
    elements.jobForm.reset();
}

function showJobDashboard() {
    if (state.currentJobId) {
        showView(elements.jobDashboardView);
        loadJobDashboard(state.currentJobId);
    }
}

function showCandidateDetail(candidateId) {
    showView(elements.candidateDetailView);
    loadCandidateDetail(candidateId);
}

// ============================================================================
// API CALLS
// ============================================================================
async function loadJobs() {
    try {
        const response = await fetch('/api/job-requirements');
        const jobs = await response.json();
        state.jobs = jobs;
        renderJobList();
        
        if (jobs.length === 0) {
            showNewJobView();
        }
    } catch (error) {
        console.error('Error loading jobs:', error);
        showError('Failed to load jobs');
    }
}

async function handleCreateJob(e) {
    e.preventDefault();

    const formData = new FormData(elements.jobForm);
    const data = {
        job_title: formData.get('job_title'),
        company_name: formData.get('company_name') || 'Company',
        description: formData.get('description'),
        required_experience: parseInt(formData.get('required_experience')) || null,
    };

    try {
        const response = await fetch('/api/job-requirements', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (!response.ok) throw new Error('Failed to create job');

        const job = await response.json();
        state.currentJobId = job.id;
        await loadJobs();
        showJobDashboard();
    } catch (error) {
        console.error('Error creating job:', error);
        showError('Failed to create job opening');
    }
}

async function loadJobDashboard(jobId) {
    try {
        const response = await fetch(`/api/job-requirements/${jobId}`);
        const job = await response.json();

        state.currentJobId = jobId;
        elements.currentJobTitle.textContent = job.job_title;
        elements.currentCompanyName.textContent = `${job.company_name} • Job opened: ${new Date(job.created_at).toLocaleDateString()}`;

        const candidates = job.candidates;
        state.candidates = candidates;

        // Update stats
        elements.totalCandidates.textContent = candidates.length;
        elements.excellentCount.textContent = candidates.filter(c => c.overall_score >= 80).length;
        elements.goodCount.textContent = candidates.filter(c => c.overall_score >= 65 && c.overall_score < 80).length;

        renderCandidateList(candidates);

        if (candidates.length > 0) {
            elements.candidatesSection.style.display = 'block';
        }
    } catch (error) {
        console.error('Error loading job dashboard:', error);
        showError('Failed to load job dashboard');
    }
}

async function loadCandidateDetail(candidateId) {
    try {
        const response = await fetch(`/api/candidates/${candidateId}`);
        const candidate = await response.json();
        state.currentCandidate = candidate;

        // Populate candidate detail
        elements.detailName.textContent = candidate.name;
        elements.detailEmail.textContent = candidate.email || 'N/A';
        elements.detailPhone.textContent = candidate.phone || 'N/A';
        elements.detailScore.textContent = candidate.overall_score;
        elements.detailSuitability.textContent = candidate.verdict_phrase;
        elements.detailSummary.textContent = candidate.summary_text;

        // Populate avatar initials
        const initials = candidate.name.split(' ').map(n => n[0]).join('').toUpperCase();
        document.getElementById('candidateInitials').textContent = initials;

        // Skills
        renderSkillChips(elements.detailMatchedSkills, candidate.matched_skills);
        renderSkillChips(elements.detailMissingSkills, candidate.missing_skills);
        renderSkillChips(elements.detailAllSkills, candidate.all_skills_found);

        // Highlights
        renderHighlights(candidate.key_highlights);

        // Scoring breakdown
        animateScoreBars(candidate);

        // Update status buttons
        updateStatusButtons(candidate.status);

        // Enable voice and download buttons
        elements.playSummaryBtn.disabled = false;
        elements.downloadSummaryBtn.disabled = false;
    } catch (error) {
        console.error('Error loading candidate detail:', error);
        showError('Failed to load candidate details');
    }
}

async function updateCandidateStatus(candidateId, status) {
    try {
        const response = await fetch(`/api/candidates/${candidateId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status }),
        });

        if (!response.ok) throw new Error('Failed to update status');

        const candidate = await response.json();
        state.currentCandidate = candidate;
        updateStatusButtons(status);
        showSuccess(`Candidate marked as ${status}`);
    } catch (error) {
        console.error('Error updating candidate status:', error);
        showError('Failed to update candidate status');
    }
}

// ============================================================================
// FILE HANDLING
// ============================================================================
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.dropzone.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.dropzone.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.dropzone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    elements.resumeFileInput.files = files;
    handleFileSelect();
}

function handleFileSelect() {
    state.selectedFiles = Array.from(elements.resumeFileInput.files);
    const fileName = state.selectedFiles.length > 1 
        ? `${state.selectedFiles.length} files selected` 
        : state.selectedFiles[0]?.name || 'Click or drag files here';
    
    const dropzoneContent = elements.dropzone.querySelector('.dropzone-content');
    dropzoneContent.querySelector('.dropzone-text').textContent = fileName;
    elements.uploadBtn.style.display = 'block';
}

async function handleUpload() {
    if (!state.selectedFiles.length || !state.currentJobId) {
        showError('Please select resume files and ensure a job is selected');
        return;
    }

    const formData = new FormData();
    formData.append('job_requirement_id', state.currentJobId);
    state.selectedFiles.forEach(file => formData.append('files', file));

    try {
        elements.uploadProgress.style.display = 'block';
        elements.uploadBtn.disabled = true;
        elements.uploadStatus.textContent = 'Analyzing resumes...';

        const response = await fetch('/api/candidates/upload', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) throw new Error('Upload failed');

        const result = await response.json();

        // Refresh dashboard
        await loadJobDashboard(state.currentJobId);

        elements.uploadProgress.style.display = 'none';
        elements.uploadBtn.disabled = false;
        elements.resumeFileInput.value = '';
        state.selectedFiles = [];

        const dropzoneContent = elements.dropzone.querySelector('.dropzone-content');
        dropzoneContent.querySelector('.dropzone-text').textContent = '📁 Drag & drop resume files here or click to select';
        elements.uploadBtn.style.display = 'none';

        showSuccess(`Successfully analyzed ${result.success} resume(s)`);
        if (result.errors.length > 0) {
            console.warn('Errors during upload:', result.errors);
        }
    } catch (error) {
        console.error('Error uploading files:', error);
        showError('Failed to upload resumes');
        elements.uploadProgress.style.display = 'none';
        elements.uploadBtn.disabled = false;
    }
}

// ============================================================================
// RENDERING
// ============================================================================
function renderJobList() {
    if (state.jobs.length === 0) {
        elements.jobList.innerHTML = '<div class="empty-state">No jobs created yet</div>';
        return;
    }

    elements.jobList.innerHTML = state.jobs.map(job => `
        <div class="job-item ${job.id === state.currentJobId ? 'active' : ''}" 
             onclick="selectJob(${job.id})">
            <div class="job-item-title">${job.job_title}</div>
            <div class="job-item-count">${job.candidate_count} candidates</div>
        </div>
    `).join('');
}

function selectJob(jobId) {
    state.currentJobId = jobId;
    renderJobList();
    showJobDashboard();
}

function renderCandidateList(candidates) {
    if (!candidates.length) {
        elements.candidateList.innerHTML = '<p style="text-align: center; color: var(--text-secondary);">No candidates yet. Upload resumes to get started.</p>';
        elements.candidatesSection.style.display = 'none';
        return;
    }

    elements.candidateList.innerHTML = candidates
        .sort((a, b) => b.overall_score - a.overall_score)
        .map(candidate => `
            <div class="candidate-card" data-candidate-id="${candidate.id}">
                <div class="candidate-avatar">${candidate.name.split(' ').map(n => n[0]).join('').toUpperCase()}</div>
                <div class="candidate-info">
                    <div class="candidate-name">${candidate.name}</div>
                    <div class="candidate-email">${candidate.email || 'No email'}</div>
                </div>
                <div class="candidate-score">
                    <div class="score-badge ${getSuitabilityClass(candidate.overall_score)}">
                        ${candidate.overall_score}%
                    </div>
                    <div class="score-label">${candidate.suitability}</div>
                </div>
            </div>
        `).join('');
}

function handleCandidateClick(e) {
    const card = e.target.closest('.candidate-card');
    if (card) {
        const candidateId = card.dataset.candidateId;
        showCandidateDetail(parseInt(candidateId));
    }
}

function renderSkillChips(container, skills) {
    if (!skills || skills.length === 0) {
        container.innerHTML = '<p style="color: var(--text-light); font-size: 0.9rem;">None detected</p>';
        return;
    }

    container.innerHTML = skills.map(skill => `
        <div class="skill-chip">${skill}</div>
    `).join('');
}

function renderHighlights(highlights) {
    if (!highlights || highlights.length === 0) {
        elements.detailHighlights.innerHTML = '<p style="color: var(--text-light); font-size: 0.9rem;">No highlights detected</p>';
        return;
    }

    elements.detailHighlights.innerHTML = highlights.map(highlight => `
        <div class="highlight-item">🌟 ${highlight}</div>
    `).join('');
}

function animateScoreBars(candidate) {
    const bars = [
        { element: elements.similarityBar, value: candidate.similarity_score, label: elements.similarityValue },
        { element: elements.skillBar, value: candidate.skill_match_score, label: elements.skillValue },
        { element: elements.experienceBar, value: candidate.experience_match_score, label: elements.experienceValue },
    ];

    bars.forEach(bar => {
        bar.element.style.width = '0%';
        bar.label.textContent = '0%';

        setTimeout(() => {
            bar.element.style.width = `${bar.value}%`;
            animateCounter(bar.label, bar.value);
        }, 100);
    });
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 30;
    const interval = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(interval);
        }
        element.textContent = Math.round(current) + '%';
    }, 20);
}

function updateStatusButtons(currentStatus) {
    elements.statusButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.status === currentStatus) {
            btn.classList.add('active');
        }
    });
}

function getSuitabilityClass(score) {
    if (score >= 80) return 'excellent';
    if (score >= 65) return 'good';
    if (score >= 50) return 'fair';
    return 'poor';
}

// ============================================================================
// VOICE SYNTHESIS (Web Speech API)
// ============================================================================
function speakSummary() {
    if (!state.currentCandidate) return;

    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();

        const summaryText = state.currentCandidate.summary_text;
        const utterance = new SpeechSynthesisUtterance(summaryText);

        utterance.rate = 0.95;
        utterance.pitch = 1;
        utterance.volume = 1;

        utterance.onstart = () => {
            state.isSpeaking = true;
            elements.voiceIndicator.classList.remove('hidden');
            elements.playSummaryBtn.disabled = true;
            elements.stopSummaryBtn.disabled = false;
        };

        utterance.onend = () => {
            state.isSpeaking = false;
            elements.voiceIndicator.classList.add('hidden');
            elements.playSummaryBtn.disabled = false;
            elements.stopSummaryBtn.disabled = true;
        };

        utterance.onerror = (e) => {
            console.error('Speech synthesis error:', e);
            showError('Failed to play audio');
            state.isSpeaking = false;
            elements.voiceIndicator.classList.add('hidden');
            elements.playSummaryBtn.disabled = false;
        };

        window.speechSynthesis.speak(utterance);
    } else {
        showError('Speech synthesis not supported in your browser');
    }
}

function stopSpeaking() {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        state.isSpeaking = false;
        elements.voiceIndicator.classList.add('hidden');
        elements.playSummaryBtn.disabled = false;
        elements.stopSummaryBtn.disabled = true;
    }
}

function downloadSummary() {
    if (!state.currentCandidate) return;

    const text = state.currentCandidate.summary_text;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${state.currentCandidate.name.replace(/\s+/g, '_')}_summary.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ============================================================================
// STATUS CHANGE HANDLER
// ============================================================================
function handleStatusChange(status) {
    if (!state.currentCandidate) return;
    updateCandidateStatus(state.currentCandidate.id, status);
}

// ============================================================================
// NOTIFICATIONS
// ============================================================================
function showSuccess(message) {
    showNotification(message, 'success');
}

function showError(message) {
    showNotification(message, 'error');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#16a34a' : '#dc2626'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        font-weight: 600;
        animation: slideIn 0.3s ease-out;
        z-index: 1000;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
