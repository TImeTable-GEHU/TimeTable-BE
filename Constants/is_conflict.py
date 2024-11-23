import psycopg2

conn = psycopg2.connect(
    dbname="timetable",          
    user="postgres",         
    password="root",   
    host="localhost",           
    port="5432"                
)
cursor = conn.cursor()
print("Connected to PostgreSQL database!")

def insert_schedule(chromosome_name, timetable):
    try:
        for day, sections in timetable.items():
            for section, classes in sections.items():
                for cls in classes:
                    cursor.execute("""
                        INSERT INTO schedule (chromosome, day, section, teacher_id, subject_id, classroom_id, time_slot)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (chromosome_name, day, section, cls['teacher_id'], cls['subject_id'], cls['classroom_id'], cls['time_slot']))
        
        conn.commit()
        print(f"New data for {chromosome_name} inserted successfully.")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

def detect_teacher_conflicts():
    cursor.execute("""
        SELECT s1.teacher_id, s1.day, s1.time_slot, COUNT(*)
        FROM schedule s1
        JOIN schedule s2
        ON s1.teacher_id = s2.teacher_id
           AND s1.time_slot = s2.time_slot
           AND s1.day = s2.day
           AND s1.chromosome != s2.chromosome
        GROUP BY s1.teacher_id, s1.day, s1.time_slot
        HAVING COUNT(*) > 1;
    """)
    return cursor.fetchall()

def detect_classroom_conflicts():
    cursor.execute("""
        SELECT s1.classroom_id, s1.day, s1.time_slot, COUNT(*)
        FROM schedule s1
        JOIN schedule s2
        ON s1.classroom_id = s2.classroom_id
           AND s1.time_slot = s2.time_slot
           AND s1.day = s2.day
           AND s1.chromosome != s2.chromosome
        GROUP BY s1.classroom_id, s1.day, s1.time_slot
        HAVING COUNT(*) > 1;
    """)
    return cursor.fetchall()

chromosome1 = {
    "Monday": {
        "A": [
            {"teacher_id": "AP24", "subject_id": "SCS-501", "classroom_id": "R1", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "SP06", "subject_id": "TCS-503", "classroom_id": "R1", "time_slot": "9:55 - 10:50"}
        ],
        "B": [
            {"teacher_id": "RS11", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "9:00 - 9:55"}
        ]
    }
}

chromosome2 = {
    "Monday": {
        "A": [
            {"teacher_id": "AP24", "subject_id": "SCS-501", "classroom_id": "R1", "time_slot": "9:00 - 9:55"},
            {"teacher_id": "DP07", "subject_id": "TCS-503", "classroom_id": "R3", "time_slot": "9:00 - 9:55"}
        ],
        "B": [
            {"teacher_id": "RS11", "subject_id": "TMA-502", "classroom_id": "R2", "time_slot": "9:00 - 9:55"}
        ]
    }
}

#without conflict sample
# chromosome1 = {
#     "Monday": {
#         "A": [
#             {"teacher_id": "T01", "subject_id": "MATH-101", "classroom_id": "R1", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T02", "subject_id": "ENG-201", "classroom_id": "R1", "time_slot": "10:00 - 10:55"}
#         ],
#         "B": [
#             {"teacher_id": "T03", "subject_id": "SCI-301", "classroom_id": "R2", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T04", "subject_id": "HIST-401", "classroom_id": "R2", "time_slot": "10:00 - 10:55"}
#         ]
#     },
#     "Tuesday": {
#         "A": [
#             {"teacher_id": "T01", "subject_id": "PHY-101", "classroom_id": "R1", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T02", "subject_id": "CHEM-102", "classroom_id": "R1", "time_slot": "10:00 - 10:55"}
#         ],
#         "B": [
#             {"teacher_id": "T03", "subject_id": "BIO-201", "classroom_id": "R2", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T04", "subject_id": "COMP-202", "classroom_id": "R2", "time_slot": "10:00 - 10:55"}
#         ]
#     }
# }

# chromosome2= {
#     "Monday": {
#         "A": [
#             {"teacher_id": "T05", "subject_id": "ART-501", "classroom_id": "R3", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T06", "subject_id": "MUS-601", "classroom_id": "R3", "time_slot": "10:00 - 10:55"}
#         ],
#         "B": [
#             {"teacher_id": "T07", "subject_id": "PHIL-701", "classroom_id": "R4", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T08", "subject_id": "LANG-801", "classroom_id": "R4", "time_slot": "10:00 - 10:55"}
#         ]
#     },
#     "Tuesday": {
#         "A": [
#             {"teacher_id": "T05", "subject_id": "DESIGN-401", "classroom_id": "R3", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T06", "subject_id": "DANCE-601", "classroom_id": "R3", "time_slot": "10:00 - 10:55"}
#         ],
#         "B": [
#             {"teacher_id": "T07", "subject_id": "LIT-101", "classroom_id": "R4", "time_slot": "9:00 - 9:55"},
#             {"teacher_id": "T08", "subject_id": "GEOG-201", "classroom_id": "R4", "time_slot": "10:00 - 10:55"}
#         ]
#     }
# }


insert_schedule("Week 1", chromosome1)  
teacher_conflicts_week1 = detect_teacher_conflicts()
classroom_conflicts_week1 = detect_classroom_conflicts()


insert_schedule("Week 2", chromosome2)  
teacher_conflicts_week2 = detect_teacher_conflicts()
classroom_conflicts_week2 = detect_classroom_conflicts()



teacher_conflicts_between_weeks = detect_teacher_conflicts()
classroom_conflicts_between_weeks = detect_classroom_conflicts()

print("Teacher Conflicts Between Weeks:", teacher_conflicts_between_weeks)
print("Classroom Conflicts Between Weeks:", classroom_conflicts_between_weeks)

# cursor.execute("TRUNCATE TABLE schedule;")
conn.commit()
print("Schedule table cleared successfully.")

cursor.close()
conn.close()
