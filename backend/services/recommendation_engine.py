import json
import os

class RecommendationEngine:
    def __init__(self):
        self.roadmaps = self._load_roadmaps()

    def _load_roadmaps(self):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', 'learning_roadmaps.json')
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading roadmaps: {e}")
            return {}

    def generate_recommendations(self, role_analysis, target_role_name=None):
        """
        Generates advice based on the best fit role or a specific target role.
        """
        if not role_analysis:
            return []

        # Determine target role (default to the highest scoring one)
        target = role_analysis[0]
        if target_role_name:
            for r in role_analysis:
                if r['role'] == target_role_name:
                    target = r
                    break
        
        recommendations = []
        
        # 1. Critical Skill Gaps
        missing = target['missing_critical_skills']
        if missing:
            rec_text = f"You are missing critical skills for {target['role']}: {', '.join(missing[:3])}."
            recommendations.append({
                "type": "Critical Skill",
                "text": rec_text,
                "priority": "High"
            })
            
        # 2. General Score Advice
        score = target['score']
        if score < 50:
            recommendations.append({
                "type": "Strategy",
                "text": f"Your profile is a weak match for {target['role']}. Focus on building the foundational projects listed in the roadmap.",
                "priority": "High"
            })
        elif score > 80:
             recommendations.append({
                "type": "Strategy",
                "text": "Excellent match! Focus on advanced system design and interview prep.",
                "priority": "Medium"
            })

        return recommendations

    def get_roadmap(self, role_name):
        """
        Returns the learning roadmap for a specific role.
        """
        return self.roadmaps.get(role_name, [])

recommendation_engine = RecommendationEngine()
