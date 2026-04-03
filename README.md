# Simulador de Bus Compartido

Este proyecto implementa una simulacion de comunicacion por **bus compartido** usando procesos independientes y un **semaforo** del modulo `multiprocessing` para sincronizar el acceso al canal.

## Que hace

- Crea varios dispositivos como procesos.
- Cada dispositivo intenta acceder al bus para enviar datos.
- Si el bus esta ocupado, el proceso espera.
- Cuando obtiene acceso, usa el bus durante un tiempo simulado.
- Luego libera el bus para que otro dispositivo pueda usarlo.
- Muestra en consola mensajes de: espera, uso y liberacion del bus.

## Requisitos

- Python 3.10 o superior

## Ejecucion

```bash
python bus_compartido.py
```

## Opciones utiles

```bash
python bus_compartido.py -n 8 --min-uso 0.8 --max-uso 2.5 --max-espera-inicial 1.5
```

- `-n, --dispositivos`: cantidad de procesos/dispositivos.
- `--min-uso`: tiempo minimo (segundos) que un dispositivo usa el bus.
- `--max-uso`: tiempo maximo (segundos) que un dispositivo usa el bus.
- `--max-espera-inicial`: retardo aleatorio previo al intento de acceso.
