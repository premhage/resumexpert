import json
import os

class RoleScorer:
    def __init__(self):
        self.role_requirements = self._load_role_requirements()

    def _load_role_requirements(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', 'role_requirements.json')
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading role requirements: {e}")
            return {}

    def score_roles(self, extracted_skills):
        """
        Evaluates the candidate against all defined roles.
        extracted_skills: dict { category: [list of skills] }
        Returns: list of dicts with role scores, sorted by best fit.
        """
        # Flatten extracted skills into a single set for easy lookup (lowercase)
        user_skills_set = set()
        for category, skills in extracted_skills.items():
            for skill in skills:
                user_skills_set.add(skill.lower())

        results = []

        for role, data in self.role_requirements.items():
            critical = data.get("critical_skills", [])
            recommended = data.get("recommended_skills", [])
            
            # Calculate matches
            critical_matches = [s for s in critical if s.lower() in user_skills_set]
            rec_matches = [s for s in recommended if s.lower() in user_skills_set]
            
            missing_critical = [s for s in critical if s.lower() not in user_skills_set]
            
            # Scoring Logic (Customizable)
            # Critical skills are worth 2x recommended skills
            # Max Score = (Num Critical * 2) + (Num Recommended * 1)
            max_score = (len(critical) * 2) + len(recommended)
            if max_score == 0:
                max_score = 1 # Avoid division by zero
                
            my_score = (len(critical_matches) * 2) + len(rec_matches)
            
            percentage = (my_score / max_score) * 100
            
            results.append({
                "role": role,
                "score": round(percentage, 1),
                "missing_critical_skills": missing_critical,
                "matched_skills": critical_matches + rec_matches
            })
            
        # Sort by highest score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

role_scorer = RoleScorer()
