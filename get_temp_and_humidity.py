#! /usr/bin/env python3

# Note: Ensure that the user running this script is a member of the `gpio` group.
# sudo usermod -a -G gpio dd-agent
# Note: Install the Adafruit_DHT module to the DD embedded python
# sudo -Hu dd-agent /opt/datadog-agent/embedded/bin/pip3 install Adafruit_DHT

from datadog_checks.base import AgentCheck
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
OUTSIDE_DHT_PIN = 4  # GPIO4 is pin 7
INSIDE_DHT_PIN = 24  # GPIO22 is pin 15

inside_humidity, inside_temperature = Adafruit_DHT.read_retry(
    DHT_SENSOR, INSIDE_DHT_PIN, retries=3, delay_seconds=2
)
outside_humidity, outside_temperature = Adafruit_DHT.read_retry(
    DHT_SENSOR, OUTSIDE_DHT_PIN, retries=3, delay_seconds=2
)


class TempHumidityCheck(AgentCheck):
    def check(self, instance):
        self.gauge("home.inside.temp", inside_temperature)
        self.gauge("home.inside.humidity", inside_humidity)
        self.gauge("home.outside.temp", outside_temperature)
        self.gauge("home.outside.humidity", outside_humidity)
