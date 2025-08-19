## Puzzle-IA: Solucionador de Rompecabezas 8-Puzzle

Este proyecto es una aplicación interactiva desarrollada en Python utilizando la librería Kivy. Su objetivo es visualizar y resolver el clásico rompecabezas 8-Puzzle utilizando diferentes algoritmos de búsqueda informada y no informada de la Inteligencia Artificial.

La aplicación permite a los usuarios seleccionar un algoritmo y una heurística, ejecutar la búsqueda de la solución y ver los pasos de la solución en tiempo real, junto con las métricas de rendimiento del algoritmo.
Ademas de hacer poder crear un cuadro comparativo entre las heuristicas con un grafico

### Algoritmos de Búsqueda Implementados

Búsqueda No Informada:
    BFS (Breadth-First Search)
    DFS (Depth-First Search)
    UCS (Uniform-Cost Search)

Búsqueda Informada:
    Greedy (Greedy Best-First Search)
    A* (A-Star Search)
    Weighted A* (Weighted A-Star Search)
    IDA* (Iterative Deepening A-Star)

### Heurísticas Implementadas

Para los algoritmos de búsqueda informada, se pueden seleccionar las siguientes heurísticas:

    Manhattan: Suma de las distancias de cada ficha a su posición objetivo.

    Misplaced: Cuenta el número de fichas que no están en su posición correcta.

    Linear Conflict: Una mejora de la distancia de Manhattan que cuenta los pares de fichas en la misma fila o columna que están en conflicto.

Requisitos y Dependencias

    Kivy: El framework de Python para el desarrollo de aplicaciones.
    matplotlib: Para crear el grafico comparativo

Instalación y Uso

    Clonar el repositorio

~~~bash
    git clone https://github.com/PinchaoRamiroA/Ia_Problems.git
    cd Ia_Problems/pizzle_ia
~~~

    Instalar dependencias:
~~~bash
    pip install kivy
    pip install matplotlib
~~~
    Ejecutar la aplicación:
~~~bash
    python main.py
~~~

Una vez que la aplicación se inicie, usa los menús desplegables para seleccionar un algoritmo y una heurística (si el algoritmo lo requiere) y luego presiona el botón "play" para resolver el rompecabezas y ver la animación de la solución.