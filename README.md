# Eight Sleep Climate

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

## Purpose

Creates a virtual climate that controls an eight sleep mattress. This allows exposing the climate to google home and controlling it using voice commands. Currently the units is "percent" but will show as default home assistant temperature unit. This implementation is a bit of a hack since google isn't really designed to handle percent in a thermostat so there are some things that do not work.

## Google Assitant

### Queries Supported

- "what is <device> temperature"
- "set <device> heat to -100"
- "set <device> heat to -45 degrees"
- "set <device> temperature to 0"

### Queries Unsupported

- "what is <device> heat"
- "set <device> cool to -100 degrees"
- "set <device> to -100"
- "set <device> temperature to -100 degrees"

### UI

The Google Assistant UI is limited to setting temperature between 50 to 90 degrees. It is not recommended to use the Google Home UI. Instead I recommend exposing virtual fan or switch to use in the Google Home UI.

### Climate Attributes Supported

| Attribute           | Example Values (comma separated) |
| ------------------- | -------------------------------- |
| state               | cooling, heating, idle, off      |
| hvac_mode           | auto, off                        |
| current_temperature | 70                               |
| target_temperature  | 70                               |

### Services

## Installation

### HACS

1. Install [HACS](https://hacs.xyz/)
2. Go to HACS `Integrations >` section
3. Click `...` in top right of screen
4. Click `Custom repositories`
5. Add repository `amosyuen/ha-eight-sleep-climate` in category `Integration`
6. In the lower right click "+ Explore & Download repositories"
7. Search for "Eight Sleep Climate" and add it
   - HA Restart is not needed since it is configured in UI config flow
8. In the Home Assistant (HA) UI go to "Configuration"
9. Click "Integrations"
10. Click "+ Add Integration"
11. Search for "Eight Sleep Climate"

### Manual

1. Using the tool of choice open the directory (folder) for your [HA configuration](https://www.home-assistant.io/docs/configuration/) (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `eight_sleep_climate`.
4. Download _all_ the files from the `custom_components/eight_sleep_climate/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the Home Assistant (HA) UI go to "Configuration"
8. Click "Integrations"
9. Click "+ Add Integration"
10. Search for "Eight Sleep Climate"

{% endif %}

## Configuration

1. Setup Home Assistant [Eight Sleep](https://www.home-assistant.io/integrations/eight_sleep/) integration
2. The integration will automatically discover unadded eight sleep state entities. Select one.
3. Choose a name for the entity
4. Click `Submit`

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://paypal.me/amosyuen?country.x=US&locale.x=en_US
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/amosyuen/ha-eight-sleep-climate.svg?style=for-the-badge
[commits]: https://github.com/amosyuen/ha-eight-sleep-climate/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/amosyuen/ha-eight-sleep-climate.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40amosyuen-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/amosyuen/ha-eight-sleep-climate.svg?style=for-the-badge
[releases]: https://github.com/amosyuen/ha-eight-sleep-climate/releases
[user_profile]: https://github.com/amosyuen
