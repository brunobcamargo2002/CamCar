import CarRequests as cr
from time import sleep

while True:
    try:
        left = int(input("Digite enableLeft (0 ou 1): "))
        right = int(input("Digite enableRight (0 ou 1): "))
        tempo_ms = int(input("Digite o tempo em milissegundos: "))

        cr.Go(left, right)
        sleep(tempo_ms / 1000.0)
        cr.Go(0, 0)  # Parar
        print(f"Parado após {tempo_ms} ms.\n")

    except ValueError:
        print("Entrada inválida. Use apenas 0 ou 1 para direção e número inteiro para tempo.\n")
