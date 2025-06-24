import cv2
import numpy as np

"""
================ESTATÍSTICAS==================================================
ERRO DA DISTÂNCIA       = 3%(LONGE - 50 cm) - 10%(MEDIO - 50/40cm) - 30%(PERTO - 30 cm)
ERRO DA CLASSIFICAÇÃO   = 0%
PRINCIPAL FONTE DE ERRO = COISAS PRETAS(SOMBRA PRINCIPALMENTE) PERTO DO POSTE
E ILUMINAÇÃO
==============================================================================
"""

#========Parametros de Calibração(MAIS FREQUENTES)==========
LIMIAR              = 70    #ELIMINAR RUIDO                 #(int): Valor de threshold para binarização (padrão: 55).
FOCAL_LENGTH_PX     = 1600  #CORREÇÃO CALCULO DISTÂNCIA     #(float): Distância focal da câmera em pixels (ajustada por calibração).    
#========Parametros de Calibração(MENOS FREQUENTES)=========
WINDOW_SIZE         = 25    #UNIR FAIXA                     #(int): Largura do lado da janela quadrada para fazer o fechamento morfologico.
MIN_AREA            = 500   #ELIMINAR RUIDO                 #(float): Área mínima para considerar um contorno válido (padrão: 500).
MAX_RATIO           = 1.0   #ELIMINAR RUIDO                 #(float): Proporção máxima entre altura e largura para considerar um contorno válido.
MAX_X_DISTANCE      = 50    #ELIMINAR RUIDO                 #(float): Distância maxima entre os Xs centrais do agrupamento.
ONE_STRIP_RATIO     = 0.25  #CLASSIFICAÇÃO ESPESSURA        #(int): Limite inferior de proporção para classificar como '1 faixas'
THREE_STRIP_RATIO   = 0.43  #CLASSIFICAÇÃO ESPESSURA        #(int): Limite superior de proporção para classificar como '2 faixas'
#===========================================================
#RATIO = Y / X
#==============Parametros do Mundo Real=====================
INITIAL_REAL_HEIGHT_CM  = 49.5 #CARACTERISTICA POSTE       #(float): Altura real do padrão no poste (ex: 40 cm)
REAL_BANDS_NUMBER            = 7    #CARACTERISTICA POSTE       #Numero de faixas do poste.
#===========================================================

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

    filtered_contours = StripeDetector(path, ShowImageFlag = False)

    thickness, average_ratio= DistanceClassifier(filtered_contours)

    result = DistanceEstimator(filtered_contours, thickness)
    if result is None:
       distance, captured_bands_nunber = None, 0
    else:
       distance, captured_bands_nunber = result

    #Printo no terminal o resultado
    Log(distance, thickness, captured_bands_nunber, average_ratio)

    return distance, thickness, average_ratio

def StripeDetector(img_path, ShowImageFlag = False):
    """
    Detecta listras pretas em uma imagem e retorna os contornos filtrados.

    Parâmetros:
        img_path (str): Caminho para a imagem.

    Retorna:
        filtered_contours (list): Lista de contornos com área acima do mínimo.
    """

    #================Parametros de Calibração===================
    limiar = LIMIAR #(int): Valor de threshold para binarização (padrão: 55).
    window_size = WINDOW_SIZE #(int): Largura do lado da janela quadrada para fazer o fechamento morfologico.
    #===========================================================

    # Carrega a imagem, gira em 180 graus e converte para escala de cinza
    img = cv2.imread(img_path)
    img_rotated = img#cv2.rotate(img, cv2.ROTATE_180)
    gray = cv2.cvtColor(img_rotated, cv2.COLOR_BGR2GRAY)

    # Binariza invertendo (faixas pretas viram branco)
    _, thresh = cv2.threshold(gray, limiar, 255, cv2.THRESH_BINARY_INV)

    # Elimina listras verticais brancas causadas pelo flash
    kernel = np.ones((window_size, window_size), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Encontra contornos externos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra contornos
    filtered_contours, candidate_contours = ContoursFilter(contours)

    #Mostra etapa das filtragens
    if ShowImageFlag:
        ShowImageStages(img_rotated, filtered_contours, candidate_contours, gray, thresh)

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
    
    return filtered_contours, candidate_contours


def AreaRatioFilter(contours):
    """
    Filtra ruídos pela por area e proporção entre altura e largura.

    Parâmetros:
        contours (list): Lista de contornos sem filtro.

    Retorna:
        filtered_contours (list): Lista de contornos filtrados que respeitam a area minimae proporção maxima.

    """

    #================Parametros de Calibração===================
    min_area = MIN_AREA #(float): Área mínima para considerar um contorno válido (padrão: 500).
    max_ratio = MAX_RATIO #(float): Proporção máxima entre altura e largura para considerar um contorno válido.
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
                candidate_contours.append((x + w // 2, c, aspect_ratio))  # salva posição x central + contorno + proporção entre altura e largura

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
    max_x_distance = MAX_X_DISTANCE #(float): Distância maxima entre os Xs centrais do agrupamento.
    #===========================================================

    if not candidate_contours:
        print("ERRO - ClusterFilter - Nenhum contorno com geometria válida.")
        return []
    else:
        #Agrupar contornos no eixo X.
        clusters = {}
        for i, (x, c, r) in enumerate(candidate_contours):
            found = False
            for cx in clusters:
                if abs(x - cx) < max_x_distance:  # distância máxima entre faixas vizinhas no X.
                    clusters[cx].append((x, c, r))
                    found = True
                    break
            if not found:
                clusters[x] = [(x, c, r)]
    
        # Pega o cluster com mais elementos.
        best_cluster = max(clusters.values(), key=len)
        filtered_contours = [(c, r) for _, c, r in best_cluster]
        return filtered_contours

def ShowImageStages(img, filtered_contours, candidate_contours, gray, thresh):
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
    img_candidate_contours = img.copy()
    img_filtered_contours = img.copy()
    candidate_contours_only = [ c for x, c, r in candidate_contours]
    filtered_contours_only = [ c for c, r in filtered_contours]
    cv2.drawContours(img_candidate_contours, candidate_contours_only, -1, (0,255,0), 2)
    cv2.drawContours(img_filtered_contours, filtered_contours_only, -1, (0,255,0), 2)

    # Como temos imagens em tons de cinza e coloridas, vamos converter as grayscale para BGR para concatenar
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    thresh_bgr = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    # Agora juntamos as imagens horizontalmente
    side_by_side = np.hstack((img, gray_bgr, thresh_bgr, img_candidate_contours, img_filtered_contours))

    # Ajuste a janela para caber
    cv2.namedWindow('Etapas', cv2.WINDOW_NORMAL)
    cv2.imshow('Etapas', side_by_side)
    
    #Espera fechar a janela
    while True:
        cv2.waitKey(100)# Espera 100ms para não travar a CPU
        if cv2.getWindowProperty('Etapas', cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows() 

def DistanceEstimator(filtered_contours, thickness):
    """
    Estima a distância até o poste com base na altura das listras detectadas.
    
    Parâmetros:
        filtered_contours (list): Lista de contornos.
        (RETORNO DA FUNÇÃO StripeDetector)
    
    Retorno:
        float: Distância estimada em cm (ou None, se não conseguir detectar)
    """

    #================Parametros de Calibração===================
    real_bands_number = REAL_BANDS_NUMBER #Numero de faixas do poste.
    initial_real_height_cm = INITIAL_REAL_HEIGHT_CM #(float): Altura real do padrão no poste (ex: 40 cm)
    focal_length_px = FOCAL_LENGTH_PX #(float): Distância focal da câmera em pixels (ajustada por calibração)
    #===========================================================

    if len(filtered_contours) < 2:
        print("ERRO - DistanceEstimator - Padrão não detectado com clareza.")
        return None
    else:

        #Cacula altura ralativa caso o poste não apareca totalmente.
        captured_bands_nunber = len(filtered_contours)
        real_height_cm =  (captured_bands_nunber/real_bands_number) * initial_real_height_cm

        # Encontra top e bottom Y das listras
        ys = [cv2.boundingRect(c)[1] for c, r in filtered_contours]
        y_top = min(ys)
        y_bot = max([y + h for (x, y, w, h) in [cv2.boundingRect(c) for c, r in filtered_contours]])

        height_pixels = y_bot - y_top

        # Aplica fórmula de distância:
        # distância = (altura_real * focal) / altura_aparente
        distance_cm = (real_height_cm * focal_length_px) / height_pixels

        return distance_cm, captured_bands_nunber

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
    one_strip_ratio = ONE_STRIP_RATIO #(int): Limite inferior de proporção para classificar como '1 faixas'
    three_strip_ratio = THREE_STRIP_RATIO #(int): Limite superior de proporção para classificar como '2 faixas'
    #===========================================================

    if len(filtered_contours) == 0:
        print("ERRO - DistanceClassifier - Nenhuma faixa detectada.")
        return None, None #Nenhuma faixa detectada.

    # Obtem as proporções entre altura e largura das faixas.
    ratios = [r for c, r in filtered_contours]  # h = altura da faixa

    average_ratio = sum(ratios) / len(ratios)

    # Classificação com base em limites definidos.
    if average_ratio < one_strip_ratio:
        return 1, average_ratio #1 faixas
    elif average_ratio >= three_strip_ratio:
        return 3, average_ratio #3 faixas
    else:
        return 2, average_ratio #2 faixas

def Log(distance, thickness, captured_bands_nunber, average_ratio):
    print("============================================================")
    print(f"Faixas identificadas: {captured_bands_nunber:.2f} faixas")
    if distance == None:
        print("ERRO - Main - Não foi possível calcular a distância.")
    elif thickness == None:
        print("ERRO - Main - Não foi possível calcular o número de faixas.")
    elif average_ratio == None:
        print("ERRO - Main - Não foi possível calcular a proporção.")
    else:
        print(f"Proporção Média das Faixas: {average_ratio:.2f}\nEspessura das faixas: {thickness:.2f} fitas\nDistância estimada: {distance:.2f} cm")
