#!/usr/bin/env python3

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


def main() -> int:
    try:
        p = subprocess.run(
            ["niri", "msg", "--json", "pick-window"],
            text=True,
            capture_output=True,
            check=True,
        )

        obj = json.loads(p.stdout.strip() or "{}")

        title = obj.get("title")
        wid = obj.get("id")
        pid = obj.get("pid")
        floating = obj.get("is_floating")

        msg = f"Title: {title}\nId: {wid}\nPid: {pid}\nFloating: {floating}"
        notify("niri pick-window", msg)
        return 0

    except Exception as e:
        err = str(e).strip() or "unknown error"
        print(err, file=sys.stderr)
        notify("niri pick-window (error)", err)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
