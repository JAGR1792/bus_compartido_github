from __future__ import annotations

# ========= Parte 1: Importaciones =========
# Esta parte importa las librerias necesarias para construir la simulacion.
# Cada import cumple un rol especifico en el control de procesos y tiempos.


import argparse # Para crear una interfaz de linea de comandos y recibir parametros de ejecucion.
import random # Para generar numeros aleatorios y forzar hacer funcionar el sistema
import time # Para pausar la ejecucion, con algo tipo: (Sleep(random))

#------------------------------------------------------------------------------------------------------
# Para crear procesos independientes y sincronizarlos con un semaforo.
# - Process: Cada dispositivo necesita una forma de crearse, dah, y Process es la clase que permite instanciarlo
# - Semaphore: controla que solo un proceso use el bus a la vez.
# - current_process: permite identificar el nombre del proceso en los mensajes.
from multiprocessing import Process, Semaphore, current_process


# ========= Parte 2: Logica de un dispositivo =========
# Esta funcion representa a un dispositivo que intenta usar el bus compartido,
# espera su turno, transfiere datos y luego libera el canal
def usar_bus(dispositivo_id: int, bus: Semaphore, min_uso: float, max_uso: float, max_espera_inicial: float) -> None:
    """Simula a un dispositivo que necesita enviar datos por un bus compartido."""

    # Se introduce un retardo aleatorio para que no todos pidan el bus al mismo tiempo exacto, que haya un número 1, y sea el primer "atendido"
    espera_inicial = random.uniform(0, max_espera_inicial)
    time.sleep(espera_inicial)

    nombre = current_process().name
    print(f"[{nombre}] Dispositivo {dispositivo_id}: quiere enviar datos, esperando bus...", flush=True)

    # Toma del semaforo: si el bus esta ocupado, este proceso se bloquea y espera.
    bus.acquire()
    try:
        # Simulacion del tiempo durante el cual el dispositivo usa el bus.
        tiempo_uso = random.uniform(min_uso, max_uso)
        print(
            f"[{nombre}] Dispositivo {dispositivo_id}: usando bus durante {tiempo_uso:.2f}s para transferir datos.",
            flush=True,
        )
        time.sleep(tiempo_uso)
        print(f"[{nombre}] Dispositivo {dispositivo_id}: transferencia completa.", flush=True)
    finally:
        # Liberacion garantizada del bus para evitar bloqueos permanentes.
        bus.release()
        print(f"[{nombre}] Dispositivo {dispositivo_id}: libera el bus.", flush=True)


# ========= Parte 3: Parametros de ejecucion =========
# Esta funcion define y lee los argumentos de linea de comandos para ajustar
# la cantidad de dispositivos y los tiempos de la simulacion.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulador de acceso concurrente a un bus compartido con semaforo de multiprocessing.",
    )
    parser.add_argument("-n", "--dispositivos", type=int, default=5, help="Cantidad de dispositivos/procesos.")
    parser.add_argument("--min-uso", type=float, default=1.0, help="Tiempo minimo de uso del bus por dispositivo.")
    parser.add_argument("--max-uso", type=float, default=3.0, help="Tiempo maximo de uso del bus por dispositivo.")
    parser.add_argument(
        "--max-espera-inicial",
        type=float,
        default=2.0,
        help="Espera aleatoria previa al primer intento de acceso al bus.",
    )
    return parser.parse_args()


# ========= Parte 4: Orquestacion principal =========
# Esta parte valida parametros, crea el semaforo del bus, lanza los procesos,
# espera a que terminen y muestra el cierre de la simulacion.
def main() -> None:
    args = parse_args()

    # Validaciones basicas para evitar configuraciones invalidas.
    if args.dispositivos <= 0:
        raise ValueError("La cantidad de dispositivos debe ser mayor a 0.")
    if args.min_uso <= 0 or args.max_uso <= 0:
        raise ValueError("Los tiempos de uso deben ser mayores a 0.")
    if args.min_uso > args.max_uso:
        raise ValueError("min-uso no puede ser mayor que max-uso.")
    if args.max_espera_inicial < 0:
        raise ValueError("max-espera-inicial no puede ser negativo.")

    # Semaforo binario: solo un dispositivo puede acceder al bus por vez.
    bus = Semaphore(1)
    procesos: list[Process] = []

    print(f"Iniciando simulacion con {args.dispositivos} dispositivos...", flush=True)

    # Creacion y arranque de todos los dispositivos/procesos.
    for i in range(1, args.dispositivos + 1):
        proceso = Process(
            target=usar_bus,
            args=(i, bus, args.min_uso, args.max_uso, args.max_espera_inicial),
            name=f"Proceso-{i}",
        )
        procesos.append(proceso)
        proceso.start()

    # Espera hasta que todos los procesos finalicen.
    for proceso in procesos:
        proceso.join()

    print("Simulacion finalizada: todos los dispositivos enviaron sus datos de forma ordenada.", flush=True)


if __name__ == "__main__":
    # Punto de entrada del programa cuando se ejecuta este archivo directamente.
    main()
