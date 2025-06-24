import math

def angleBetweenTwoPoints(p1, p2):
    """
    Calcula o ângulo em graus entre dois pontos p1 e p2.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    angle = math.atan2(dy, dx)

    if angle < 0:
        angle += 2 * math.pi

    return math.degrees(angle)

def distanceBetweenTwoPoints(p1, p2):
    """
    Calcula a distância entre dois pontos p1 e p2.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    return math.sqrt(dx**2 + dy**2)

def euclideanDistance(p1, pr2, pr3):
    """
    Calcula a distância euclidiana de um ponto até uma reta definida por dois pontos pr2 e pr3 e
    retorna o ponto da reta que foi projetado mais próximo do ponto p1.
    """

    x0, y0 = p1
    x1, y1 = pr2
    x2, y2 = pr3

    # Vetor da reta (pr2 -> pr3)
    dx = x2 - x1
    dy = y2 - y1

    # Se o vetor da reta for nulo, a reta é um ponto
    if dx == 0 and dy == 0:
        distance = math.hypot(x0 - x1, y0 - y1)
        closest_point = pr2
        return distance, closest_point

    # Projeção escalar do vetor (pr2 -> p1) no vetor da reta
    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)

    # Coordenadas do ponto mais próximo na reta
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    # Distância euclidiana entre p1 e o ponto mais próximo na reta
    distance = math.hypot(x0 - closest_x, y0 - closest_y)

    return distance, (closest_x, closest_y)

if __name__ == "__main__":
    # Teste das funções
    p1 = (1, 2)
    p2 = (4, 6)
    pr2 = (0, 0)
    pr3 = (5, 5)

    print("Ângulo entre p1 e p2:", angleBetweenTwoPoints(p1, p2))
    print("Distância entre p1 e p2:", distanceBetweenTwoPoints(p1, p2))
    distance, closest_point = euclideanDistance(p1, pr2, pr3)
    print("Distância euclidiana de p1 até a reta:", distance)
    print("Ponto mais próximo na reta:", closest_point)