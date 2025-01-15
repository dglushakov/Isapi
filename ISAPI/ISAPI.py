import requests
from requests.auth import HTTPDigestAuth

import xml.etree.ElementTree as ET


class ISAPI:
    ISAPI_GET_PATHS = {
        "DEVICE_INFO": "/ISAPI/System/deviceinfo",
        "USERS": "/ISAPI/Security/users",
        "CHANNELS_STATUS": "/ISAPI/System/workingstatus/chanStatus?format=json",
        "CHANNELS": "/ISAPI/ContentMgmt/InputProxy/channels",
        "WORKING_STATUS": "/ISAPI/System/workingstatus",
        "HDD_STATUS": "/ISAPI/ContentMgmt/Storage/hdd",
        "STATUS": "/ISAPI/System/Video/capabilities",
    }

    def __init__(self, ip, login="admin", password="12345", protocol="http"):
        self.ip = ip
        self.login = login
        self.password = password
        self.protocol = protocol

    def get_request(self, isapi_abs_path_key):
        url = self.protocol + "://" + self.ip + self.ISAPI_GET_PATHS[isapi_abs_path_key] + "?format=json"
        response = {
            "url": url,
            "success": 0,
            "error": None,
            "status_code": None,
            "text": None,
        }
        try:
            headers = {'Content-type': 'application/json'}
            r = requests.get(url, auth=HTTPDigestAuth(self.login, self.password), timeout=1, headers=headers)
            # r = requests.get(url, auth=HTTPDigestAuth(self.login, self.password), timeout=1,)
            response["success"] = 1
            response["status_code"] = r.status_code
            response["text"] = r.text
        except requests.exceptions.ConnectTimeout as error:
            response["success"] = 0
            response["error"] = error
        finally:
            return response


if __name__ == '__main__':
    isapi = ISAPI(ip="192.168.2.168", login='admin', password='2wsx#EDC')

    print(isapi.get_request(isapi_abs_path_key="HDD_STATUS"))
    print(isapi.get_request(isapi_abs_path_key="HDD_STATUS")["text"])
    print(isapi.get_request(isapi_abs_path_key="DEVICE_INFO")["text"])
    print(isapi.get_request(isapi_abs_path_key="WORKING_STATUS")["text"])

    print("=================")
    print(isapi.get_request(isapi_abs_path_key="USERS")["url"])
    print(isapi.get_request(isapi_abs_path_key="USERS")["text"])
