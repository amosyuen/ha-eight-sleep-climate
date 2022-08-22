"""Adds config flow for Eight Sleep Climate."""
import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .const import CONF_EIGHT_SLEEP_STATE
from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)


def _get_schema(data: dict[str:Any]):
    if data is None:
        data = {}
    return vol.Schema(
        {
            vol.Required(CONF_NAME, default=data.get(CONF_NAME)): cv.string,
            vol.Required(
                CONF_EIGHT_SLEEP_STATE, data.get(CONF_EIGHT_SLEEP_STATE)
            ): cv.entity_id,
        }
    )


class RoomPresenceFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for eight_sleep_climate."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=_get_schema(user_input),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        return RoomPresenceOptionsFlowHandler(config_entry)


class RoomPresenceOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for eight_sleep_climate."""

    def __init__(self, config_entry: ConfigEntry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.data = dict(config_entry.data)
        self._errors = {}

    async def async_step_init(self, user_input: dict[str:Any] = None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            self.data.update(user_input)
            return self.async_create_entry(
                title=self.config_entry.data.get(CONF_NAME), data=self.data
            )

        return self.async_show_form(
            step_id="init",
            data_schema=_get_schema(self.data),
            errors=self._errors,
        )
