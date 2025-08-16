import tkinter as tk

def run_mobile():
    root = tk.Tk()
    root.title("Puzzle IA")
    label = tk.Label(root, text="Selector de Algoritmo (WIP)")
    label.pack(padx=20, pady=20)

    # Aquí se pueden agregar botones para cada algoritmo
    """button_bfs = tk.Button(root, text="BFS", command=lambda: run_algorithm(bfs))
        button_dfs = tk.Button(root, text="DFS", command=lambda: run_algorithm(dfs))
        button_astar = tk.Button(root, text="A* (Manhattan)", command=lambda: run_algorithm(astar, manhattan))

        button_bfs.pack(padx=10, pady=5)
        button_dfs.pack(padx=10, pady=5)
        # button_astar.pack(padx=10, pady=5) 
    """

    root.mainloop()
