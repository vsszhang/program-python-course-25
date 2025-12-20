# Task 3 Graph GUI

## 1. Program Startup
- **`main`**
  - Entry point of the program.
  - Creates the GUI application and starts the Tkinter event loop.

- **`BaconGUI.__init__()`**
  - Initializes the main window, UI widgets, and embedded Matplotlib canvas.

---

## 2. Load Data and Build Graph
- **`BaconGUI.on_load()`**
  - Handles the “Load” button click: reads the JSON file, builds the graph, computes layout, and initializes the UI state.

- **`build_actor_graph(data)`**
  - Builds an undirected actor collaboration graph from JSON data, storing shared movies as edge attributes.

- **`nx.spring_layout(graph, ...)`**
  - Computes 2D positions for graph nodes for visualization.

- **`BaconGUI.draw_graph(None)`**
  - Draws the full actor graph without highlighting any path.

---

## 3. Actor Selection and Path Computation
- **`BaconGUI.on_actor_selected(event=None)`**
  - Triggered when an actor is selected; computes the shortest path and updates text and visualization.

- **`shortest_actor_graph(graph, actor, target="Kevin Bacon")`**
  - Computes the shortest path between the selected actor and Kevin Bacon using NetworkX.

---

## 4. Graph Visualization and Highlighting
- **`BaconGUI.draw_graph(path)`**
  - Draws the actor graph and highlights the edges and nodes belonging to the shortest path.

---

## 5. Event Loop
- **`app.mainloop()`**
  - Runs the Tkinter event loop and waits for user interactions.