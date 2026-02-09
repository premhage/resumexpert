# 🚀 ResumeXpert - AI-Powered Resume Analyzer

ResumeXpert is an intelligent career guidance system that uses NLP and Machine Learning to analyze resumes, identify skill gaps against target roles, and provide personalized learning roadmaps.

## ✨ Features

- **Resume Parsing**: Extracts structured data from PDF and DOCX files.
- **Smart Matching**: Uses TF-IDF and Semantic Analysis (Sentence Transformers) to score resumes against job descriptions.
- **Role Analysis**: Evaluates candidate fit for multiple roles (e.g., Data Scientist, Java Developer).
- **Skill Gap Analysis**: Identifies critical missing skills.
- **Career Roadmap**: Generates week-by-week learning plans.
- **Market Insights**: Shows skill demand trends and benchmarks.
- **Interview Prep**: Predicts potential technical interview questions.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-RESTful
- **AI/ML**: spaCy, sentence-transformers, scikit-learn
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js

## 🚀 How to Run

### 1. Prerequisites

- Python 3.9+
- Git

### 2. Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/premhage/ResumeXpert.git
    cd ResumeXpert
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```

4.  Download the required spaCy model:
    ```bash
    python -m spacy download en_core_web_md
    ```

### 3. Running the Application

1.  Start the Backend Server:
    ```bash
    python backend/app.py
    ```
    The server will run at `http://localhost:5000`.

2.  Open the Frontend:
    - Navigate to the `frontend` folder.
    - Open `index.html` in your web browser.

### 4. Usage

1.  Click **"Choose File"** and upload your resume (PDF/DOCX).
2.  (Optional) Paste a Job Description for better matching accuracy.
3.  Click **"Analyze My Resume"**.
4.  View your **Match Score**, **Skill Gaps**, and **Personalized Roadmap** on the dashboard.

## 🧪 Running Tests

To verify the system components:

```bash
# Test Core Matching Engine
python -m backend.tests.test_matching

# Test Advanced Analytics
python -m backend.tests.test_advanced_features

# Test API Upload Endpoint
python test_api_upload.py
```

## 📂 Project Structure

```
ResumeXpert/
├── backend/
│   ├── app.py                 # Main Flask Application
│   ├── services/              # Core Logic (Parser, NLP, Matcher)
│   ├── data/                  # JSON Data (Roles, Roadmaps, Trends)
│   └── tests/                 # Unit Tests
├── frontend/
│   ├── index.html             # Landing Page
│   ├── dashboard.html         # Analysis Dashboard
│   ├── css/                   # Stylesheets
│   └── js/                    # JavaScript Logic
├── scripts/                   # Database Setup Scripts
└── requirements.txt           # Python Dependencies
```

---
Built with ❤️ by Prem Hage
