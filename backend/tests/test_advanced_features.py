from services.analytics_engine import analytics_engine
from services.summary_generator import summary_generator

def test_advanced_features():
    print("--- Testing Advanced Analytics ---")
    
    # 1. Benchmarking
    role = "Java Developer"
    score = 75
    benchmark = analytics_engine.get_benchmark_comparison(role, score)
    print(f"\n[Benchmarking] User Score: {score} for {role}")
    print(f"Result: {benchmark['percentile']} ({benchmark['status']})")
    print(f"Details: {benchmark['comparison']}")
    
    assert benchmark['status'] in ["Good", "Excellent"], "Score 75 should be at least Good"

    # 2. Skill Trends
    skills = ["Java", "React", "COBOL"] # Include one weird skill
    trends = analytics_engine.get_skill_trends(skills)
    print(f"\n[Skill Trends] Analyzing: {skills}")
    for t in trends:
        print(f"Skill: {t['skill']} | Demand: {t['demand']} | Trend: {t['trend']}")
        
    assert len(trends) >= 2, "Should find trends for Java and React"

    # 3. Interview Prediction
    questions = analytics_engine.predict_interview_questions(["Java", "Spring Boot"])
    print(f"\n[Interview Prep] Predicted Questions:")
    for q in questions:
        print(f"- {q}")
        
    assert len(questions) > 0, "Should return at least one question"

    # 4. Summary Generation
    summary = summary_generator.generate_summary("Full Stack Developer", ["React", "Node.js", "MongoDB"])
    print(f"\n[Summary Generator]\n{summary}")
    
    assert "Full Stack Developer" in summary
    assert "React" in summary
    
    print("\n[SUCCESS] Advanced Features Test Passed!")

if __name__ == "__main__":
    test_advanced_features()
