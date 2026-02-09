from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all domains
CORS(app)
api = Api(app)

# Service Imports
from services.resume_parser import parse_resume, clean_text
from services.nlp_processor import nlp_processor
from services.skill_extractor import skill_extractor
from services.matching_engine import matching_engine
from services.role_scorer import role_scorer
from services.recommendation_engine import recommendation_engine
from services.analytics_engine import analytics_engine
from services.summary_generator import summary_generator

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return {"error": "No resume file uploaded"}, 400
    
    file = request.files['resume']
    jd_text = request.form.get('job_description', '')
    
    if file.filename == '':
        return {"error": "No selected file"}, 400
        
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        try:
            # 1. Parse Resume
            resume_text = parse_resume(filepath)
            if not resume_text:
                return {"error": "Could not extract text from resume"}, 400
            
            # 2. Extract Skills
            cleaned_text = " ".join(nlp_processor.preprocess_text(resume_text))
            extracted_skills = skill_extractor.extract_skills(resume_text) # Pass raw text for regex
            
            # Flatten skills for easy access
            flat_skills = []
            for cat, skills in extracted_skills.items():
                flat_skills.extend(skills)
            
            # 3. Match against JD (if provided)
            match_scores = matching_engine.evaluate(clean_text(resume_text), clean_text(jd_text)) if jd_text else {}
            
            # 4. Role Analysis
            role_scores = role_scorer.score_roles(extracted_skills)
            best_role = role_scores[0]['role'] if role_scores else "General"
            
            # 5. Advanced Analytics
            benchmark = analytics_engine.get_benchmark_comparison(best_role, match_scores.get('overall_score', 0))
            trends = analytics_engine.get_skill_trends(flat_skills)
            interview_q = analytics_engine.predict_interview_questions(flat_skills)
            summary = summary_generator.generate_summary(best_role, flat_skills)
            
            # 6. Recommendations
            recommendations = recommendation_engine.generate_recommendations(role_scores)
            roadmap = recommendation_engine.get_roadmap(best_role)
            
            # Cleanup
            os.remove(filepath)
            
            return {
                "success": True,
                "analysis": {
                    "resume_text_preview": resume_text[:500] + "...",
                    "extracted_skills": extracted_skills,
                    "match_scores": match_scores,
                    "role_scores": role_scores[:3], # Top 3 roles
                    "best_fit_role": best_role,
                    "benchmark": benchmark,
                    "skill_trends": trends,
                    "interview_questions": interview_q,
                    "summary": summary,
                    "recommendations": recommendations,
                    "roadmap": roadmap
                }
            }
            
        except Exception as e:
            return {"error": str(e)}, 500

@app.route('/')
def home():
    # Serve the frontend HTML
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    if os.path.exists(frontend_path):
        from flask import send_file
        return send_file(frontend_path)
    return {"message": "ResumeXpert API is running. Use POST /api/upload to analyze resumes."}

@app.route('/<path:path>')
def serve_frontend(path):
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
    file_path = os.path.join(frontend_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        from flask import send_file
        return send_file(file_path)
    # If file not found, return frontend index.html for client-side routing
    index_path = os.path.join(frontend_dir, 'index.html')
    if os.path.exists(index_path):
        from flask import send_file
        return send_file(index_path)
    return {"error": "Not found"}, 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
