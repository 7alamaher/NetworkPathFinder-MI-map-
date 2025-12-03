import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

from algorithms import second_best_path
from map_display import build_map_figure


def create_gui(G):

    window = tk.Tk()
    window.title("Dijkstra Path Comparison")
    window.geometry("800x1200")

    # map Display
    map_frame = tk.Frame(window)
    map_frame.pack(side="left", padx=90, pady=10)

    fig = build_map_figure(G)
    canvas = FigureCanvasTkAgg(fig, master=map_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    cities = list(G.nodes())

    right_frame = tk.Frame(window)
    right_frame.pack(side="right", fill="y", padx=150, pady=(200))

    sg_frame = tk.Frame(right_frame)
    sg_frame.pack(pady=10)

    tk.Label(sg_frame, text="Start City:", font=("Arial", 12)).grid(row=0, column=0, padx=10)
    start_cb = ttk.Combobox(sg_frame, values=cities, state="readonly", width=18)
    start_cb.grid(row=1, column=0, padx=10)

    tk.Label(sg_frame, text="Goal City:", font=("Arial", 12)).grid(row=0, column=1, padx=10)
    goal_cb = ttk.Combobox(sg_frame, values=cities, state="readonly", width=18)
    goal_cb.grid(row=1, column=1, padx=10)

    output = tk.Text(right_frame, height=27, width=90)
    output.pack(pady=10)

    #runs dijkstra
    def run_dijkstra_compare():

        start = start_cb.get()
        goal = goal_cb.get()

        output.delete("1.0", tk.END)

        if not start or not goal:
            output.insert(tk.END, "Please choose both cities.\n")
            return

        #check invalid direct road (no direct edge)
        invalid_pair = None
        if goal not in G[start]:
            invalid_pair = (start, goal)

        #check if any path exists
        if not nx.has_path(G, start, goal):
            output.insert(tk.END, f"No valid route exists between {start} and {goal}.\n")
            new_fig = build_map_figure(G, invalid_pair=invalid_pair)
            canvas.figure = new_fig
            canvas.draw()
            return

        #compute valid paths
        p1, dist1, p2, dist2, nodes1, nodes2 = second_best_path(G, start, goal)

        #update map with valid paths and dotted invalid path
        new_fig = build_map_figure(G, p1, p2, invalid_pair)
        canvas.figure = new_fig
        canvas.draw()

        #shortest path
        output.insert(tk.END, "===== THE SHORTEST PATH =====\n")
        output.insert(tk.END, "Sequence of Cities:\n")
        output.insert(tk.END, " → ".join(p1) + "\n")
        output.insert(tk.END, f"Total Distance: {dist1} miles\n\n")

        #second-shortest path
        output.insert(tk.END, "===== THE SECOND SHORTEST PATH =====\n")
        if p2 is None:
            output.insert(tk.END, "No valid alternate path exists.\n")
            return

        output.insert(tk.END, "Sequence of Cities:\n")
        output.insert(tk.END, " → ".join(p2) + "\n")
        output.insert(tk.END, f"Total Distance: {dist2} miles\n\n")

        #summary
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
        f"Nodes Expanded (Shortest Path): {nodes1}\n"
            f"Nodes Expanded (Second Best Path): {nodes2}\n"
            "Complexity: O((V + E) log V)\n\n")

        output.insert(tk.END,f"Optimal Path:\n")
        output.insert(tk.END, " → ".join(p1) + "\n")
    #show Paths Button
    style = ttk.Style()
    style.configure("BigButton.TButton", font=("Arial", 13))

    ttk.Button(
        right_frame,
        text="Show Paths",
        command=run_dijkstra_compare,
        width=10,
        style="BigButton.TButton"
    ).pack(pady=20, ipadx=5, ipady=8)

    window.mainloop()
