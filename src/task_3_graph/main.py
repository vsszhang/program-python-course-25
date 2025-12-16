import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox


class BaconGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bacon Number")
        self.geometry("520x160")

        self.data = None

        # ---- UI ----
        self.btn_load = tk.Button(self, text="load", command=self.on_load)
        self.btn_load.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        tk.Label(self, text="Actor:").grid(row=1, column=0, padx=10, sticky="w")

        self.combo = Combobox(self, state="readonly", width=50, values=[])
        self.combo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.lbl_file = tk.Label(self, text="No file loaded", fg="gray")
        self.lbl_file.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # grid stretching
        self.grid_columnconfigure(1, weight=1)

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
            self.combo["values"] = actors
            self.combo.set(actors[0])
            self.lbl_file.config(text=f"Loaded: {path}", fg="black")

        except Exception as e:
            messagebox.showerror("Load error", str(e))


if __name__ == "__main__":
    app = BaconGUI()
    app.mainloop()
