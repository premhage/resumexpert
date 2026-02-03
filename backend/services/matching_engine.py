from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

class MatchingEngine:
    def __init__(self):
        """
        Initializes the matching engine.
        Loads the SentenceTransformer model (semantic) which might take a few seconds.
        """
        print("Loading Sentence Transformer model (all-MiniLM-L6-v2)...")
        # all-MiniLM-L6-v2 is a lightweight, fast, and high-quality model for semantic similarity
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Sentence Transformer model loaded.")

    def calculate_keyword_score(self, resume_text, jd_text):
        """
        Calculates similarity based on finding exact keywords (TF-IDF).
        Good for specific technical terms (e.g., "SQL", "Python").
        """
        if not resume_text or not jd_text:
            return 0.0
            
        try:
            # Create vectors (1-gram and 2-gram to capture phrases like "Machine Learning")
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
            
            # Compute Cosine Similarity between the two
            # matrix[0] is resume, matrix[1] is JD
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error in keyword scoring: {e}")
            return 0.0

    def calculate_semantic_score(self, resume_text, jd_text):
        """
        Calculates similarity based on meaning (Embeddings).
        Good for context (e.g., matching "coding" with "software development").
        """
        if not resume_text or not jd_text:
            return 0.0
            
        try:
            # Encode both texts into high-dimensional vectors
            embeddings = self.semantic_model.encode([resume_text, jd_text])
            
            # Compute Cosine Similarity
            # embeddings[0] is resume, embeddings[1] is JD
            # We reshape to (1, -1) because cosine_similarity expects 2D arrays
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error in semantic scoring: {e}")
            return 0.0

    def evaluate(self, resume_text, jd_text):
        """
        Main evaluation function.
        Combines semantic and keyword scores.
        Weight: 60% Semantic, 40% Keyword (as per project spec).
        """
        keyword_score = self.calculate_keyword_score(resume_text, jd_text)
        semantic_score = self.calculate_semantic_score(resume_text, jd_text)
        
        # Weighted combination
        overall_score = (semantic_score * 0.6) + (keyword_score * 0.4)
        
        # Convert to percentages (0-100) for UI friendliness, rounded to 1 decimal
        return {
            "overall_score": round(overall_score * 100, 1),
            "keyword_match": round(keyword_score * 100, 1),
            "semantic_match": round(semantic_score * 100, 1)
        }

# Singleton
matching_engine = MatchingEngine()
