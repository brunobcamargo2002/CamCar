import cv2
import numpy as np

def DistanceEstimator(filtered_contours):
    """
    Estima a distância até o poste com base na altura das listras detectadas.
    
    Parâmetros:
        filtered_contours (list): Lista de contornos.
        (RETORNO DA FUNÇÃO StripeDetector)
    
    Retorno:
        float: Distância estimada em cm (ou None, se não conseguir detectar)
    """

    #================Parametros de Calibração===================
    real_height_cm = 49.5 #(float): Altura real do padrão no poste (ex: 40 cm)
    focal_length_px = 600 #(float): Distância focal da câmera em pixels (ajustada por calibração)
    #===========================================================

    if len(filtered_contours) < 2:
        print("ERRO - DistanceEstimator - Padrão não detectado com clareza.")
        return None

    # Encontra top e bottom Y das listras
    ys = [cv2.boundingRect(c)[1] for c in filtered_contours]
    y_top = min(ys)
    y_bot = max([y + h for (x, y, w, h) in [cv2.boundingRect(c) for c in filtered_contours]])

    height_pixels = y_bot - y_top

    # Aplica fórmula de distância:
    # distância = (altura_real * focal) / altura_aparente
    distance_cm = (real_height_cm * focal_length_px) / height_pixels

    return distance_cm

def DistanceClassifier(filtered_contours):
    """
    Classifica um poste com base na espessura média das faixas (em pixels).
    
    Parâmetros:
        filtered_contours (list): Lista de contornos.
        (RETORNO DA FUNÇÃO StripeDetector)

    Retorno:
        int: quantidade de faixas detectadas.
    """

    #================Parametros de Calibração===================
    one_strip_thickness = 15 #(int): Limite inferior em pixels para classificar como '1 faixas'
    three_strip_thickness = 30 #(int): Limite superior em pixels para classificar como '2 faixas'
    #===========================================================

    if len(filtered_contours) == 0:
        print("ERRO - DistanceClassifier - Nenhuma faixa detectada.")
        return None #Nenhuma faixa detectada.

    # Obtem as alturas (ou larguras) das faixas
    heights = [cv2.boundingRect(c)[3] for c in filtered_contours]  # h = altura da faixa

    average_height = sum(heights) / len(heights)

    # Classificação com base em limites definidos
    if average_height < one_strip_thickness:
        return 1 #1 faixas
    elif average_height >= three_strip_thickness:
        return 3 #3 faixas
    else:
        return 2 #2 faixas

def StripeDetector(img_path):
    """
    Detecta listras pretas em uma imagem e retorna os contornos filtrados.

    Parâmetros:
        img_path (str): Caminho para a imagem.

    Retorna:
        filtered_contours (list): Lista de contornos com área acima do mínimo.
    """

    #================Parametros de Calibração===================
    limiar = 80 #(int): Valor de threshold para binarização (padrão: 80). 
    min_area = 500 #(float): Área mínima para considerar um contorno válido (padrão: 500).
    #===========================================================

    # Carrega a imagem e converte para escala de cinza
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Binariza invertendo (faixas pretas viram branco)
    _, thresh = cv2.threshold(gray, limiar, 255, cv2.THRESH_BINARY_INV)

    # Encontra contornos externos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra contornos pela área
    filtered_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    return filtered_contours
