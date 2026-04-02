# Sistema experto para clasificacion de animales

Proyecto en Python 3.10 con un motor de inferencia basado en reglas usando Pyke
(`pyke-master` incluido localmente) y una interfaz grafica en Tkinter.

## Estructura

```text
app.py
requirements.txt
src/
  animal_expert_system/
    __init__.py
    domain.py
    inference.py
    gui.py
    knowledge/
      __init__.py
      animals.kfb
      animal_rules.krb
pyke-master/
```

## Ejecucion

1. Activar tu entorno virtual de Python 3.10.
2. Ejecutar:

```bash
python app.py
```

## Que hace

- Permite ingresar caracteristicas del animal en espanol.
- Ofrece dos modos de razonamiento: encadenamiento hacia adelante y hacia atras.
- Muestra un proceso visual con trazas paso a paso.
- Usa reglas de produccion para inferir clase, orden y familia.
- Presenta el resultado en una interfaz grafica mas atractiva.
