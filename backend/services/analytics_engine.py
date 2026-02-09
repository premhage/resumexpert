import json
import os
import random

class AnalyticsEngine:
    def __init__(self):
        self.benchmarks = self._load_json('benchmarks.json')
        self.skill_trends = self._load_json('skill_trends.json')
        self.interview_questions = self._load_json('interview_questions.json')

    def _load_json(self, filename):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return {}

    def get_benchmark_comparison(self, role, score):
        """
        Compares user score against industry benchmarks for the given role.
        Assumes 'Junior' level for MVP simplicity, or we could infer from years of exp.
        """
        role_data = self.benchmarks.get(role, {})
        # Default to Junior logic if we don't have experience parsing yet
        level_data = role_data.get("Junior") 
        
        if not level_data:
            return {"percentile": "Unknown", "status": "N/A"}
            
        avg = level_data['average_score']
        top = level_data['top_10_score']
        
        if score >= top:
            return {"percentile": "Top 10%", "status": "Excellent", "comparison": f"You are significantly above the market average of {avg}%."}
        elif score >= avg:
            return {"percentile": "Top 50%", "status": "Good", "comparison": f"You are above the market average of {avg}%."}
        else:
            return {"percentile": "Bottom 50%", "status": "Needs Improvement", "comparison": f"You are below the market average of {avg}%."}

    def get_skill_trends(self, skills):
        """
        Returns trend data for the provided list of skills.
        """
        insights = []
        for skill in skills:
            # We check case-insensitive usually, but our DB keys are Capitalized
            # Ideally we'd flatten keys, but for MVP we assume matching format or direct lookup
            trend_data = self.skill_trends.get(skill) # Simple lookup
            
            # Try title case if simple lookup fails
            if not trend_data:
                trend_data = self.skill_trends.get(skill.title())
                
            if trend_data:
                insights.append({
                    "skill": skill,
                    "demand": trend_data['demand'],
                    "trend": trend_data['trend']
                })
        return insights

    def predict_interview_questions(self, skills):
        """
        Returns a list of 5 random interview questions relevant to the user's skills.
        """
        relevant_questions = []
        
        for skill in skills:
            questions = self.interview_questions.get(skill)
            if not questions:
                questions = self.interview_questions.get(skill.title())
                
            if questions:
                relevant_questions.extend(questions)
                
        # Shuffle and pick 5 unique ones
        if relevant_questions:
            random.shuffle(relevant_questions)
            return list(set(relevant_questions))[:5]
            
        return ["Tell me about yourself.", "What is your greatest strength?", "Why do you want this job?"]

analytics_engine = AnalyticsEngine()
