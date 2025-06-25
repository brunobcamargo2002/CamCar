import requests
import time

url = "http://192.168.33.185/movement"

def Go(enableLeft, enableRight):
    dados = {
        "leftDirection": enableLeft,
        "leftRPM": 0.8,
        "rightDirection": enableRight,
        "rightRPM": 0.8
    }

    try:
        resposta = requests.post(url, json=dados, timeout=2)
        resposta.raise_for_status()
        print("Comando enviado com sucesso.")
    except requests.RequestException as e:
        print("Erro ao enviar comando:", e)

# Envia comandos

'''
def Stop():
    dados = {
        "leftDirection": 0,
        "leftRPM": 0.0,
        "rightDirection": 0,
        "rightRPM": 0.0
    }
    resposta = requests.post(mov_url, json=dados)

def Rotate(degree):
    dados = {
        "rotation": degree
    }
    resposta = requests.post(rot_url, json=dados)
'''