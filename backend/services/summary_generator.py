class SummaryGenerator:
    def generate_summary(self, role, top_skills):
        """
        Generates a professional summary statement.
        Args:
            role (str): The target or best-fit role (e.g., "Java Developer").
            top_skills (list): A list of key skills (e.g., ["Java", "Spring", "SQL"]).
        Returns:
            str: A formatted summary paragraph.
        """
        if not role or not top_skills:
            return "Professional with a strong technical background seeking new opportunities."
            
        skills_str = ", ".join(top_skills[:3])
        
        # Simple template-based generation
        summary = (
            f"Results-driven {role} with expertise in {skills_str}. "
            f"Proven ability to build scalable applications and solve complex technical challenges. "
            f"Passionate about leveraging {top_skills[0] if top_skills else 'technology'} to drive business success."
        )
        
        return summary

summary_generator = SummaryGenerator()
