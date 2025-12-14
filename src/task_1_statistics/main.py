from __future__ import annotations

from pathlib import Path

import pandas as pd

COLS = {"TIME", "EVENT", "AVGTSMR"}


def find_header_line_idx(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        s = line.strip()

        # Skip the description line
        if not s or s.startswith("["):
            continue

        cols = s.split("\t")
        if len(cols) < 3:
            cols = s.split()

        if COLS.issubset(set(cols)):
            return i

    raise ValueError("[WARIN] Header line not found: TIME/EVENT/AVGTSMR")


def load_data_txt(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    header_i = find_header_line_idx(lines)
    header = lines[header_i].strip().split("\t")

    # parse the data line, at the begining of harder
    rows = []
    for raw in lines[header_i + 1 :]:
        s = raw.strip()

        # skip blank line
        if not s:
            continue

        # split by tab if present, otherwise by whitespace
        parts = s.split("\t") if "\t" in s else s.split()
        if len(parts) < 2:
            continue

        # determine whether real data row or not
        if parts[0].startswith("[") and parts[0].endswith("]"):
            parts[0] = parts[0].strip("[]")
        if not parts[1].isalpha():
            continue

        if len(parts) < len(header):
            parts += [""] * (len(header) - len(parts))
        elif len(parts) > len(header):
            parts = parts[: len(header)]

        rows.append(parts)

    df = pd.DataFrame(rows, columns=header)

    # keep the EVENT and AVGTSMR
    df["AVGTSMR"] = pd.to_numeric(df["AVGTSMR"], errors="coerce")
    df = df.dropna(subset=["EVENT", "AVGTSMR"])

    return df


if __name__ == "__main__":
    df = load_data_txt("src/task_1_statistics/data.txt")
    print(df.head())
    print(df["EVENT"].value_counts().head())
