import cv2
import numpy as np

def DistanceEstimatorClassifier(path):
    #=========================================
    #   MAIN -  USAR ESSA FUNÇÃO PARA CHAMAR
    #=========================================

    """
    Estima a distância até o objeto e classifica a espessura das listras com base na imagem fornecida.

    Parâmetros:
        path (str): Caminho para a imagem a ser processada.

    Retorna:
        distance (float): Estimativa da distância até o objeto.
        thickness (str): Classificação da espessura das listras.
    """

    filtered_contours = StripeDetector(path)

    distance = DistanceEstimator(filtered_contours)
    thickness = DistanceClassifier(filtered_contours)

    return distance, thickness

def StripeDetector(img_path):
    """
    Detecta listras pretas em uma imagem e retorna os contornos filtrados.

    Parâmetros:
        img_path (str): Caminho para a imagem.

    Retorna:
        filtered_contours (list): Lista de contornos com área acima do mínimo.
    """

    #================Parametros de Calibração===================
    limiar = 55 #(int): Valor de threshold para binarização (padrão: 80). 
    #===========================================================

    # Carrega a imagem, gira em 180 graus e converte para escala de cinza
    img = cv2.imread(img_path)
    img_rotated = cv2.rotate(img, cv2.ROTATE_180)
    gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)

    # Binariza invertendo (faixas pretas viram branco)
    _, thresh = cv2.threshold(gray, limiar, 255, cv2.THRESH_BINARY_INV)

    # Encontra contornos externos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra contornos
    filtered_contours = ContoursFilter(contours)

    #Mostra etapa das filtragens
    ShowImageStages(img_rotated, filtered_contours, gray, thresh)

    return filtered_contours

def ContoursFilter(contours):
    """
    Filtra ruídos dos contronos.

    Parâmetros:
        contours (list): Lista de contornos sem filtro.

    Retorna:
        filtered_contours (list): Lista de contornos filtrados que representam as faixas 
        verticais agrupadas (provavelmente pertencentes ao poste).
    """

    #Filtra contornos por area e proporção
    candidate_contours = AreaRatioFilter(contours)
    filtered_contours = ClusterFilter(candidate_contours)
    
    return filtered_contours


def AreaRatioFilter(contours):
    """
    Filtra ruídos pela por area e proporção entre altura e largura.

    Parâmetros:
        contours (list): Lista de contornos sem filtro.

    Retorna:
        filtered_contours (list): Lista de contornos filtrados que respeitam a area minimae proporção maxima.

    """

    #================Parametros de Calibração===================
    min_area = 500 #(float): Área mínima para considerar um contorno válido (padrão: 500).
    max_ratio = 1.0 #(float): Proporção máxima entre altura e largura para considerar um contorno válido.
    #===========================================================

    candidate_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        #Se area for maior que o parametro minimo, coloca na lista de candidatos a contorno.
        if area > min_area:
            x, y, w, h = cv2.boundingRect(c)

            #Calcula proporção entre altura e largura
            aspect_ratio = h / float(w)
            # Se for achatado é um contorno
            if aspect_ratio < max_ratio: 
                candidate_contours.append((x + w // 2, c))  # salva posição x central + contorno

    return candidate_contours

def ClusterFilter(candidate_contours):
    """
    Filtra ruídos por agrupamento na vertical.

    Parâmetros:
        contours (list): Lista de contornos sem filtro.

    Retorna:
        filtered_contours (list): Lista de agrupamento(na vertical) que mais tem chance de ser um poste.

    """

    #================Parametros de Calibração===================
    max_x_distance = 50 #(float): Distância maxima entre os Xs centrais do agrupamento.
    #===========================================================

    if not candidate_contours:
        print("ERRO - ClusterFilter - Nenhum contorno com geometria válida.")
        return []
    else:
        #Agrupar contornos no eixo X.
        clusters = {}
        for i, (x, c) in enumerate(candidate_contours):
            found = False
            for cx in clusters:
                if abs(x - cx) < max_x_distance:  # distância máxima entre faixas vizinhas no X.
                    clusters[cx].append((x, c))
                    found = True
                    break
            if not found:
                clusters[x] = [(x, c)]
    
        # Pega o cluster com mais elementos.
        best_cluster = max(clusters.values(), key=len)
        filtered_contours = [c for _, c in best_cluster]
        return filtered_contours

def ShowImageStages(img, filtered_contours, gray, thresh):
    """
    Exibe visualmente as principais etapas do processamento de imagem.

    Parâmetros:
        img (np.ndarray): Imagem original em formato BGR.
        filtered_contours (list): Lista de contornos filtrados a serem desenhados.
        gray (np.ndarray): Imagem em tons de cinza.
        thresh (np.ndarray): Imagem binarizada (threshold).

    A função não retorna nada, apenas exibe uma janela com quatro imagens lado a lado:
    - Original
    - Em tons de cinza
    - Binarizada
    - Original com contornos desenhados

    A janela permanece aberta até ser fechada pelo usuário.
    """

    # Para mostrar contornos, vamos copiar a imagem original
    img_contours = img.copy()
    cv2.drawContours(img_contours, filtered_contours, -1, (0,255,0), 2)

    # Como temos imagens em tons de cinza e coloridas, vamos converter as grayscale para BGR para concatenar
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # Agora juntamos as imagens horizontalmente
    side_by_side = np.hstack((img, gray_bgr, thresh_bgr, img_contours))

    # Ajuste a janela para caber
    cv2.namedWindow('Etapas', cv2.WINDOW_NORMAL)
    cv2.imshow('Etapas', side_by_side)
    
    #Espera fechar a janela
    while True:
        cv2.waitKey(100)# Espera 100ms para não travar a CPU
        if cv2.getWindowProperty('Etapas', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows() 

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
    focal_length_px = 1600 #(float): Distância focal da câmera em pixels (ajustada por calibração)
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
