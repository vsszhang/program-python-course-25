import json
import tkinter as tk
from collections import defaultdict
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox

import networkx as nx


def build_actor_graph(data: dict) -> nx.Graph:
    """Build an actor collaboration graph from movies.json data.

       Nodes: actor names
       Edges: actors who appeared together in at least one movie
       Edge attribute:
            movies = [(title, year), ...]

    Args:
        data (dict): json with dict type

    Returns:
        nx.Graph: Networkx Graph
    """
    G = nx.Graph()

    # add all actors as nodes
    for actor in data.keys():
        G.add_node(actor)

    # build movie -> actors reverse index
    movie_to_actors = defaultdict(list)
    for actor, movies in data.items():
        for movie in movies:
            title = movie["title"]
            year = int(movie["airdate"][:4])
            movie_key = (title, year)
            movie_to_actors[movie_key].append(actor)

    # connect actors who played in the same movie
    for (title, year), actors in movie_to_actors.items():
        for i in range(len(actors)):
            for j in range(i + 1, len(actors)):
                a1, a2 = actors[i], actors[j]
                if not G.has_edge(a1, a2):
                    G.add_edge(a1, a2, movies=[])
                G[a1][a2]["movies"].append((title, year))

    return G


def shortest_actor_graph(
    graph: nx.Graph, actor: str, target: str = "Kevin Bacon"
) -> list[str] | None:
    if graph is None:
        return None
    if actor not in graph or target not in graph:
        return None

    try:
        return nx.shortest_path(graph, source=actor, target=target)
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


class BaconGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bacon Number")
        self.geometry("520x240")

        self.data = None
        self.graph = None

        # ---- UI ----
        self.btn_load = tk.Button(self, text="load", command=self.on_load)
        self.btn_load.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(self, text="Actor:").grid(row=1, column=0, padx=10, sticky="w")

        self.combo = Combobox(self, state="readonly", width=50, values=[])
        self.combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.combo.bind("<<ComboboxSelected>>", self.on_actor_selected)

        self.lbl_file = tk.Label(self, text="No file loaded", fg="gray")
        self.lbl_file.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.lbl_path = tk.Label(
            self, text="Path: (select an actor)", justify="left", wraplength=500
        )
        self.lbl_path.grid(
            row=3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w"
        )

        # grid stretching
        self.grid_columnconfigure(1, weight=1)

    def on_actor_selected(self, event=None):
        actor = self.combo.get()
        if not actor or self.graph is None:
            return

        path = shortest_actor_graph(self.graph, actor, "Kevin Bacon")
        if path is None:
            self.lbl_path.config(text=f"Path: no path from {actor} to Kevin Bacon")
            return

        bacon_number = len(path) - 1
        self.lbl_path.config(
            text=f"Path: {' -> '.join(path)}\nBacon number: {bacon_number}"
        )

    def on_load(self):
        path = filedialog.askopenfilename(
            title="Select file movies.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # expected format
            if not isinstance(data, dict):
                raise ValueError(
                    "JSON root must be an object/dict: {actor: [movies...]}"
                )

            actors = sorted(list(data.keys()))
            if not actors:
                raise ValueError("No actors found in JSON keys.")

            self.data = data
            self.graph = build_actor_graph(data)
            self.combo["values"] = actors
            self.combo.set(actors[0])
            self.on_actor_selected()
            self.lbl_file.config(text=f"Loaded: {path}", fg="black")

        except Exception as e:
            messagebox.showerror("Load error", str(e))


if __name__ == "__main__":
    app = BaconGUI()
    app.mainloop()
