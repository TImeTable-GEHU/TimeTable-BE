import csv
import io
import json


def csv_to_json(file):
    file.seek(0)  # Ensure the file pointer is at the beginning
    reader = list(
        csv.reader(io.StringIO(file.read().decode("utf-8")))
    )  # Read uploaded file
    time_slots = reader[0][1:]
    timetable = {}

    # Iterate through the CSV rows, skipping the first row (header)
    for i in range(1, len(reader), 2):
        day = reader[i][0].strip()
        if not day:
            continue

        timetable[day] = {}  # Initialize empty dictionary for each day
        subjects = reader[i][1:]
        teachers = reader[i + 1][1:] if i + 1 < len(reader) else []

        # Create sections for each subject
        for j, subject in enumerate(subjects):
            subject = subject.strip()
            if subject and subject not in ["BREAK", "LUNCH"]:
                # Assuming each day can have multiple sections
                section_key = f"Section {j + 1}"

                if section_key not in timetable[day]:
                    timetable[day][section_key] = []

                timetable[day][section_key].append(
                    {
                        "teacher_id": (
                            teachers[j].strip()
                            if j < len(teachers) and teachers[j]
                            else "Unknown"
                        ),
                        "subject_id": subject,
                        "classroom_id": f"R{j+1}",
                        "time_slot": time_slots[j],
                    }
                )

    return json.dumps(timetable, indent=2)


def json_to_csv(json_file, csv_file):
    with open(json_file, "r", encoding="utf-8") as file:
        timetable = json.load(file)

    time_slots = set()
    for day in timetable.values():
        for entry in day:
            time_slots.add(entry["time_slot"])
    time_slots = sorted(time_slots)

    header = ["DAY \\ TIME"] + time_slots
    rows = []

    for day, slots in timetable.items():
        subjects_row = [day] + [""] * len(time_slots)
        teachers_row = [""] + [""] * len(time_slots)

        for entry in slots:
            index = time_slots.index(entry["time_slot"]) + 1
            subjects_row[index] = entry["subject_id"]
            teachers_row[index] = entry["teacher_id"]

        rows.append(subjects_row)
        rows.append(teachers_row)

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
