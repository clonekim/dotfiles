#!/usr/bin/env python3
# Minimal niri pick-color -> notify-send
# Expected niri output (JSON):
# {"rgb":[0.1294,0.1294,0.1294]}
#
# Output format:
# Picked color: rgb(R, G, B)
# Hex: #rrggbb

import json
import shutil
import subprocess
import sys

TIMEOUT_MS = 60000


def notify(summary: str, body: str) -> None:
    if shutil.which("notify-send"):
        subprocess.run(
            ["notify-send", "-t", str(TIMEOUT_MS), summary, body], check=False
        )


def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def to_u8(v) -> int:
    f = clamp01(float(v))
    return int(round(f * 255.0))


def main() -> int:
    try:
        p = subprocess.run(
            ["niri", "msg", "--json", "pick-color"],
            text=True,
            capture_output=True,
        )
        if p.returncode != 0:
            raise RuntimeError(
                ((p.stderr or p.stdout) or "niri pick-color failed").strip()
            )

        obj = json.loads(p.stdout.strip() or "{}")
        rgb = obj.get("rgb", [0.0, 0.0, 0.0])

        r, g, b = (to_u8(rgb[0]), to_u8(rgb[1]), to_u8(rgb[2]))
        hexv = f"#{r:02x}{g:02x}{b:02x}"

        msg = f"Picked color: rgb({r}, {g}, {b})\nHex: {hexv}"
        notify("niri pick-color", msg)
        return 0

    except Exception as e:
        err = str(e).strip() or "unknown error"
        print(err, file=sys.stderr)
        notify("niri pick-color (error)", err)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
