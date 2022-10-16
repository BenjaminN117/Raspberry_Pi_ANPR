## Raspberry Pi Number Plate Recognition
### Description
This project uses two USB cameras that look for the basic number plate outline and then send the image to Sighthound for a reliable result. If the number plate matches an entry in a JSON file then the script sends out a webhook to a preferred target. In addition to this, a web portal is hosted on the Pi in a Docker container that allows a user to log in and add or remove approved number plates, the JSON file is automatically updated without having to restart the main script.

### Requirements
* 2x USB Cameras (Preferably night vision)
* Account with Sighthound (Setup an API key as well)
* Raspberry Pi 4 (2GB is minimum)
* HomeAssistant server setup for web requests (alternatively you can use any service that accepts and sends webhooks)

**Currently in development (not finished)**
