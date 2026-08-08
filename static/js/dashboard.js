// Dashboard JavaScript

const state = {
    user: null,
    jobs: [],
    currentJobId: null,
};

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadUserProfile();
    await loadJobs();
    setupNavigation();
    setupFormHandlers();
});

// Load user profile
async function loadUserProfile() {
    try {
        const response = await fetch('/api/profile');
        const user = await response.json();
        state.user = user;

        document.getElementById('userFullName').textContent = user.full_name || user.username;
        document.getElementById('userEmail').textContent = user.email;

        // Populate profile form
        document.getElementById('profile_username').value = user.username;
        document.getElementById('profile_email').value = user.email;
        document.getElementById('profile_full_name').value = user.full_name || '';
        document.getElementById('profile_company_name').value = user.company_name || '';
        document.getElementById('profile_phone').value = user.phone || '';
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Load jobs
async function loadJobs() {
    try {
        const response = await fetch('/api/jobs');
        const jobs = await response.json();
        state.jobs = jobs;

        renderJobsList();
        updateDashboard();
    } catch (error) {
        console.error('Error loading jobs:', error);
    }
}

// Render jobs list
function renderJobsList() {
    const listContainer = document.getElementById('jobsList');
    const recentContainer = document.getElementById('recentJobsList');

    if (state.jobs.length === 0) {
        listContainer.innerHTML = '<div class="empty-state">No job openings yet. <a href="#new-job" class="link" onclick="switchView(\'new-job\')">Create one</a></div>';
        recentContainer.innerHTML = '<div class="empty-state">No job openings yet. <a href="#new-job" class="link" onclick="switchView(\'new-job\')">Create one</a></div>';
        return;
    }

    const jobsHtml = state.jobs.map(job => `
        <div class="job-card" onclick="selectJob(${job.id})">
            <div class="job-card-title">💼 ${job.job_title}</div>
            <div class="job-card-meta">
                <span>📍 ${job.company_name}</span>
                <span>👥 ${job.candidate_count} candidates</span>
                <span>📅 ${new Date(job.created_at).toLocaleDateString()}</span>
            </div>
        </div>
    `).join('');

    listContainer.innerHTML = jobsHtml;
    recentContainer.innerHTML = jobsHtml.slice(0, 3);
}

// Update dashboard stats
function updateDashboard() {
    const activeJobs = state.jobs.filter(j => j.status === 'active').length;
    const totalCandidates = state.jobs.reduce((sum, j) => sum + j.candidate_count, 0);

    document.getElementById('activeJobs').textContent = activeJobs;
    document.getElementById('totalCandidates').textContent = totalCandidates;
    document.getElementById('excellentMatches').textContent = '0'; // TODO: Calculate
    document.getElementById('callsSent').textContent = '0'; // TODO: Calculate
}

// Navigation
function setupNavigation() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const view = item.dataset.view;
            switchView(view);
            updateNavigation(item);
        });
    });
}

function switchView(viewName) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));

    // Show selected view
    const view = document.getElementById(viewName + 'View');
    if (view) {
        view.classList.add('active');
    }

    // Scroll to top
    document.querySelector('.main-content').scrollTop = 0;
}

function updateNavigation(activeItem) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    activeItem.classList.add('active');
}

function selectJob(jobId) {
    state.currentJobId = jobId;
    // TODO: Redirect to job detail view
    console.log('Selected job:', jobId);
}

// Form handlers
function setupFormHandlers() {
    // Job form
    document.getElementById('jobForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            job_title: document.getElementById('job_title').value,
            company_name: document.getElementById('company_name').value,
            description: document.getElementById('description').value,
            job_type: document.getElementById('job_type').value,
            required_experience: parseInt(document.getElementById('required_experience').value) || null,
            salary_min: parseInt(document.getElementById('salary_min').value) || null,
            salary_max: parseInt(document.getElementById('salary_max').value) || null,
            location: document.getElementById('location').value,
        };

        try {
            const response = await fetch('/api/jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                const result = await response.json();
                showNotification('Job created successfully!', 'success');
                document.getElementById('jobForm').reset();
                await loadJobs();
                switchView('jobs');
            } else {
                showNotification('Failed to create job', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        }
    });

    // Profile form
    document.getElementById('profileForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const profileData = {
            full_name: document.getElementById('profile_full_name').value,
            company_name: document.getElementById('profile_company_name').value,
            phone: document.getElementById('profile_phone').value,
        };

        try {
            const response = await fetch('/api/profile', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(profileData)
            });

            if (response.ok) {
                showNotification('Profile updated successfully!', 'success');
                await loadUserProfile();
            } else {
                showNotification('Failed to update profile', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            showNotification('An error occurred', 'error');
        }
    });
}

// Notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : '#4299e1'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(400px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(400px);
        }
    }
`;
document.head.appendChild(style);
