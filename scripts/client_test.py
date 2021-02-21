import requests

if __name__ == "__main__":
    data = {"a":"b"}
    res = requests.post("http://192.168.200.233:7008/api_show_result",json=data)
    print(res)
