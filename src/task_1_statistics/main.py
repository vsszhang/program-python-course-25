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
    # Переделать загрузку файла:
    # Использовать pd.read_csv(имя_файла, для корректной загрузки настроить параметры sep, skiprows)
    path = Path(path)
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    header_i = find_header_line_idx(lines)

    # care for the TAB-separated
    header_line = lines[header_i]
    sep = "\t" if "\t" in header_line else r"\s+"

    df = pd.read_csv(
        path,
        sep=sep,
        engine="python",
        skiprows=header_i,
        header=0,
    )

    # Keep only required columns
    df = df[["TIME", "EVENT", "AVGTSMR"]]

    # TIME values in data rows look like "[14:10:27]"; strip brackets for consistency
    df["TIME"] = df["TIME"].astype(str).str.strip("[]")

    # ensure numeric type for AVGTSMR
    df["AVGTSMR"] = pd.to_numeric(df["AVGTSMR"], errors="coerce")

    # drop broken rows
    df = df.dropna(subset=["EVENT", "AVGTSMR"])
    return df


if __name__ == "__main__":
    df = load_data_txt("src/task_1_statistics/data.txt")

    # ========= task 1: output statistics =========
    q = df.groupby("EVENT")["AVGTSMR"].quantile([0.5, 0.9, 0.99, 0.999])
    q_df = q.unstack()

    m = df.groupby("EVENT")["AVGTSMR"].min().to_frame("min")

    result = q_df.join(m)
    result = result.rename(
        columns={
            0.5: "50%",
            0.9: "90%",
            0.99: "99%",
            0.999: "99.9%",
        }
    )
    for event, row in result.iterrows():
        print(
            f"{event} "
            f"min={int(row['min'])} "
            f"50%={int(row['50%'])} "
            f"90%={int(row['90%'])} "
            f"99%={int(row['99%'])} "
            f"99.9%={int(row['99.9%'])}"
        )

    # ========= task 2: output ExecTime bucket table =========
    df["ExecTime"] = (df["AVGTSMR"] // 5) * 5

    table = (
        df["ExecTime"]
        .value_counts()
        .sort_index()
        .to_frame("TransNo")
        .reset_index(names="ExecTime")
    )

    total = table["TransNo"].sum()

    # weight,%: percent of total txs in this ExecTime bucket
    table["Weight,%"] = table["TransNo"] / total * 100

    # persent: cumulative persent of txs with ExecTime <= current bucket
    table["Percent"] = (table["TransNo"].cumsum() / total) * 100

    print(table.round(2).to_string(index=False))
