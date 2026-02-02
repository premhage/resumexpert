# ResumeXpert - System Architecture

## Overview
ResumeXpert is an AI-powered resume analysis and career guidance system. It uses a hybrid approach combining traditional keyword matching (TF-IDF/BM25) with modern semantic understanding (Sentence Transformers) to evaluate resumes against job descriptions.

## High-Level Architecture

```mermaid
graph TD
    User[User] -->|Upload Resume| Frontend[Frontend (Dashboard)]
    User -->|Input JD| Frontend
    
    Frontend -->|REST API| Backend[Flask Backend]
    
    subgraph "Backend Services"
        Backend -->|Parse| Parser[Resume Parser (PDF/DOCX)]
        Backend -->|Process| NLP[NLP Processor (spaCy)]
        NLP -->|Extract| Skills[Skill Extractor]
        
        Backend -->|Match| Engine[Matching Engine]
        Engine -->|Keyword| TFIDF[TF-IDF / BM25]
        Engine -->|Semantic| SBERT[Sentence Transformers]
        
        Backend -->|Generate| Recommender[Recommendation Engine]
    end
    
    subgraph "Data Persistence"
        Backend -->|Read/Write| Supabase[Supabase (PostgreSQL)]
    end
```

## Tech Stack

### Frontend
- **HTML5/CSS3**: Core structure and styling.
- **JavaScript (ES6+)**: logic and API interaction.
- **Chart.js**: Data visualization.
- **Bootstrap 5**: Responsive layout.

### Backend
- **Language**: Python 3.9+
- **Framework**: Flask (RESTful API).
- **Libraries**:
    - `flask-cors`: Cross-Origin Resource Sharing.
    - `pypdf2`, `pdfplumber`, `python-docx`: File parsing.
    - `spacy`: NLP and Named Entity Recognition.
    - `sentence-transformers`: Semantic embeddings.
    - `scikit-learn`: TF-IDF and cosine similarity.
    - `supabase`: Database client.

### Database (Supabase)
- **Tables**:
    - `users`: User management (Optional).
    - `resume_analysis`: Stores parsed resume data and analysis results.
    - `role_scores`: Scores for different roles.
    - `recommendations`: AI-generated suggestions.
    - `learning_roadmaps`: Generated learning paths.
    - `skill_trends`: Aggregated market data.

## Data Flow

1.  **Input**: User uploads a resume (PDF/DOCX) and provides a Job Description (JD).
2.  **Parsing**: System extracts text from the resume and cleans the JD.
3.  **Preprocessing**: Text is tokenized, lemmatized, and stop-words are removed.
4.  **Extraction**: Skills, Education, and Experience are extracted.
5.  **Vectorization**:
    - Resume and JD are converted to TF-IDF vectors.
    - Resume and JD are converted to Semantic Embeddings.
6.  **Matching**:
    - Calculate Cosine Similarity for both vectors.
    - Compute Weighted Score (60% Semantic + 40% Keyword).
7.  **Analysis**:
    - Identify Skill Gaps.
    - Generate Recommendations.
    - Predict Compatibility for other roles.
8.  **Output**: JSON response sent to Frontend for visualization.
