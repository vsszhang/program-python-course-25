from __future__ import annotations

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

        if COLS.issubclass(set(cols)):
            return i

    raise ValueError("[WARIN] Header line not found: TIME/EVENT/AVGTSMR")


def main():
    print("Hello from task-1-statistics!")


if __name__ == "__main__":
    main()
