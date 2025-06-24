import requests
import time


url = "http://192.168.187.185/movement"

def Go():
    dados = {
        "leftDirection": 1,
        "leftRPM": 1.0,
        "rightDirection": 1,
        "rightRPM": 1.0
    }
    resposta = requests.post(url, json=dados)

def Stop():
    dados = {
        "leftDirection": 0,
        "leftRPM": 0.0,
        "rightDirection": 0,
        "rightRPM": 0.0
    }
    resposta = requests.post(url, json=dados)

def Rotate(degree): ## talvez fique uma bosta, implementar rotina para rotacionar dentro do carrinho
    if(degree < 0):
        degree = 360 + degree  # Normalize negative degrees to positive

    dados = {
        "leftDirection": 1,
        "leftRPM": 1.0,
        "rightDirection": 0,
        "rightRPM": 0.0
    }
    resposta = requests.post(url, json=dados)
    time.sleep(degree / 90)  # Assuming 90 degrees takes 1 second
    Stop()