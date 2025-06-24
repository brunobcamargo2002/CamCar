import time as t
import Constants as k
import CarRequests as cr
from DistanceEstimatorClassifier import DistanceEstimatorClassifier
from Math import angleBetweenTwoPoints


# === FUNÇÕES PRINCIPAIS ===

def findCarPosition(last_position):
    """
    Captura a posição atual do carrinho e retorna junto com o ângulo atual do objeto car.
    """
    pos = getPosition()
    return (pos, last_position[1])


def findCarPositionOrientation():
    """
    Captura posição inicial, faz o carrinho andar, captura nova posição
    e calcula o ângulo de orientação em relação ao movimento.
    """
    p1 = getPosition()
    if p1 is None:
        return None

    cr.Go()
    t.sleep(2)

    p2 = getPosition()
    if p2 is None:
        return None

    angle = angleBetweenTwoPoints(p1, p2)
    return (p2, angle)


# === FUNÇÕES DE APOIO ===

def getPosition():
    """
    Para o carrinho, espera pelo período da foto, obtém distâncias e calcula coordenadas.
    """
    cr.Stop()
    t.sleep(k.PHOTO_PERIOD + 1)

    distances = findPoles()
    if distances is None:
        # TODO: Implementar estratégia quando não encontrar postes
        return None

    return calculateCarCoordinates(k.POLES_COORDS, distances)


def findPoles():
    """
    Tenta identificar as distâncias aos três postes conhecidos.
    """
    distances = [None, None, None]
    found = 0
    max_attempts = 5
    attempts = 0

    while found < 3 and attempts < max_attempts:
        for cam in k.CAMS:
            distance, thickness = DistanceEstimatorClassifier(cam)

            if distance is not None and thickness is not None:
                index = int(thickness)
                if 0 <= index < 3 and distances[index] is None:
                    distances[index] = distance
                    found += 1
        attempts += 1
        # TODO: Criar rotina de rotação caso não encontre postes

    if found < 3:
        print(f"Warning: Only found {found} poles after {attempts} attempts.")
        return None

    return distances


def calculateCarCoordinates(poles, car_distances):
    """
    Calcula a posição do carrinho a partir das coordenadas dos postes e das distâncias medidas.
    """
    P1 = np.array(poles[0])
    P2 = np.array(poles[1])
    P3 = np.array(poles[2])

    d1, d2, d3 = car_distances

    A = 2 * (P2 - P1)
    B = 2 * (P3 - P1)

    C = d1 ** 2 - d2 ** 2 + np.dot(P2, P2) - np.dot(P1, P1)
    D = d1 ** 2 - d3 ** 2 + np.dot(P3, P3) - np.dot(P1, P1)

    M = np.vstack((A, B))
    Y = np.array([C, D])

    pos = np.linalg.lstsq(M, Y, rcond=None)[0]

    print("Posição do carrinho:", pos)

    return (pos[0], pos[1])


# === EXEMPLO DE USO (descomente para testar manualmente) ===
# poles = [(0, 0), (0, 1), (1, 0)]
# car_distances = [1, 1, 1]
# pos = calculateCarCoordinates(poles, car_distances)
