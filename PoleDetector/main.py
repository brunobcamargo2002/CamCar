from DistanceEstimatorClassifier import DistanceEstimator, DistanceClassifier, StripeDetector
"""
    ARQUIVO PARA TESTE DAS FUNÇÕES
"""
path = r"TestPhotos/6.jpeg"

filtered_contours = StripeDetector(path)

distance = DistanceEstimator(filtered_contours)
thickness = DistanceClassifier(filtered_contours)

if distance == None:
    print("ERRO - Main - Não foi possível calcular a distância.")
elif thickness == None:
    print("ERRO - Main - Não foi possível calcular o número de faixas.")
else:
    print(f"Distância estimada: {distance:.2f} cm\nNúmero de faixas estimada: {thickness:.2f} faixas")
