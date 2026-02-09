document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');

    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const fileInput = document.getElementById('resumeFile');
            const jdInput = document.getElementById('jobDescription');

            if (!fileInput.files.length) {
                alert("Please select a resume file.");
                return;
            }

            const file = fileInput.files[0];
            const jdText = jdInput.value;

            // Show loading state
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('d-none');
            loadingSpinner.classList.remove('d-none');

            try {
                // Call the API function from api.js
                const result = await uploadResume(file, jdText);

                if (result.success) {
                    // Store data in localStorage to pass to dashboard.html
                    localStorage.setItem('resumeAnalysis', JSON.stringify(result.analysis));
                    window.location.href = 'dashboard.html';
                }
            } catch (error) {
                alert("Analysis failed: " + error.message);
                analyzeBtn.disabled = false;
                analyzeBtn.classList.remove('d-none');
                loadingSpinner.classList.add('d-none');
            }
        });
    }
});
