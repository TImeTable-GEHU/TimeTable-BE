import random
from collections import defaultdict
from constants.constant import SectionsConstants

class StudentScorer:
    def __init__(self, attribute_weights=SectionsConstants.ATTRIBUTE_WEIGHTS, attribute_conditions=SectionsConstants.ATTRIBUTE_CONDITIONS):
        self.attribute_weights = attribute_weights
        self.attribute_conditions = attribute_conditions

    def calculate_student_score(self, student):
        """Calculate the binary score for a student based on defined attributes and conditions."""
        score = 0
        for attribute, weight in self.attribute_weights.items():
            if self.attribute_conditions[attribute](student):
                score += weight
        return score

    def assign_scores_to_students(self, students):
        """Assign binary scores to a list of students."""
        for student in students:
            student['Score'] = self.calculate_student_score(student)
        return students

    def generate_students(self, num_students=500):
        """Generate random student data."""
        return [
            {
                'ID': i,
                'CGPA': round(random.uniform(6.0, 9.8), 2),
                'Hostler': random.choice([True, False])
            }
            for i in range(1, num_students + 1)
        ]
    def divide_students_into_sections(self, students, class_strength):
        """Divide students into sections based on their scores and class strength."""
        # Group students by score
        grouped_by_score = defaultdict(list)
        for student in students:
            grouped_by_score[student['Score']].append(student)

        # Distribute students into sections, keeping same-score students together
        sections = []
        current_section = []

        for score_group in grouped_by_score.values():
            for student in score_group:
                if len(current_section) < class_strength:
                    current_section.append(student)
                else:
                    sections.append(current_section)
                    current_section = [student]

        if current_section:
            sections.append(current_section)

        return sections


if __name__ == "__main__":
    scorer = StudentScorer()

    # Generate students and assign scores
    students = scorer.generate_students(500)  # Example with 10 students
    students_with_scores = scorer.assign_scores_to_students(students)

    # Divide students into sections with a maximum class strength
    class_strength = 100
    sections = scorer.divide_students_into_sections(students_with_scores, class_strength)

    # Display the sections
    for i, section in enumerate(sections, 1):
        print(f"Section {i} (Total Students: {len(section)}):")
        for student in section:
            print(f"  Student ID: {student['ID']}, CGPA: {student['CGPA']}, Hostler: {student['Hostler']}, Score: {student['Score']}")
