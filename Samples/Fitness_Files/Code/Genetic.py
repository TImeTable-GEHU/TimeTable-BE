import random

class Timetable:
    def __init__(self):
        self.days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.sections = ["A", "B", "C", "D"]
        self.time_slots = [
            "9:00 A.M - 9:55 A.M",      
            "9:55 A.M - 10:50 A.M", 
            "10:50 A.M - 11:00 A.M (Break)",  # Morning Break
            "11:00 A.M - 11:55 A.M", 
            "11:55 A.M - 12:50 P.M", 
            "12:50 P.M - 1:00 P.M (Lunch Break)",  # Lunch Break
            "1:00 P.M - 2:00 P.M"
        ]
        
        # Subject-to-teacher mapping
        self.subject_teacher_map = {
            "Communication Models and Protocols": ["Mr. Anubhav Bewerval", "Mr. Prince Kumar"],
            "Operating Systems": ["Mr. Shashi Kumar Sharma", "Mr. Aviral Awasthi", "Mr. Akshay Choudhary"],
            "Database Management Systems": ["Mr. Shashi Kumar Sharma", "Ms. Senam Pandey", "Mr. Devesh Pandey", "Mr. Akshay Choudhary"],
            "DBMS Lab": ["Ms. Senam Pandey", "Ms. Vaishali Dev"],
            "Computer Based Numerical and Statistical Techniques": ["Dr. B P Joshi", "Mr. Rahul Singh", "Mr. JS Mehta", "Dr. Navneet Joshi"],
            "CBNST Lab": ["Mr. Parthak Mehra", "Mr. Ansh Dhingra", "Ms. Akshita Arya"],
            "Machine Learning": ["Dr. Shilpa Jain", "Dr. Ankur Singh Bist", "Ms. Heera Patwal", "Dr. Subhankar Ghosal"],
            "Career Skills": ["Mr. Divas Tewari", "Mr. Pawan Agarwal", "Mr. Narendra Bisht"],
            "Placement Classes": ["Mr. Ayush Kapri"],
            "Operating Systems Lab": ["Mr. Ansh Dhingra", "Ms. Rashmi Deopa"]
        }

        self.classrooms = ["R1", "R2", "R3", "R4", "R5"]
        self.teacher_work_load = {
            "Mr. Anubhav Bewerval": 4, "Mr. Shashi Kumar Sharma": 5, "Ms. Senam Pandey": 4,
            "Dr. B P Joshi": 3, "Dr. Shilpa Jain": 4, "Mr. Parthak Mehra": 4,
            "Mr. Ansh Dhingra": 3, "Mr. Divas Tewari": 5, "Mr. Pawan Agarwal": 5,
            "Mr. Devesh Pandey": 4, "Mr. Rahul Singh": 5, "Mr. Aviral Awasthi": 3,
            "Mr. JS Mehta": 4, "Dr. Ankur Singh Bist": 3, "Mr. Narendra Bisht": 5,
            "Mr. Ayush Kapri": 4, "Dr. Navneet Joshi": 3, "Ms. Heera Patwal": 4,
            "Ms. Akshita Arya" : 4, "Ms. Rashmi Deopa": 3, "Ms. Vaishali Dev": 4, 
            "Mr. Prince Kumar" : 4 , "Mr. Akshay Choudhary": 4, "Dr. Subhankar Ghosal": 4
        }
        self.room_capacity = {"R1": 250, "R2": 250, "R3": 200, "R4": 240, "R5": 250}
        self.section_strength = {"A": 200, "B": 200, "C": 200, "D": 200}

    def generate_day_schedule(self):
        day_schedule = {}
        for section in self.sections:
            section_schedule = []
            for time_slot in self.time_slots:
                if "Break" in time_slot:
                    # Handle breaks without assigning teachers or subjects
                    schedule_item = {
                        "teacher_id": "None",
                        "subject_id": "Break",
                        "classroom_id": "N/A",
                        "time_slot": time_slot
                    }
                else:
                    # Randomly choose a subject and assign a teacher who can teach it
                    subject = random.choice(list(self.subject_teacher_map.keys()))
                    teacher = random.choice(self.subject_teacher_map[subject])
                    classroom = random.choice(self.classrooms)
                    
                    schedule_item = {
                        "teacher_id": teacher,
                        "subject_id": subject,
                        "classroom_id": classroom,
                        "time_slot": time_slot
                    }
                section_schedule.append(schedule_item)
            day_schedule[section] = section_schedule
        return day_schedule

    def create_timetable(self):
        timetable = {}
        for day in self.days:
            timetable[day] = self.generate_day_schedule()
        return timetable

    def calculate_fitness(self, chromosome):
        overall_fitness_score = 0
        section_fitness_scores = {}

        for day, day_schedule in chromosome.items():
            section_fitness_scores[day] = {}
            for section, section_schedule in day_schedule.items():
                section_score = 100
                teacher_time_slots = {}
                classroom_time_slots = {}
                teacher_load = {}

                for item in section_schedule:
                    teacher = item['teacher_id']
                    classroom = item['classroom_id']
                    time_slot = item['time_slot']
                    strength = self.section_strength[section]

                    if "Break" in time_slot:
                        continue  # Skip breaks

                    # Check for teacher time slot clashes
                    if (teacher, time_slot) in teacher_time_slots:
                        section_score -= 30
                    else:
                        teacher_time_slots[(teacher, time_slot)] = section

                    # Check for classroom time slot clashes
                    if (classroom, time_slot) in classroom_time_slots:
                        section_score -= 20
                    else:
                        classroom_time_slots[(classroom, time_slot)] = section

                    # Count teacher load
                    if teacher not in teacher_load:
                        teacher_load[teacher] = []
                    teacher_load[teacher].append(time_slot)

                    # Check if section strength exceeds room capacity
                    if strength > self.room_capacity[classroom]:
                        section_score -= 25

                # Evaluate teacher maximum hours and consecutive classes
                for teacher, slots in teacher_load.items():
                    if len(slots) > self.teacher_work_load[teacher]:
                        section_score -= 15

                    for i in range(1, len(slots)):
                        if "Break" not in slots[i - 1] and "Break" not in slots[i]:
                            section_score -= 10

                section_fitness_scores[day][section] = max(section_score, 0)
                overall_fitness_score += max(section_score, 0)

        print("\n--- Section-wise Fitness Scores ---")
        for day, day_scores in section_fitness_scores.items():
            for section, score in day_scores.items():
                print(f"{day}, Section {section}: Fitness Score = {score}")

        print(f"\nOverall Fitness Score: {overall_fitness_score/20}")
        return overall_fitness_score

# Instantiate the Timetable class and generate a timetable
timetable_obj = Timetable()
chromosome = timetable_obj.create_timetable()
fitness = timetable_obj.calculate_fitness(chromosome)

# Display the generated timetable and its fitness score
for day, day_schedule in chromosome.items():
    print(f"--- {day} ---")
    for section, schedule in day_schedule.items():
        print(f" Section {section}:")
        for item in schedule:
            print(f"  Teacher: {item['teacher_id']}, Subject: {item['subject_id']}, Classroom: {item['classroom_id']}, Time Slot: {item['time_slot']}")
    print("\n" + "-" * 40 + "\n")

print("Final Fitness Score:", fitness/20)
