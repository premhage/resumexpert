document.addEventListener('DOMContentLoaded', () => {
    // 1. Retrieve Data
    const dataString = localStorage.getItem('resumeAnalysis');

    if (!dataString) {
        alert("No analysis data found. Please upload a resume first.");
        window.location.href = 'index.html';
        return;
    }

    const data = JSON.parse(dataString);
    console.log("Dashboard Data Loaded:", data);

    // 2. Render Executive Summary
    document.getElementById('summaryText').textContent = data.summary;

    // 3. Render Best Fit Role
    const bestRole = data.best_fit_role;
    document.getElementById('roleDisplay').textContent = `Target Role: ${bestRole}`;

    // 4. Render Benchmarks
    const bench = data.benchmark;
    const benchEl = document.getElementById('benchmarkDisplay');
    benchEl.innerHTML = `<strong>${bench.percentile}</strong> (${bench.status}) <br> <small>${bench.comparison}</small>`;

    // Color coding for benchmark
    if (bench.status === "Excellent" || bench.status === "Good") {
        benchEl.className = "alert alert-success py-2 mt-3";
    } else {
        benchEl.className = "alert alert-warning py-2 mt-3";
    }

    // 5. Render Chart (Score Gauge)
    const score = data.match_scores.overall_score || data.role_scores[0].score;
    document.getElementById('scoreDisplay').textContent = `${score}%`;
    renderScoreChart(score);

    // 6. Render Roles Table
    const rolesBody = document.getElementById('rolesTable');
    data.role_scores.forEach(role => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${role.role}</strong></td>
            <td>
                <div class="progress" style="height: 10px;">
                    <div class="progress-bar bg-primary" role="progressbar" style="width: ${role.score}%"></div>
                </div>
                <small>${role.score}%</small>
            </td>
            <td>
                <button class="btn btn-sm btn-outline-primary view-roadmap-btn" onclick="filterRoadmap('${role.role}')">View Roadmap</button>
            </td>
        `;
        rolesBody.appendChild(row);
    });

    // 7. Render Skills
    // Matched
    const matchedContainer = document.getElementById('matchedSkillsList');
    data.role_scores[0].matched_skills.forEach(skill => {
        const span = document.createElement('span');
        span.className = "skill-tag matched";
        span.textContent = skill;
        matchedContainer.appendChild(span);
    });

    // Missing
    const missingContainer = document.getElementById('missingSkillsList');
    data.role_scores[0].missing_critical_skills.forEach(skill => {
        const li = document.createElement('li');
        li.className = "list-group-item d-flex justify-content-between align-items-center text-danger";
        li.innerHTML = `Missing: ${skill} <span class="badge bg-danger rounded-pill">Critical</span>`;
        missingContainer.appendChild(li);
    });

    // 8. Market Trends
    const trendsList = document.getElementById('trendsList');
    if (data.skill_trends && data.skill_trends.length > 0) {
        data.skill_trends.forEach(trend => {
            let badgeClass = "badge bg-secondary";
            if (trend.demand === "High") badgeClass = "badge bg-success";
            else if (trend.demand === "Low") badgeClass = "badge bg-warning text-dark";

            let trendIcon = "➡️";
            if (trend.trend === "Rising") trendIcon = "↗️";
            if (trend.trend === "Declining") trendIcon = "↘️";

            const li = document.createElement('li');
            li.className = "list-group-item";
            li.innerHTML = `
                ${trend.skill} 
                <span class="trend-badge text-muted">${trendIcon} ${trend.trend}</span>
                <span class="${badgeClass} float-end me-2">${trend.demand} Demand</span>
            `;
            trendsList.appendChild(li);
        });
    } else {
        trendsList.innerHTML = "<li class='list-group-item text-muted'>No trend data available for top skills.</li>";
    }

    // 9. Recommendations
    const recList = document.getElementById('recommendationsList');
    data.recommendations.forEach(rec => {
        const p = document.createElement('div');
        p.className = "alert alert-light border-start border-4 border-info";
        p.innerHTML = `<strong>${rec.type}:</strong> ${rec.text}`;
        recList.appendChild(p);
    });

    // 10. Roadmap
    renderRoadmap(data.roadmap);

    // 11. Interview Prep
    const interviewContainer = document.getElementById('interviewAccordion');
    if (data.interview_questions) {
        data.interview_questions.forEach((q, index) => {
            const item = document.createElement('div');
            item.className = "accordion-item";
            item.innerHTML = `
                <h2 class="accordion-header" id="heading${index}">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${index}">
                        Question #${index + 1}
                    </button>
                </h2>
                <div id="collapse${index}" class="accordion-collapse collapse" data-bs-parent="#interviewAccordion">
                    <div class="accordion-body">
                        <strong>${q}</strong>
                        <p class="mt-2 text-muted small">Prepare a STAR method answer specifically mentioning your experience.</p>
                    </div>
                </div>
            `;
            interviewContainer.appendChild(item);
        });
    }
});

function renderScoreChart(score) {
    const ctx = document.getElementById('scoreChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Score', 'Gap'],
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: ['#4A90E2', '#E0E0E0'],
                borderWidth: 0
            }]
        },
        options: {
            circumference: 180,
            rotation: -90,
            cutout: '80%',
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function renderRoadmap(steps) {
    const container = document.getElementById('roadmapTimeline');
    container.innerHTML = "";

    if (!steps || steps.length === 0) {
        container.innerHTML = "<p class='text-muted'>No specific roadmap available for this role yet.</p>";
        return;
    }

    steps.forEach(step => {
        const div = document.createElement('div');
        div.className = "timeline-item";
        div.innerHTML = `
            <h5 class="fw-bold">Week ${step.week}: ${step.topic}</h5>
            <p>${step.details}</p>
            <a href="${step.resources[0]}" target="_blank" class="btn btn-sm btn-outline-secondary">View Resource</a>
        `;
        container.appendChild(div);
    });
}
