#=========================================================================================
#   COMANDOS PARA INICIAR SERVIDOR NO LINUX
#   sudo /opt/lampp/lampp start
#   sudo /opt/lampp/manager-linux-x64.run
#=========================================================================================

from DistanceEstimatorClassifier import DistanceEstimatorClassifier
"""
    ARQUIVO PARA TESTE DAS FUNÇÕES
"""
path = r"/opt/lampp/htdocs/ESP32CAM/captured_images/ESP32CAMCap.jpg"

distance, thickness =  DistanceEstimatorClassifier(path)

if distance == None:
    print("ERRO - Main - Não foi possível calcular a distância.")
elif thickness == None:
    print("ERRO - Main - Não foi possível calcular o número de faixas.")
else:
    print(f"Distância estimada: {distance:.2f} cm\nNúmero de faixas estimada: {thickness:.2f} faixas")
