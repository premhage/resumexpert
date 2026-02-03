from backend.services.matching_engine import matching_engine

def test_engine():
    print("--- Testing Matching Engine ---")

    # Sample Job Description (Python Developer)
    jd_text = """
    We are looking for a Python Developer with experience in Flask and REST APIs.
    Must know SQL databases like PostgreSQL.
    Machine Learning knowledge using scikit-learn is a plus.
    Good communication skills required.
    """

    # Sample Resume 1: Good Match
    resume_good = """
    Experienced Python Backend Developer.
    Skilled in building RESTful services using Flask and Django.
    Proficient in PostgreSQL and MySQL.
    Familiar with basic Machine Learning concepts and scikit-learn.
    Strong team player with excellent communication skills.
    """

    # Sample Resume 2: Poor Match (Designer)
    resume_bad = """
    Graphic Designer with 5 years of experience.
    Expert in Adobe Photoshop, Illustrator, and Figma.
    Creative UI/UX design skills.
    Love painting and sketching.
    """

    print("\nAnalyzing Good Match Resume...")
    scores_good = matching_engine.evaluate(resume_good, jd_text)
    print(f"Scores: {scores_good}")

    print("\nAnalyzing Bad Match Resume...")
    scores_bad = matching_engine.evaluate(resume_bad, jd_text)
    print(f"Scores: {scores_bad}")
    
    # Assertions
    assert scores_good['overall_score'] > scores_bad['overall_score'], "Good resume should score higher!"
    assert scores_good['keyword_match'] > 0, "Good resume should have keyword match"
    
    print("\n[SUCCESS] Test Passed: Logic holds up!")

if __name__ == "__main__":
    test_engine()
