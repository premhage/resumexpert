from backend.services.role_scorer import role_scorer
from backend.services.recommendation_engine import recommendation_engine

def test_analytics():
    print("--- Testing Analytics System ---")
    
    # Mock extracted skills (Simulating a Data Scientist profile)
    user_skills = {
        "Programming Languages": ["Python", "R"],
        "Data Science": ["Machine Learning", "Pandas", "NumPy", "Scikit-learn"],
        "Databases": ["SQL"]
    }
    
    print("\n1. Testing Role Scorer...")
    role_scores = role_scorer.score_roles(user_skills)
    
    # Print top 3 roles
    for r in role_scores[:3]:
        print(f"Role: {r['role']} | Score: {r['score']}%")
        
    best_role = role_scores[0]['role']
    print(f"Best Fit: {best_role}")
    
    assert best_role == "Data Scientist", "System failed to identify Data Scientist profile"
    
    print("\n2. Testing Recommendations...")
    recs = recommendation_engine.generate_recommendations(role_scores)
    for rec in recs:
        print(f"[{rec['priority']}] {rec['type']}: {rec['text']}")
        
    roadmap = recommendation_engine.get_roadmap(best_role)
    print(f"\nFetched Roadmap steps: {len(roadmap)}")
    assert len(roadmap) > 0, "Roadmap should not be empty"

    print("\n[SUCCESS] Analytics Test Passed!")

if __name__ == "__main__":
    test_analytics()
