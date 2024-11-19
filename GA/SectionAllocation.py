import random
from collections import defaultdict
from Constants.constant import SectionsConstants

class StudentScorer:
    def __init__(self, attribute_weights=SectionsConstants.ATTRIBUTE_WEIGHTS):
        self.attribute_weights = attribute_weights

    def calculate_dynamic_cgpa_threshold(self, students, top_percentage=30):
        """Calculate the CGPA threshold as the top X%."""
        sorted_cgpas = sorted([student['CGPA'] for student in students], reverse=True)
        threshold_index = max(1, int(len(sorted_cgpas) * top_percentage / 100)) - 1
        return sorted_cgpas[threshold_index]

    def assign_dynamic_conditions(self, cgpa_threshold):
        """Assign dynamic conditions for CGPA."""
        SectionsConstants.ATTRIBUTE_CONDITIONS['good_cgpa'] = lambda student: student['CGPA'] >= cgpa_threshold

    def calculate_student_binary_score(self, student):
        """Calculate the binary score for a student based on defined attributes and conditions."""
        score = 0
        for attribute, weight in self.attribute_weights.items():
            if SectionsConstants.ATTRIBUTE_CONDITIONS.get(attribute, lambda x: False)(student):
                score += weight
        return score

    def assign_scores_to_students(self, students):
        """Assign binary scores to a list of students."""
        for student in students:
            student['Score'] = self.calculate_student_binary_score(student)
        return students

    def divide_students_into_sections(self, students, class_strength):
            """Divide students into sections based on their scores and class strength."""
            grouped_by_score = defaultdict(list)
            for student in students:
                grouped_by_score[student['Score']].append(student)

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
    num_students = 500
    students = [
        {
            'ID': i,
            'CGPA': round(random.uniform(6.0, 9.8), 2),
            'Hostler': random.choice([True, False])
        }
        for i in range(1, num_students + 1)
    ]
    cgpa_threshold = scorer.calculate_dynamic_cgpa_threshold(students, top_percentage=30)
    print(f"Dynamic CGPA Threshold (Top 30%): {cgpa_threshold}")

    # Assign the dynamic condition for CGPA
    scorer.assign_dynamic_conditions(cgpa_threshold)

    # Assign scores to students
    students_with_scores = scorer.assign_scores_to_students(students)

    # Divide students into sections with a maximum class strength
    class_strength = 50
    sections = scorer.divide_students_into_sections(students_with_scores, class_strength)

    # Display the sections
    for i, section in enumerate(sections, 1):
        print(f"Section {i} (Total Students: {len(section)}):")
        for student in section:
            print(f"  Student ID: {student['ID']}, CGPA: {student['CGPA']}, Hostler: {student['Hostler']}, Score: {student['Score']}")
