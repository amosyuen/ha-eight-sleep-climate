"""Constants for Eight Sleep Climate."""
from homeassistant.components.climate import DOMAIN as CLIMATE_PLATFORM

# Base component constants
DOMAIN = "eight_sleep_climate"

UNIQUE_ID_POSTFIX = ".climate"
CONF_EIGHT_SLEEP_DEVICE = "eight_sleep_state"

# Platforms
PLATFORMS = [CLIMATE_PLATFORM]
