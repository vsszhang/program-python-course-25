# Python Course Assignment of FKI MSU 2025
This is a uv python project for FKI MSU 2025 python course assignment.

The assignment have three tasks:
- Task 1: statistics (with Pandas)
- Task 2: physics problem (with NumPy, Matplotlib)
- Task 3: graph GUI (with Tkinter, NetworkX, Matplotlib)

This project is based on a [uv](https://docs.astral.sh/uv/) monorepo scaffold, so make sure u are already install the uv!

All the code is under the directory `./src/`, as u can see that, every task is named by the format "task_n_xxxxx".

## How to run the task project
⚠️ Before running the project, make sure u are always under the base workspace.

🚀 So, let's rock and roll...

### Step 1: Build the project
Install the required packages.
```bash
uv sync --all-packages
```

### Step 2: Run the project
Choose one script and run the following command.
```bash
# Task 1
uv run --package task-1-statistics ./src/task_1_statistics/main.py

# Task 2
uv run --package task-2-physics-problem ./src/task_2_physics_problem/main.py

# Task 3
uv run --package task-3-graph ./src/task_3_graph/main.py
```