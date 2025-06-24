import requests
import time


url = "http://192.168.187.185"
mov_url = url + "/movement"
rot_url = url + "/rotation"

def Go():
    dados = {
        "leftDirection": 1,
        "leftRPM": 1.0,
        "rightDirection": 1,
        "rightRPM": 1.0
    }
    resposta = requests.post(mov_url, json=dados)

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