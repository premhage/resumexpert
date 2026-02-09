# ResumeXpert API Documentation

This API powers the ResumeXpert application, providing resume parsing, skill extraction, role matching, and career guidance.

## Base URL
`http://localhost:5000`

---

## Endpoints

### 1. Health Check
**GET** `/`

Returns the API status.

**Response:**
```json
{
  "message": "ResumeXpert API is running..."
}
```

### 2. Upload & Analyze Resume
**POST** `/api/upload`

Uploads a resume file and optional job description for analysis.

**Headers:**
- `Content-Type`: `multipart/form-data`

**Body Parameters:**
- `resume` (File): The resume file (`.pdf` or `.docx`). **Required**.
- `job_description` (Text): The job description text to match against. **Optional**.

**Response (Success - 200 OK):**
```json
{
  "success": true,
  "analysis": {
    "resume_text_preview": "John Doe \n Software Engineer...",
    "extracted_skills": {
      "Programming Languages": ["Python", "Java"],
      "Databases": ["SQL"]
    },
    "match_scores": {
      "overall_score": 75.5,
      "keyword_match": 60.0,
      "semantic_match": 85.0
    },
    "role_scores": [
      {
        "role": "Python Developer",
        "score": 80.0,
        "missing_critical_skills": ["Docker"]
      }
    ],
    "best_fit_role": "Python Developer",
    "benchmark": {
      "percentile": "Top 50%",
      "status": "Good"
    },
    "skill_trends": [
      { "skill": "Python", "demand": "High", "trend": "Rising" }
    ],
    "interview_questions": [
      "Explain lists vs tuples in Python."
    ],
    "summary": "Experienced Python Developer...",
    "recommendations": [
      { "type": "Critical Skill", "text": "Learn Docker..." }
    ],
    "roadmap": [
      { "week": "1-2", "topic": "Advanced Python", ... }
    ]
  }
}
```

**Response (Error - 400 Bad Request):**
```json
{
  "error": "No resume file uploaded"
}
```
