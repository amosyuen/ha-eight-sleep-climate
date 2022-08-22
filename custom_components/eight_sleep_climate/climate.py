"""Adds support for Eight Sleep thermostat units."""
import logging

from homeassistant.components.climate import (
    ClimateEntity,
)
from homeassistant.components.climate.const import ATTR_HVAC_MODE
from homeassistant.components.climate.const import ATTR_TARGET_TEMP
from homeassistant.components.climate.const import CURRENT_HVAC_COOL
from homeassistant.components.climate.const import CURRENT_HVAC_HEAT
from homeassistant.components.climate.const import CURRENT_HVAC_IDLE
from homeassistant.components.climate.const import CURRENT_HVAC_OFF
from homeassistant.components.climate.const import HVAC_MODE_AUTO
from homeassistant.components.climate.const import HVAC_MODE_OFF
from homeassistant.components.climate.const import SUPPORT_PRESET_MODE
from homeassistant.components.climate.const import SUPPORT_TARGET_TEMPERATURE
from homeassistant.components.eight_sleep.const import ATTR_DURATION
from homeassistant.components.eight_sleep.const import ATTR_TARGET
from homeassistant.components.eight_sleep.const import DOMAIN as EIGHT_SLEEP_PLATFORM
from homeassistant.components.eight_sleep.const import SERVICE_HEAT_SET
from homeassistant.components.eight_sleep.sensor import ATTR_DURATION_HEAT
from homeassistant.components.eight_sleep.sensor import ATTR_TARGET_HEAT
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.const import CONF_NAME
from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import callback
from homeassistant.helpers.event import (
    async_track_state_change_event,
)
from homeassistant.helpers.restore_state import RestoreEntity

from . import CONF_EIGHT_SLEEP_STATE

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the eight sleep thermostat platform."""
    name = config.get(CONF_NAME)
    eight_sleep_state_entity_id = config.get(CONF_EIGHT_SLEEP_STATE)

    async_add_entities(
        [
            EightSleepThermostat(
                name,
                eight_sleep_state_entity_id,
                hass.config.units.temperature_unit,
            )
        ]
    )


class EightSleepThermostat(ClimateEntity, RestoreEntity):
    """Representation of a Eight Sleep Thermostat device."""

    def __init__(
        self,
        name,
        eight_sleep_state_entity_id,
        temperature_unit,
    ):
        """Initialize the thermostat."""
        self._eight_sleep_state_entity_id = eight_sleep_state_entity_id

        self._attr_hvac_mode = None
        self._attr_hvac_modes = [HVAC_MODE_AUTO, HVAC_MODE_OFF]
        self._attr_max_temp = 100
        self._attr_min_temp = -100
        self._attr_name = name
        self._attr_should_poll = False
        self._attr_target_temp = None
        self._attr_target_temp_step = 1
        self._attr_temperature_unit = temperature_unit

    async def async_added_to_hass(self):
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        if self._is_running():
            self._attr_target_temp = self._get_target_temp()
        else:
            # Restore old state
            old_state = await self.async_get_last_state()
            if old_state is not None:
                if self._attr_target_temp is None:
                    self._attr_target_temp = old_state.attributes.get(ATTR_TARGET_TEMP)
            if self._attr_target_temp is None:
                self._attr_target_temp = 10

        # Add listener
        async_track_state_change_event(
            self.hass, self._eight_sleep_state_entity_id, self._async_bed_state_changed
        )

    @property
    def available(self) -> bool:
        """Return true if the sensor and thermostate are available."""
        return not self.hass.states.is_state(
            self._eight_sleep_state_entity_id, STATE_UNAVAILABLE
        )

    @property
    def current_temperature(self):
        """Return the state temperature."""
        return self._get_eight_sleep_state().state

    @property
    def hvac_action(self):
        """Return the current running hvac operation.."""
        if not self._is_running():
            return CURRENT_HVAC_OFF

        diff = self.target_temperature - self.current_temperature
        if diff < 0:
            return CURRENT_HVAC_COOL
        if diff > 0:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE

    @property
    def state(self):
        """Return the state."""
        return HVAC_MODE_AUTO if self._is_running() else HVAC_MODE_OFF

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_PRESET_MODE & SUPPORT_TARGET_TEMPERATURE

    async def async_set_hvac_mode(self, hvac_mode):
        """Set hvac mode."""
        await self.async_set_temperature(hvac_mode=hvac_mode)

    async def async_set_temperature(self, **kwargs):
        """Set tempearture."""
        hvac_mode = self.hvac_mode
        if ATTR_TARGET_TEMP in kwargs:
            target_temp = int(kwargs[ATTR_TARGET_TEMP])
            if target_temp < -100 or target_temp > 100:
                _LOGGER.error(
                    "Target temp %d must be between -100 and 100 inclusive", target_temp
                )
                return False
            self._attr_target_temp = target_temp
        if ATTR_HVAC_MODE in kwargs:
            hvac_mode = kwargs[ATTR_HVAC_MODE]
            if hvac_mode not in self._attr_hvac_modes:
                _LOGGER.error("Unrecognized hvac mode: %s", hvac_mode)
                return False

        data = {
            ATTR_ENTITY_ID: self._eight_sleep_state_entity_id,
            ATTR_DURATION: 7200 if hvac_mode == HVAC_MODE_AUTO else 0,
            ATTR_TARGET: self._attr_target_temp,
        }
        _LOGGER.debug("_async_update_climate: Set heat data=%s", data)
        await self.hass.services.async_call(
            EIGHT_SLEEP_PLATFORM, SERVICE_HEAT_SET, data, False
        )

    async def async_turn_off(self):
        """Turn thermostat on."""
        self.async_set_temperature(hvac_mode=HVAC_MODE_OFF)

    async def async_turn_on(self):
        """Turn thermostat on."""
        self.async_set_temperature(hvac_mode=HVAC_MODE_AUTO)

    def _get_target_temp(self):
        return self._get_eight_sleep_state().attributes.get(ATTR_TARGET_HEAT)

    def _is_running(self):
        """Return whether the bed is running."""
        duration = self._get_eight_sleep_state().attributes.get(ATTR_DURATION_HEAT)
        return duration is not None and int(duration) > 0

    def _get_eight_sleep_state(self):
        return self.hass.states.get(self._eight_sleep_state_entity_id)

    @callback
    async def _async_bed_state_changed(self, event):
        """Handle bed state changes."""
        old_state = event.data.get("old_state")
        new_state = event.data.get("new_state")
        if new_state is None:
            return

        is_running_new = new_state.attributes.get(ATTR_DURATION) > 0
        if is_running_new:
            target_temp = new_state.attributes.get(ATTR_TARGET_HEAT) > 0
            if target_temp != self._attr_target_temp:
                self._attr_target_temp = target_temp
                self.async_schedule_update_ha_state()
                return

        is_running_old = old_state.attributes.get(ATTR_DURATION) > 0
        if is_running_new != is_running_old or new_state.state != old_state.state:
            self.async_schedule_update_ha_state()
