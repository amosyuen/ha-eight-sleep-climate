"""Utils."""
import bisect

from homeassistant.const import UnitOfTemperature

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
        """Convert Eight Sleep Raw Temp (both F and C depending on the HA Config in Preferences)
           to Degres (either in F and C depending on the HA Config in Preferences)
           This method uses interpolation to determine the degree.
        """
        unit_map = RAW_TO_FAHRENHEIT_MAP

        if degree_unit == UnitOfTemperature.CELSIUS:
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
        """Convert Degrees (either F and C depending on the HA Config in Preferences)
           to  Eight Sleep Raw Temp. This method uses reverse interpolation to determine the
           raw temp.
        """

        unit_map = RAW_TO_FAHRENHEIT_MAP

        if degree_unit == UnitOfTemperature.CELSIUS:
            unit_map = RAW_TO_CELSIUS_MAP

        temp_raw_map = {v: k for k, v in unit_map.items()}

        # Sorted temperature values for binary search
        temp_keys = sorted(temp_raw_map.keys())  # [55, 56, 57, 58, ...]

        # Find index where degree_val would be inserted
        insertion_index = bisect.bisect_left(temp_keys, degree_val)  # Returns index where degree_val fits

        # Get nearest known values
        temp_low, temp_high = temp_keys[insertion_index - 1], temp_keys[insertion_index]
        raw_low, raw_high = temp_raw_map[temp_low], temp_raw_map[temp_high]

        # Peform Linear Interpolation
        ratio = (degree_val- temp_low) / (temp_high - temp_low)
        interpolated_raw = raw_low + ratio * (raw_high - raw_low)

        return interpolated_raw

