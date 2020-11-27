# Tally Arbiter WS28xx Listener
Tally Arbiter WS28xx Listener was written by 5pm-HDH, using the TallyArbiter-Blink1Listener from  josephdadams as Template and is distributed under the MIT License.

Tally Arbiter WS28xx Listener is an accessory program that allows you to connect to a Tally Arbiter server and control WS28xx LED Stripes based on the incoming tally information.

It is written in Python and designed to run on a Pi Zero with minimal configuration needed. It uses the `python-socketio[client]` library to communicate with the Tally Arbiter server.

To learn more about the Tally Arbiter project, [click here](http://github.com/josephdadams/tallyarbiter).

It is not sold, authorized, or associated with any other company or product.


## Getting Started
A lot of these instructions on getting started are available all over the internet. Some highlights are listed here that should cover it from a top-level:

1. The Raspberry Pi OS Lite version is sufficient for this use. You can download it here: https://www.raspberrypi.org/downloads/raspbian/
1. Use Balena Etcher to write the image to your microSD card: https://www.balena.io/etcher/
1. Once the image is written, mount the card to your computer and enable SSH by adding a blank file named `SSH` to the root of the `boot` volume oef the card. If you're using MacOS, an easy way to do this is to open Terminal, type `cd /Volumes/boot` and then `touch ssh`. This will create an empty file. You do not need to put anything in the file, it just needs to exist.
1. Add another file to the root of the `boot` volume named `wpa_supplicant.conf`. Again, in terminal, just type `touch wpa_supplicant.conf` while you're in the root of the `boot` volume and it will be created.
1. The new `wpa_supplicant.conf` file needs to be edited. Use `sudo nano wpa_supplicant.conf`. This file should contain the following:
	```
	ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
	update_config=1
	country=US

	network={
		ssid="Your network name/SSID"
		psk="Your WPA/WPA2 security key"
		key_mgmt=WPA-PSK
	}
	```
	Edit `country=`, `ssid=` and `psk=` with your information and save the file by pressing `CTRL + X`.
1. At this point, you can eject the card and put into the Pi and turn it on.
1. Now you can SSH into the Pi to continue configuration. You'll need the IP address of the Pi. You can usually get this in your router admin page, or you might need to do more depending on your network.
1. In the terminal window, type `ssh pi@192.168.1.5` (replace with your actual Pi IP address). It will prompt for a password. The default is usually `raspberry`.
1. Once you're connected to the Pi via SSH, it's a good idea to go ahead and change the default password. You can do this by running the `sudo raspi-config` tool, Option 1. Reboot the Pi when you're done by using `sudo shutdown -r now`. Your connection to the Pi will be terminated and you can reconnect once it has booted back up.
1. Go ahead and update the Pi to the latest OS updates by running `sudo apt-get update -y` followed by `sudo apt-get upgrade -y`

## TODO Wire and Setup WS28xx

## Installing Python Libraries and Script
The Tally Arbiter Python Listener Client uses the following libraries:
* `rpi-ws281x-python` https://github.com/rpi-ws281x/rpi-ws281x-python
* `python-socketio[client]`

These will have to be installed on the Pi in order for the script to function correctly.

1. In your SSH terminal session, run the following:
    * `sudo pip3 install rpi_ws281x`
    * `sudo pip3 install "python-socketio[client]"`: This library is used to communicate with a Tally Arbiter server over websockets.
    *  `sudo pip3 install git` To get the Tally Arbiter WS28xx Listener from this Repo

    *If `pip3` is not installed, you can get it by running `sudo apt-get install python3-pip`.*




## Setting up the script to start at boot
TODO set up systemd service config  

The program should now launch every time the Pi boots up, and automatically connect to your Tally Arbiter server once the server is available. The ws28xx strip will flash white until it successfully connects to the server.
