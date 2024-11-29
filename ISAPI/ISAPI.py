import requests
from requests.auth import HTTPDigestAuth

import xml.etree.ElementTree as ET


class ISAPI:
    @staticmethod
    def is_request_has_successs(response):
        if response["success"] == 0 or response["error"] or response["status_code"] != 200:
            return True
        return False

    ISAPI_PATHS = {
        "DEVICE_INFO": "/ISAPI/System/deviceinfo",
        "USERS": "/ISAPI/Security/users",

        "CHANNELS_STATUS": "/ISAPI/System/workingstatus/chanStatus?format=json",
        "CHANNELS": "/ISAPI/ContentMgmt/InputProxy/channels",

        "working_status": "/ISAPI/System/workingstatus",

        "hdd": "/ISAPI/ContentMgmt/Storage/hdd",

        "status": "/ISAPI/System/Video/capabilities",  # ?
    }

    def __init__(self, ip, login="admin", password="12345", protocol="http"):
        self.ip = ip
        self.login = login
        self.password = password
        self.protocol = protocol

    def __make_url__(self, isapi_abs_path: str) -> str:
        url = self.protocol + "://" + self.ip + isapi_abs_path
        return url

    def xml_to_dict_recursive(self, root):

        trash_perfix = "{http://www.hikvision.com/ver20/XMLSchema}"

        if root.tag.startswith(trash_perfix):
            tag = root.tag[len(trash_perfix):]
        else:
            tag = root.tag
        if len(list(root)) == 0:
            return {tag: root.text}
        else:
            return {tag: list(map(self.xml_to_dict_recursive, list(root)))}

    def get_request(self, isapi_abs_path):
        url = self.__make_url__(isapi_abs_path)
        response = {
            "success": 0,
            "error": None,
            "status_code": None,
            "text": None,
        }
        try:
            r = requests.get(url, auth=HTTPDigestAuth(self.login, self.password), timeout=1)
            response["success"] = 1
            response["status_code"] = r.status_code
            response["text"] = r.text
        except requests.exceptions.ConnectTimeout as error:
            response["error"] = error
        finally:
            return response

    def post_request(ip, isapi_abs_path, payload, login="admin", password="2wsx#EDC1", protocol="http"):
        pass

    def get_users(self):
        """ Возвращает список словарей вида: {'id': '1', 'userName': 'admin', 'userLevel': 'Administrator'} или None (в случае ошибки)"""
        response_xml = self.get_request(self.ISAPI_PATHS["USERS"])
        if ISAPI.is_request_has_successs(response_xml):
            return None
        else:
            result = []
            root = ET.XML(response_xml["text"])
            users_data = self.xml_to_dict_recursive(root)

            for user in users_data["UserList"]:
                id = user["User"][0]["id"]
                username = user["User"][1]["userName"]
                userlevel = user["User"][4]["userLevel"]
                result.append({
                    "id": id,
                    "userName": username,
                    "userLevel": userlevel
                })

            return result

    def get_device_info(self):
        response_xml = self.get_request(self.ISAPI_PATHS["DEVICE_INFO"])
        if ISAPI.is_request_has_successs(response_xml):
            return None
        else:
            root = ET.XML(response_xml["text"])
            response = self.xml_to_dict_recursive(root)
            return response


if __name__ == '__main__':
    isapi = ISAPI(ip="192.168.2.168", login='admin', password='2wsx#EDC')
    users = isapi.get_users()
    print(users)
    if users:
        for user in users:
            print(user)

    print(isapi.get_device_info())
