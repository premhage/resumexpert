const API_URL = 'http://localhost:5000/api';

async function uploadResume(file, jobDescription) {
    const formData = new FormData();
    formData.append('resume', file);
    if (jobDescription) {
        formData.append('job_description', jobDescription);
    }

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }

        return await response.json();
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}
