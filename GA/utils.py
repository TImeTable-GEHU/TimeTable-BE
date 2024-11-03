from datetime import datetime

class Utils:
    # Dictionary mapping slot numbers to time intervals in 12-hour format
    time_slots = {
        1: "9:00 - 9:55",
        2: "9:55 - 10:50",
        3: "11:10 - 12:05",
        4: "12:05 - 1:00",
        5: "1:20 - 2:15",
        6: "2:15 - 3:10",
        7: "3:30 - 4:25",
    }

    @staticmethod
    def convert_to_12_hour_format(time_24):
        """Convert 24-hour time format to 12-hour format with AM/PM using datetime."""
        time_obj = datetime.strptime(time_24, "%H:%M")
        return time_obj.strftime("%I:%M")


    @classmethod
    def get_slot_number(cls, start_time, end_time, is_24_hour_format=False):
        """Get the slot number for a given start and end time, optionally converting from 24-hour to 12-hour format."""
        # Convert to 12-hour format if needed
        if is_24_hour_format:
            start_time = cls.convert_to_12_hour_format(start_time)
            end_time = cls.convert_to_12_hour_format(end_time)

        # Construct time interval string
        time_interval = f"{start_time} - {end_time}"
        start_time_interval = datetime.strptime(time_interval.split(" - ")[0], "%H:%M").time()
        end_interval_time = datetime.strptime(time_interval.split(" - ")[1], "%H:%M").time()
        """Find the slot corresponding to a given time interval, handling leading zeros."""
        for slot, interval in cls.time_slots.items():
            start_time = datetime.strptime(interval.split(" - ")[0], "%H:%M").time()
            end_time = datetime.strptime(interval.split(" - ")[1], "%H:%M").time()
            if start_time == start_time_interval and end_time == end_interval_time:
                return slot
        return None  # Return None if the interval doesn't match any slot
    @classmethod
    def get_time_interval(cls, slot_number):
        """Get the time interval for a given slot number."""
        return cls.time_slots.get(slot_number, "Invalid slot number")



if __name__ == "__main__":
    # Example usage
    print(Utils.get_slot_number("09:00", "09:55", is_24_hour_format=False))  # Output: 1
    print(Utils.get_time_interval(1))                                       # Output: "9:00 - 9:55"
    print(Utils.get_time_interval(5))                                       # Output: "1:20 - 2:15"
    print(Utils.get_slot_number("13:20", "14:15", is_24_hour_format=True))  # Convert 13:30-14:25 to 1:30-2:25 PM
