'''
Product: Raspberry Pi ANPR
Description: Number Plate Checking Script
Author: Benjamin Norman
Creation Date: 2022
'''

import base64
import ssl
import json
import http.client as httplib
from typing import Dict

class NumberPlateChecker():
    
    NumberPlatesDict = Dict
    
    def __init__(self):
        self.SighthoundAPIKey = ""
        self.APIKeyFile = "APIKey.json"
        self.NumberPlateFile = "NumberPlates.json"
        self.NumberPlatesDict = {}
    
    def api_key_loading(self):
        '''
        Loads the API key for Sighthound
        '''
        with open(self.APIKeyFile) as APIKeyFile:
            contents = json.load(APIKeyFile)
        self.SighthoundAPIKey = contents["SighthoundAPIKey"]
    def number_plate_importer(self):
        '''
        Loads in the number plate JSON file
        '''
        with open(self.NumberPlateFile) as NumberPlateFile:
            self.NumberPlatesDict = json.load(NumberPlateFile)
    
        
    def sighthound_request(self, imageName): # Executes the sighthound API and finds the exact number plate characters / This also checks the plate against a database
        '''
        Queries the Sighthound API for a result of the number plate
        '''
        ### API from Sighthound Developer Page ###
        headers = {"Content-type": "application/json",
        "X-Access-Token": self.SighthoundAPIKey}
        conn = httplib.HTTPSConnection("dev.sighthoundapi.com",
        context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
        
        # To use a local file uncomment the following line and update the path
        image_data = base64.b64encode(open(imageName, "rb").read()).decode() #Encodes the image and sends it to Sighthound

        params = json.dumps({"image": image_data})
        conn.request("POST", "/v1/recognition?objectType=licenseplate", params, headers)
        response = conn.getresponse()
        result = response.read()
        ### END ###
        
        result = json.loads(result)
        for objects in result["objects"]:
            foundNumberPlate = objects["licenseplateAnnotation"]["attributes"]["system"]["string"]["name"]

        return foundNumberPlate
        
    def dict_searcher(self, NumberPlate):
        '''
        Traverses the self.NumberPlatesDict to see if there is a match between the inputted plate name and the dict
        '''
        for VehicleName, Plate in self.NumberPlatesDict["NumberPlates"].items():    
            if Plate == NumberPlate:
                return VehicleName, Plate

#Testing only
if __name__ == "__main__":
    inst = NumberPlateChecker()
    inst.api_key_loading()
    inst.number_plate_importer()
    SearchResult = inst.sighthound_request("S.jpg")
    print(inst.dict_searcher(SearchResult))