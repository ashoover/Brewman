# Brewman
**RaspberryPi Brew Management**

**Currently working:**
* Multi-Thermometer sensor checking
* Action (currently temperature) based relays power control
* Historical logging for each sensor in it's own file

**Stuff to be aware of**
1. Raspberry Pi relies on NTP for timing. (I use _ntpdate_)
2. Virtually unlimited temperature sensors, but limited by relays (Unless you switch over to I2c or some solution along those limes)
3. Currently just a script (I run mine in a _screen_ session)

**Plans & Features**
* Incorporate some kind of pretty graphs (InfluxDB/Grafana?)
* Internal web server to host dashboard (flask or cherrypy?)
* Push notifications (Pushover)
* Email notifications
* Web managed dashboard

**Equipment Used**
* [DS18B20 Temperature Probe](https://www.amazon.com/gp/product/B01DQQPR2A/ref=oh_aui_detailpage_o04_s01?ie=UTF8&psc=1)
* [8 Channel 5v Relay Switch Module](http://www.ebay.com/itm/2x-5v-Eight-8-Channel-DC-5V-Relay-Switch-Module-for-Arduino-Raspberry-Pi-ARM-AVR-/191690781601?hash=item2ca1a933a1:g:L4YAAOSwYlRZIGJ-)
* [Pre-Wired 12v Relay (because I'm lazy)](http://www.ebay.com/itm/5mm-Amber-Orange-12-Volt-Pre-Wired-LEDs-Qty-10-12V-Leds-with-Resistors-USA-/261817014773?hash=item3cf58299f5:g:0esAAOxy4fVTEjvJ&vxp=mtr)