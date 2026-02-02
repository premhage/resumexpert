import spacy
import re

class NLPProcessor:
    def __init__(self):
        """
        Initialize the NLP Processor by loading the spaCy model.
        Usage: processor = NLPProcessor()
        """
        try:
            # Load the medium-sized English model
            # It contains word vectors which are useful for similarity (Phase 2),
            # though we will use Sentence Transformers for the heavy lifting.
            print("Loading spaCy model...")
            self.nlp = spacy.load("en_core_web_md")
            print("spaCy model loaded successfully.")
        except OSError:
            print("❌ Error: spaCy model 'en_core_web_md' not found.")
            print("Run: python -m spacy download en_core_web_md")
            self.nlp = None

    def preprocess_text(self, text):
        """
        Standardizes text for analysis:
        1. Tokenization
        2. Lowercasing
        3. Lemmatization (converting words to their base form, e.g., 'running' -> 'run')
        4. Removing stop words (common words like 'and', 'the') and punctuation.
        
        Returns:
            list: A list of cleaned string tokens.
        """
        if not self.nlp or not text:
            return []

        # Create a spaCy Doc object
        doc = self.nlp(text)
        
        cleaned_tokens = []
        
        for token in doc:
            # Filter out stop words, punctuation, and whitespace
            if not token.is_stop and not token.is_punct and not token.is_space:
                # Use the lemma (base form) and convert to lower case
                cleaned_tokens.append(token.lemma_.lower())
                
        return cleaned_tokens

    def get_entities(self, text):
        """
        Extracts named entities (like companies, dates, or geopolitical entities)
        that spaCy recognizes out-of-the-box.
        """
        if not self.nlp or not text:
            return []
        
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

# Singleton instance to avoid reloading the model multiple times
nlp_processor = NLPProcessor()
