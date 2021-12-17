import requests
import csv


class GetInfoByIP:
    _ip_info: dict

    def __init__(self, ip):
        response = requests.get(f"http://ip-api.com/json/{ip}")
        self._ip_info = response.json()

    def get_info(self):
        return self._ip_info


class GetMyIP:
    _ip_data: list

    def __init__(self):
        response = requests.get("http://whoami.miccedu.local")
        html = response.text
        data_list = html.splitlines()
        self._ip_data = data_list

    def get_ip_data(self):
        return self._ip_data

    def get_ip(self):
        return self._ip_data[-1]


class Facade:
    def __init__(self, subsystem1: GetMyIP = None, subsystem2: GetInfoByIP = None):
        self.ss1 = subsystem1 or GetMyIP()
        self.ss2 = subsystem2 or GetInfoByIP(self.ss1.get_ip())

    def operation(self):
        host = self.ss1.get_ip_data()[7]
        data = self.ss2.get_info()
        data["host"] = host
        return data


class Adapter:
    def __init__(self, data, filepath="./res.csv"):
        self.filepath = filepath
        self.data = data

    def write2csv(self):
        with open('mycsvfile.csv', 'w') as f:
            w = csv.DictWriter(f, self.data.keys())
            w.writeheader()
            w.writerow(self.data)


facade = Facade()
data_ip = facade.operation()
print(data_ip)
adapter = Adapter(data_ip)
adapter.write2csv()
