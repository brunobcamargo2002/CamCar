#=========================================================================================
#   COMANDOS PARA INICIAR SERVIDOR NO LINUX
#   sudo systemctl stop apache2
#   sudo /opt/lampp/lampp start
#   sudo /opt/lampp/manager-linux-x64.run
#=========================================================================================

import time
from DistanceEstimatorClassifier import DistanceEstimatorClassifier

"""
    ARQUIVO PARA TESTE DAS FUNÇÕES
"""

path = r"/opt/lampp/htdocs/ESP32CAM/captured_images/ESP32CAMCap.jpg"

while(True):
    distance, thickness, average_ratio =  DistanceEstimatorClassifier(path)
    time.sleep(5)
