

class WorkingDays:
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class SectionsConstants:
    # Define attribute weights and conditions
    ATTRIBUTE_WEIGHTS = {
        'good_cgpa': 1,         # 2^0
        'hostler': 2,           # 2^1
        # Additional attributes can be added here
    }

    ATTRIBUTE_CONDITIONS = {
        'good_cgpa': lambda student: student['CGPA'],
        'hostler': lambda student: student['Hostler'],
        # Additional conditions can be added here
    }
