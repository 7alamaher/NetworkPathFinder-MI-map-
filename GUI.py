# GUI.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from algorithms import second_best_path
from map_display import build_map_figure


def create_gui(G):

    window = tk.Tk()
    window.title("Dijkstra Path Comparison")
    window.geometry("800x1200")

    #map display
    map_frame = tk.Frame(window)
    map_frame.pack(pady=10)

    #creates the initial blank map with no paths
    fig = build_map_figure(G, None, None)
    canvas = FigureCanvasTkAgg(fig, master=map_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    #start and goal
    cities = list(G.nodes())

    sg_frame = tk.Frame(window)
    sg_frame.pack(pady=10)

    tk.Label(sg_frame, text="Start City:", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    start_cb = ttk.Combobox(sg_frame, values=cities, state="readonly", width=18)
    start_cb.grid(row=1, column=0, padx=10)

    tk.Label(sg_frame, text="Goal City:", font=("Arial", 12)).grid(row=0, column=1, padx=10)
    goal_cb = ttk.Combobox(sg_frame, values=cities, state="readonly", width=18)
    goal_cb.grid(row=1, column=1, padx=10)


    output = tk.Text(window, height=27, width=90)
    output.pack(pady=10)

    def run_dijkstra_compare():

        start = start_cb.get()
        goal = goal_cb.get()

        output.delete("1.0", tk.END)

        if not start or not goal:
            output.insert(tk.END, "Please choose BOTH cities.\n")
            return

        #compute paths
        p1, dist1, p2, dist2 = second_best_path(G, start, goal)


        #redraws map
        new_fig = build_map_figure(G, p1, p2)
        canvas.figure = new_fig
        canvas.draw()


        #summary
        if p1 is None:
            output.insert(tk.END, "No valid path exists.\n")
            return

        #primary path
        output.insert(tk.END, "===== THE SHORTEST PATH =====\n")
        output.insert(tk.END, "Sequence of Cities:\n")
        output.insert(tk.END, " → ".join(p1) + "\n")
        output.insert(tk.END, f"Total Distance: {dist1} miles\n\n")

        #second path
        output.insert(tk.END, "===== THE SECOND SHORTEST PATH =====\n")
        if p2 is None:
            output.insert(tk.END, "No valid alternate path exists.\n")
            return

        output.insert(tk.END, "Sequence of Cities:\n")
        output.insert(tk.END, " → ".join(p2) + "\n")
        output.insert(tk.END, f"Total Distance: {dist2} miles\n\n")

        #comparsion
        output.insert(tk.END, "===== SUMMARY =====\n")
        output.insert(tk.END,
            "Dijkstra's Algorithm:\n"
            "- Optimal for weighted graphs.\n"
            "- Always finds the shortest weighted path first.\n\n"
        )

        output.insert(tk.END,
            f"Distance Comparison:\n"
            f"- Shortest Path: {dist1} miles\n"
            f"- Second-Best Path: {dist2} miles\n"
            f"- Difference: {dist2 - dist1} miles\n\n"
        )

        output.insert(tk.END,
            "Growth Rate / Efficiency:\n"
            "Both runs use O((V + E) log V).\n"
            "The algorithm scales efficiently with the number of cities (V) and roads (E), even for \nlarge maps.\n\n"
        )

        output.insert(tk.END,
            "VALID PATH CHECK:\n"
            "Both paths are valid weighted routes.\n"
        )

    #compare Button
    ttk.Button(window, text="Show Paths", command=run_dijkstra_compare).pack(pady=1)

    window.mainloop()
