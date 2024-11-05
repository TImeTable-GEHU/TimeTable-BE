from datetime import datetime
from constants.TimeIntervals import TimeIntervalConstant


class TimeSlotUtils:
    """
        - Utility class for working with time slots and intervals.
        - Contains methods for converting between time intervals and slot numbers.
        - Works with 12-hour time formats.
        - Data is stored in the TimeIntervalConstant class.
    """

    time_slots = TimeIntervalConstant.time_slots

    @classmethod
    def get_slot_number(cls, start_time:str, end_time:str):
        """Get the slot number for a given start and end time."""

        if start_time == "Invalid time format" or end_time == "Invalid time format":
            return "Invalid time format"

        # Remove the seconds from the time
        start_time = ":".join(start_time.split(":")[:2])
        end_time = ":".join(end_time.split(":")[:2])


        # Construct time interval string
        time_interval = f"{start_time} - {end_time}"
        try:
            start_time_interval = datetime.strptime(time_interval.split(" - ")[0], "%H:%M").time()
            end_interval_time = datetime.strptime(time_interval.split(" - ")[1], "%H:%M").time()
            """Find the slot corresponding to a given time interval, handling leading zeros."""
            for slot, interval in cls.time_slots.items():
                data_start_time = datetime.strptime(interval.split(" - ")[0], "%H:%M").time()
                data_end_time = datetime.strptime(interval.split(" - ")[1], "%H:%M").time()
                if data_start_time == start_time_interval and data_end_time == end_interval_time:
                    return slot
            return None  # Return None if the interval doesn't match any slot
        except:
            return "Invalid time format"


    @classmethod
    def get_time_interval(cls, slot_number:int) -> str:
        """Get the time interval for a given slot number."""
        return cls.time_slots.get(slot_number, "Invalid slot number")



if __name__ == "__main__":
    # Example usage
    print(TimeSlotUtils.get_slot_number("09:00", "09:55"))  # Output: 1
    print(TimeSlotUtils.get_time_interval(1))                                       # Output: "9:00 - 9:55"
    print(TimeSlotUtils.get_time_interval(5))                                       # Output: "1:20 - 2:15"
    print(TimeSlotUtils.get_slot_number("09:00", "2:55"))
