import json
import os
import re
from backend.services.nlp_processor import nlp_processor

class SkillExtractor:
    def __init__(self):
        self.skills_db = self._load_skills_db()
        self.flattened_skills = self._flatten_skills()

    def _load_skills_db(self):
        """Loads the skills database from the JSON file."""
        try:
            # Construct absolute path relative to this file
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, 'data', 'skills_database.json')
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading skills database: {e}")
            return {}

    def _flatten_skills(self):
        """
        Creates a simple set of all unique skills (lower-cased) for fast lookup.
        This handles keys like 'Amazon Web Services' mapping to 'AWS' in future versions,
        but for now, we just list everything.
        """
        flat_skills = set()
        for category, skills in self.skills_db.items():
            for skill in skills:
                flat_skills.add(skill.lower())
        return flat_skills

    def extract_skills(self, text):
        """
        Identifies skills in the provided text.
        Strategy:
        1. Preprocess text using NLP (lemmatize, etc.)
        2. Check for existence of multi-word skills (like 'Machine Learning') in raw text.
        3. Check for existence of single-word skills in tokenized text.
        """
        found_skills = {category: [] for category in self.skills_db.keys()}
        
        if not text:
            return found_skills

        # 1. Direct Text Search for Multi-word phrases (e.g., "Machine Learning", "C++")
        # We search in valid raw text (lowercased) to catch "C++" which might gets split by tokenizers
        text_lower = text.lower()
        
        # 2. NLP Token processing (good for stemming: 'Developing' -> 'Develop')
        # We look at tokens to find single words
        tokens = set(nlp_processor.preprocess_text(text))

        for category, skill_list in self.skills_db.items():
            for skill in skill_list:
                skill_lower = skill.lower()
                
                # Check 1: Exact match in tokens (Success for "Python", "Java")
                if skill_lower in tokens:
                    found_skills[category].append(skill)
                    continue
                
                # Check 2: Substring match for complex skills or special chars (Success for "C++", "Node.js")
                # Using regex to ensure word boundary, but allowing special chars where appropriate
                # E.g. search for "\bnode\.js\b"
                try:
                    # Escape special characters like +, . for regex
                    escaped_skill = re.escape(skill_lower)
                    # boundary check is tricky with C++, so we do a simpler check for special chars
                    if re.search(r'\b' + escaped_skill + r'\b', text_lower):
                         found_skills[category].append(skill)
                    elif skill_lower in text_lower and not skill_lower.isalpha():
                        # Fallback for things like C++ or C# where word boundaries fail
                         found_skills[category].append(skill)
                except re.error:
                    pass

        # Remove duplicates
        for category in found_skills:
            found_skills[category] = list(set(found_skills[category]))
            
        return found_skills

skill_extractor = SkillExtractor()
