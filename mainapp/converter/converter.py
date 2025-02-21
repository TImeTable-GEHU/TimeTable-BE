import csv
import io
import json
import os

def csv_to_json(file):
    file.seek(0)  # Ensure the file pointer is at the beginning
    reader = list(csv.reader(io.StringIO(file.read().decode("utf-8"))))

    # Identify the starting row for timetable data
    start_index = None
    for i, row in enumerate(reader):
        if row and "DAY" in row[0].upper():
            start_index = i
            break

    if start_index is None:
        return json.dumps({"error": "No valid timetable structure found"}, indent=2)

    reader = reader[start_index:]  # Skip metadata rows
    time_slots = [slot.strip() for slot in reader[0][1:] if slot.strip()]
    timetable = {}

    weekdays = {
        "MONDAY",
        "TUESDAY",
        "WEDNESDAY",
        "THURSDAY",
        "FRIDAY",
    }

    for i in range(
        1, len(reader), 2
    ):  # Iterate two rows at a time (subjects and teachers)
        if i + 1 < len(reader):  # Ensure the next row exists
            day = reader[i][0].strip().upper()
            if day not in weekdays:
                continue  # Skip rows that are not part of the main weekday schedule

            timetable[day] = []  # Initialize list for day's classes
            subjects = [
                cell.split("(")[0].strip()
                for cell in reader[i][1 : len(time_slots) + 1]
            ]  # Remove extra mapping info
            teachers = reader[i + 1][1 : len(time_slots) + 1]

            for j, subject in enumerate(subjects):
                subject = subject.strip()
                if subject and subject not in ["BREAK", "LUNCH", ""]:
                    timetable[day].append(
                        {
                            "teacher_id": (
                                teachers[j].strip()
                                if j < len(teachers) and teachers[j]
                                else "Unknown"
                            ),
                            "subject_id": subject,
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


def extract_time_slots_for_teacher(timetable, time_slot_order):
    """Extract and sort time slots dynamically based on backend input."""
    unique_slots = {entry["time_slot"] for day_data in timetable.values() for slots in day_data.values() for entry in slots}
    sorted_slots = sorted(unique_slots, key=lambda slot: time_slot_order.get(slot, float('inf')))
    return [("CLASS", slot) for slot in sorted_slots]


def teacher_json_to_csv(teacher_timetable, output_folder, time_slots):
    """Convert teacher timetable dictionary to CSV with dynamic time slots."""
    os.makedirs(output_folder, exist_ok=True)
    time_slot_order = {v: k for k, v in time_slots.items()}
    days_of_week_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for teacher_id, schedule in teacher_timetable.items():
        final_slots = extract_time_slots(schedule, time_slot_order)
        csv_file = os.path.join(output_folder, f"{teacher_id}.csv")
        header = ["DAY"] + [slot[1] for slot in final_slots]
        rows = []

        sorted_days = sorted(schedule.items(), key=lambda x: days_of_week_order.index(x[0]))

        for day, day_data in sorted_days:
            row = [day] + ["" for _ in final_slots]
            
            for section, classes in day_data.items():
                for entry in classes:
                    for i, slot in enumerate(final_slots):
                        if entry["time_slot"] == slot[1]:
                            row[i + 1] = f"{entry['subject_id']} ({section}, {entry['classroom_id']})"
            
            rows.append(row)

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)
            
            
    
def extract_time_slots_for_clasroom(timetable, time_slot_order):
    """Extract and sort time slots from the timetable based on a predefined order."""
    unique_slots = set()
  
    # Collect all unique time slots
    for day_data in timetable.values():
        for slots in day_data.values():
            for entry in slots:
                if isinstance(entry, dict) and "time_slot" in entry:
                    unique_slots.add(entry["time_slot"])
                else:
                    print(f"⚠️ ERROR: Unexpected entry format -> {entry}")

    sorted_slots = sorted(unique_slots, key=lambda slot: time_slot_order.get(slot, float('inf')))
    
    return [("CLASS", slot) for slot in sorted_slots]

def classroom_json_to_csv(classroom_timetable, output_folder, time_slot_order):
    """Convert classroom timetable JSON to CSV."""
    os.makedirs(output_folder, exist_ok=True)
    time_slot_order = {v: k for k, v in time_slots.items()}
    days_of_week_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] 
    for classroom_id, schedule in classroom_timetable.items():
        final_slots = extract_time_slots(schedule, time_slot_order)
        csv_file = os.path.join(output_folder, f"{classroom_id}.csv")
        header = ["DAY"] + [slot[1] for slot in final_slots]
        rows = []

        # Sort days correctly
        sorted_days = sorted(schedule.items(), key=lambda x: days_of_week_order.index(x[0]) if x[0] in days_of_week_order else float('inf'))

        for day, day_data in sorted_days:
            row = [day] + ["" for _ in final_slots]  # Empty slots initially
            
            for section, classes in day_data.items():
                for entry in classes:
                    for i, slot in enumerate(final_slots):
                        if entry["time_slot"] == slot[1]:
                            row[i + 1] = f"{entry['subject_id']} ({section}, {entry['teacher_id']})"
            
            rows.append(row)

        # Write to CSV
        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)