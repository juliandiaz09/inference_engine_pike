# Sistema Experto de Identificación de Aves

Proyecto en Python 3.10 con un motor de inferencia basado en reglas usando Pyke
(`pyke-master` incluido localmente) y una interfaz gráfica en Tkinter.

**Versión refactorizada y enfocada netamente en aves**, con base de conocimiento verificable, documentación completa y trazabilidad detallada de reglas.

## Estructura

```
Taller 2 - Test/
├── app.py
├── requirements.txt
├── KNOWLEDGE_BASE.md          # Documentación de la base de conocimiento
├── README.md                  # Este archivo
├── README_COMPLETE.md         # Documentación detallada
├── pyke-master/              # Motor de inferencia Pyke
└── src/
    └── animal_expert_system/
        ├── __init__.py
        ├── domain.py          # Configuración del dominio (aves)
        ├── inference.py       # Motor de inferencia mejorado
        ├── gui.py             # Interfaz gráfica
        └── knowledge/
            ├── __init__.py
            ├── animals.kfb   # Base de hechos de 12 especies de aves
            ├── animal_rules.krb # Reglas principales
            ├── animal_rules_fc.krb # Reglas forward chaining
            └── animal_rules_bc.krb # Reglas backward chaining
```

## Características

- ✅ Sistema**netamente enfocado en aves**
- ✅ **12 especies verificables** basadas en taxonomía formal
- ✅ Dos modos de razonamiento: **forward chaining** y **backward chaining**
- ✅ **Trazabilidad detallada** indicando exactamente qué reglas se disparan
- ✅ **Código Python completamente en inglés**
- ✅ **Hechos, reglas e interfaz en español**
- ✅ Interfaz gráfica moderna con visualización de flujo
- ✅ Validación de coincidencias exactas

## Ejecución

1. Asegurar que Python 3.10+ esté instalado
2. Activar el entorno virtual si es necesario
3. Ejecutar:

```bash
python app.py
```

## Qué Hace

- Permite ingresar características de un ave en español (hábitat, alimentación, morfología, tamaño, actividad)
- Ofrece dos modos de razonamiento:
  - **Encadenamiento hacia adelante**: Los hechos generan conclusiones automáticamente
  - **Encadenamiento hacia atrás**: Se demuestra si un ave cumple los criterios
- Muestra un proceso visual con trazas paso a paso indicando qué reglas se disparan
- Usa reglas específicas para inferir orden y familia taxonómica
- Identifica la especie exacta de ave basada en características observables
- Presenta el resultado con clasificación taxonómica completa

## Aves Identificables

1. **Águila Real** (Aquila chrysaetos) - Accipitriformes
2. **Gavilán Cola Roja** (Buteo jamaicensis) - Accipitriformes
3. **Búho Real** (Bubo virginianus) - Strigiformes
4. **Lechuza de Campanario** (Tyto alba) - Strigiformes
5. **Cuervo Común** (Corvus corax) - Passeriformes
6. **Golondrina Azul y Blanca** (Hirundo rustica) - Passeriformes
7. **Loro Amazónico** (Amazona viridis) - Psittaciformes
8. **Paloma Común** (Columba livia) - Columbiformes
9. **Gaviota Pico Anillado** (Larus delawarensis) - Charadriiformes
10. **Cormorán Grande** (Phalacrocorax carbo) - Pelecaniformes
11. **Garza Azul** (Ardea herodias) - Pelecaniformes
12. **Grulla Canadiense** (Antigone canadensis) - Gruiformes

## Información Complementaria

Para documentación detallada sobre la base de conocimiento, combinaciones válidas de características, reglas implementadas y ejemplos de uso, consulta [KNOWLEDGE_BASE.md](KNOWLEDGE_BASE.md) y [README_COMPLETE.md](README_COMPLETE.md).
