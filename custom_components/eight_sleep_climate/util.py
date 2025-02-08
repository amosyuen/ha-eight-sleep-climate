"""Utils."""
import bisect

from .const import RAW_TO_CELSIUS_MAP, RAW_TO_FAHRENHEIT_MAP, UNIQUE_ID_POSTFIX


def add_unique_id_postfix(unique_id):
    """Add unique ID postfix"""
    return unique_id + UNIQUE_ID_POSTFIX


def remove_unique_id_postfix(unique_id):
    """Remove unique ID postfix"""
    return unique_id[0 : -len(UNIQUE_ID_POSTFIX)]

class DegreeConversion:
    @staticmethod
    def convert_raw_temp_degrees(raw_val, degree_unit):

        unit_map = RAW_TO_FAHRENHEIT_MAP

        if degree_unit == "c":
            unit_map = RAW_TO_CELSIUS_MAP

        if raw_val in unit_map:
            return float(unit_map[raw_val])

        # Convert mapping keys to a sorted list for binary search
        raw_keys = sorted(unit_map.keys())

        insertion_index = bisect.bisect_left(raw_keys, raw_val)

        if insertion_index == 0 or insertion_index == len(raw_keys):
            raise ValueError(f"Raw value {raw_val} is out of expected range.")

        # Get the two closest mapped values
        raw_low, raw_high = raw_keys[insertion_index - 1], raw_keys[insertion_index]
        temp_low, temp_high = unit_map[raw_low], unit_map[raw_high]

        # Perform linear interpolation
        ratio = (raw_val - raw_low) / (raw_high - raw_low)
        interpolated_temp = temp_low + ratio * (temp_high - temp_low)

        return float(interpolated_temp)

    @staticmethod
    def convert_degree_to_raw_temp(degree_val, degree_unit):
        unit_map = RAW_TO_FAHRENHEIT_MAP

        if degree_unit == "c":
            unit_map = RAW_TO_CELSIUS_MAP

        temp_raw_map = {v: k for k, v in unit_map.items()}

        # Sorted temperature values for binary search
        temp_keys = sorted(temp_raw_map.keys())  # [55, 56, 57, 58, ...]

        # Find index where 57.6°F would be inserted
        idx = bisect.bisect_left(temp_keys, 57.6)  # Returns index where 57.6 fits

        # Get nearest known values
        temp_low, temp_high = temp_keys[idx - 1], temp_keys[idx]  # 57 and 58
        raw_low, raw_high = temp_raw_map[temp_low], temp_raw_map[temp_high]  # -97 and -95

        # Interpolation
        ratio = (57.6 - temp_low) / (temp_high - temp_low)  # 0.6
        interpolated_raw = raw_low + ratio * (raw_high - raw_low)  # -95.8

        return interpolated_raw

