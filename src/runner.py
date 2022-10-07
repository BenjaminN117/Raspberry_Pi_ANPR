'''
Product: Raspberry Pi ANPR
Description: runner script
Author: Benjamin Norman
Creation Date: 2022
'''

from flask import Flask, request, jsonify
import threading
import sys
import json
from NumberPlateChecker import NumberPlateChecker

'''
Code runner for ANPR proj

'''



'''
Executes two seperate instances of the cv2 image detection program (one for each camera).

if the script discovers a possible number plate, capture a photo then launch the Sighthound API caller (disable the other camera temporarily)

When the number plate is validated and returned, reinstate the cameras.

When the gates are opened from the inside recieve a webhook from HomeAssistant to temporarily disable the image detection for a set period of time (1 min probs)

- Runs 4 threads in total :(

'''

class webController():
    def __init__(self):
        self.configFileName = "config.json"
        self.portNumber = 0
        self.apiToken = ""
        self.outgoingWebhookAddress = ""

    def config_importer(self):
        with open(self.configFileName) as ConfigFile:
            configDict = json.load(ConfigFile)
            
        self.apiToken = configDict["config_file"][3]["API_Token"]
        self.portNumber = configDict["config_file"][2]["Incoming_Webhook_Port_Number"]
        self.outgoingWebhookAddress = configDict["config_file"][1]["Outgoing_Webhook_Address"]
        
    def response_filter(self, message):
        try:
            return self.detection_delay(message["delay_time"])
        except:
            return "Invalid JSON data"

    def detection_delay(self, delay_time):
        if delay_time == "disable":
            return "200"
        elif delay_time == "enable":
            return "200"
        elif type(delay_time) is int:
            return "200"
        else:
            return "Invalid JSON data"

if __name__ == "__main__":
    inst = webController()
    inst.config_importer()

    app = Flask(__name__)

    @app.route('/detection/delay/<api_key>', methods=['GET', 'POST'])
    def add_message(api_key):
        content = request.json
        if api_key != inst.apiToken:
            return jsonify({"Status":"Invalid API token"})
        output = inst.response_filter(content)
        return jsonify({"Status":output})

    app.run(host= '0.0.0.0',debug=True, port=inst.portNumber)