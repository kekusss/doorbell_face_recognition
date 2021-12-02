import requests
import os
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ApiController:
    def __init__(self):
        load_dotenv()
        self.api_address = os.environ.get("api-address")
        self.api_key = os.environ.get("api-key")

    def __call_api(self, endpoint):
        headers = {"Authorization": "Bearer " + self.api_key}
        response = requests.get(self.api_address + endpoint, headers=headers, verify=False)
        return response

    def send_notify(self):
        response = self.__call_api('send')
        print(response.text)

    def send_open(self):
        self.__call_api('entrance/open')