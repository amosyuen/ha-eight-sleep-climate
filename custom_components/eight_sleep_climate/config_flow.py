"""Adds config flow for Eight Sleep Climate."""
import logging
from typing import Dict
from typing import List
from typing import Set

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.climate import DOMAIN as CLIMATE_PLATFORM
from homeassistant.components.eight_sleep.const import DOMAIN as EIGHT_SLEEP_DOMAIN
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry
from homeassistant.helpers import entity_platform
from homeassistant.helpers.device_registry import DeviceEntry

from .const import CONF_EIGHT_SLEEP_DEVICE
from .const import DOMAIN
from .util import add_unique_id_postfix
from .util import remove_unique_id_postfix

CONF_PASSWORD = "password"
CONF_USERNAME = "username"

_LOGGER: logging.Logger = logging.getLogger(__package__)


class EightSleepClimateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for eight_sleep_climate."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._data = {}
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Select eight sleep device."""
        self._errors = {}

        devices = _get_eight_sleep_devices(self.hass)
        if user_input is not None:
            device_id = user_input[CONF_EIGHT_SLEEP_DEVICE]
            unique_id = add_unique_id_postfix(device_id)
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            name = devices[device_id]

            return self.async_create_entry(title=name, data={CONF_NAME: name})

        if len(devices) == 0:
            self._errors = {CONF_EIGHT_SLEEP_DEVICE: "no_devices"}

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_EIGHT_SLEEP_DEVICE): vol.In(devices),
                }
            ),
            errors=self._errors,
        )


def _get_eight_sleep_devices(hass: HomeAssistant) -> List[DeviceEntry]:
    """Return the devices associated with a given config entry."""
    platforms = entity_platform.async_get_platforms(hass, "eight_sleep_climate")
    existing_unique_ids: Set[str] = set()
    for platform in platforms:
        if (
            platform.domain == CLIMATE_PLATFORM
            and platform.config_entry.state != ConfigEntryState.NOT_LOADED
        ):
            eight_sleep_unique_id = remove_unique_id_postfix(
                platform.config_entry.unique_id
            )
            existing_unique_ids.add(eight_sleep_unique_id)
            _LOGGER.debug("Found existing config: %s", eight_sleep_unique_id)

    eight_sleep_devices: Dict[str, str] = {}
    for device in device_registry.async_get(hass).devices.values():
        if device.manufacturer == "Eight Sleep" and device.via_device_id is not None:
            unique_id = get_eight_sleep_id(device)
            if unique_id not in existing_unique_ids:
                _LOGGER.debug("Found eight sleep device: %s", device)
                eight_sleep_devices[unique_id] = _get_device_name(device)
    return eight_sleep_devices


def get_eight_sleep_id(device):
    for id in device.identifiers:
        if id[0] == EIGHT_SLEEP_DOMAIN:
            return id[1]
    return None


def _get_device_name(device):
    return device.name_by_user or device.name
