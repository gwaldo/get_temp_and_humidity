#! /usr/bin/env python3

# Note: Ensure that the user running this script is a member of the `gpio` or `dialout` group.
# sudo usermod -a -G gpio dd-agent
# Note: Install the Adafruit_DHT module to the DD embedded python
# sudo -Hu dd-agent /opt/datadog-agent/embedded/bin/pip3 install Adafruit_DHT

from datadog_checks.base import AgentCheck
import Adafruit_DHT

__version__ = "1.1.0"

DHT_SENSOR = Adafruit_DHT.DHT22
OUTSIDE_DHT_PIN = 4  # GPIO4 is pin 7
INSIDE_DHT_PIN = 24  # GPIO22 is pin 15


def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


class TempHumidityCheck(AgentCheck):
    def check(self, instance):
        inside_humidity, inside_temperature_c = Adafruit_DHT.read_retry(
            DHT_SENSOR, INSIDE_DHT_PIN, retries=3, delay_seconds=2
        )
        outside_humidity, outside_temperature_c = Adafruit_DHT.read_retry(
            DHT_SENSOR, OUTSIDE_DHT_PIN, retries=3, delay_seconds=2
        )

        # if inside_humidity is not None:
        # do inside_humidity things
        # repeat...

        inside_temperature_f = celsius_to_fahrenheit(inside_temperature_c)
        outside_temperature_f = celsius_to_fahrenheit(outside_temperature_c)

        self.gauge("home.inside.temp.c", inside_temperature_c)
        self.gauge("home.inside.temp.f", inside_temperature_f)
        self.gauge("home.inside.humidity", inside_humidity)
        self.gauge("home.outside.temp.c", outside_temperature_c)
        self.gauge("home.outside.temp.f", outside_temperature_f)
        self.gauge("home.outside.humidity", outside_humidity)
