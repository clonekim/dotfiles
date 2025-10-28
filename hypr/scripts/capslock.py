#!/usr/bin/env python3

import json
import os
import socket

sock = f"{os.environ['XDG_RUNTIME_DIR']}/hypr/{os.environ['HYPRLAND_INSTANCE_SIGNATURE']}/.socket.sock"
with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
    s.connect(sock)
    s.sendall(b"j/devices")  # hyprctl -j devices 와 동일
    data = s.recv(4_000_000)

caps_on = any(k["capsLock"] for k in json.loads(data.decode())["keyboards"])
print("Caps" if caps_on else "")
