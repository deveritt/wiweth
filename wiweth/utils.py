import requests
from typing import Dict
import json


RequestHeaders = Dict[str,str]


def make_request(address: str, headers: RequestHeaders, verb:str="GET") -> Dict:
    """
    Sends a get request to MapQuest. (Only written for GET requests here.)
    :param params: String with protocol, url and parameters.
    :param: headers.
    :param: verb. (Only written for GET requests.)
    :return: JSON response
    """
    r = requests.request(verb, address, headers=headers)
    r.raise_for_status()
    return r.json()
