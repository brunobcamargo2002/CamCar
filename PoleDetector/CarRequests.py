import requests
import time

url = "http://192.168.137.251"
line_url = url + "/line"
stop_url = url + "/stop"

def Go(forward):
    dados = {
        "forward": forward
    }
    resposta = requests.post(line_url, json=dados)
def Stop():
    dados = {
    }
    resposta = requests.post(stop_url, json=dados)

if __name__ == "__main__":
    Go(False)
    print("Deu bom")
    time.sleep(5)
    Stop()
