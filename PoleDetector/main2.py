#=========================================================================================
#   COMANDOS PARA INICIAR SERVIDOR NO LINUX
#   sudo systemctl stop apache2
#   sudo /opt/lampp/lampp start
#   sudo /opt/lampp/manager-linux-x64.run
#=========================================================================================
from time import sleep
from math import ceil
from LocationOrientation import findCarPosition, findCarPositionOrientation
from Math import angleBetweenTwoPoints, distanceBetweenTwoPoints, euclideanDistance

import CarRequests as cr
import Constants as k

trajetory = [(-1, 0), (1, 5), (2, 10)]
missingPoints = trajetory[:]


for idx, point in enumerate(trajetory):
    # Atualiza posição e orientação antes de começar a andar para o ponto
    #carPosition = findCarPosition()
    #initial point
    carPosition = findCarPositionOrientation()

    while True:
        angle = angleBetweenTwoPoints(carPosition[0], point)
        cr.rotate(angle - carPosition[1])

        distance = distanceBetweenTwoPoints(carPosition[0], point)
        if distance < k.REACHED_THRESHOLD:
            # Ponto alcançado, sai do loop e vai para próximo ponto
            break

        cicles = distance / (k.CAR_SPEED * k.CAR_MOVE)
        for i in range(ceil(cicles)):
            cr.Go()

            # Ajusta tempo no último ciclo para andar só a distância necessária
            move_time = k.CAR_SPEED * k.CAR_MOVE
            if i == ceil(cicles) - 0 and cicles % 1 != 0:
                move_time *= (cicles % 1)

            sleep(move_time)

            carPosition = findCarPositionOrientation()

            error, closest_point = euclideanDistance(carPosition[0], initialPoint, point)
            if error > k.MAX_ERROR:
                # Corrige posição retornando para a reta
                correction_angle = angleBetweenTwoPoints(carPosition[0], closest_point)
                cr.rotate(correction_angle - carPosition[1])

                correction_distance = distanceBetweenTwoPoints(carPosition[0], closest_point)
                correction_cicles = correction_distance / (k.CAR_SPEED * k.CAR_MOVE)

                for _ in range(ceil(correction_cicles)):
                    cr.Go()
                    sleep(k.CAR_SPEED * k.CAR_MOVE)
                    carPosition = findCarPositionOrientation()

                break  # sai do for para recalcular trajetória e seguir

    # Atualiza o ponto inicial para o próximo segmento da trajetória
    initialPoint = point




"""
distance, thickness =  DistanceEstimatorClassifier(path)

if distance == None:
    print("ERRO - Main - Não foi possível calcular a distância.")
elif thickness == None:
    print("ERRO - Main - Não foi possível calcular o número de faixas.")
else:
    print(f"Distância estimada: {distance:.2f} cm\nNúmero de faixas estimada: {thickness} faixas")
"""
