#!/usr/bin/env python3

"""
Hyprland Scratchpad Manager
A Python implementation using direct IPC socket communication
Based on the original bash script by Nikhil Singh <nik.singh710@gmail.com>
"""

import datetime
import json
import os
import socket
import sys
import argparse
import subprocess
import shutil
from typing import Dict, List, Optional


class Colors:
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    YELLOW = "\033[0;33m"
    RESET = "\033[0m"


class HyprlandIPC:
    def __init__(self):
        self.scratchpad_name = os.environ.get("HYPRLAND_SCRATCHPAD_NAME", "scratchpad")
        self.menu_cmd = ["rofi", "-dmenu", "-i", "-p", "scratchpad"]

        # Hyprland IPC 소켓 경로
        runtime_dir = os.environ.get("XDG_RUNTIME_DIR")
        hypr_instance = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")

        if not runtime_dir or not hypr_instance:
            self.log("error", "Hyprland environment variables not found")
            sys.exit(1)

        self.socket_path = f"{runtime_dir}/hypr/{hypr_instance}/.socket.sock"
        self.socket2_path = f"{runtime_dir}/hypr/{hypr_instance}/.socket2.sock"
        self.log_path = f"{runtime_dir}/hypr/{hypr_instance}/hyprland.log"

        # 소켓 존재 확인
        if not os.path.exists(self.socket_path):
            self.log("error", "Hyprland IPC socket not found")
            sys.exit(1)

    def log(self, level: str, message: str):
        """로그 출력"""
        if level == "ok":
            icon = "✓"
            color = Colors.GREEN
        elif level == "error":
            icon = "✗"
            color = Colors.RED
        elif level == "info":
            icon = "ℹ"
            color = Colors.BLUE
        elif level == "warn":
            icon = "⚠"
            color = Colors.YELLOW
        else:
            icon = "•"
            color = Colors.RESET

        print(f"[{color}{icon}{Colors.RESET}] {message}")

        # 파일에 로그 기록
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_msg = f"[{timestamp}] [{level.upper()}] {message}\n"

            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(log_msg)

        except Exception as e:
            # 로그 파일 쓰기 실패 시 콘솔에만 에러 출력 (무한 루프 방지)
            print(f"[{Colors.RED}✗{Colors.RESET}] Failed to write log file: {e}")

    def notify(self, title: str, message: str = ""):
        """알림 발송"""
        if shutil.which("notify-send"):
            try:
                subprocess.run(["notify-send", title, message], check=True)
            except subprocess.CalledProcessError:
                print(f"{title}: {message}")
        else:
            print(f"{title}: {message}")

    def send_command(self, command: str) -> Optional[str]:
        """Hyprland IPC 소켓으로 명령어 전송"""
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(self.socket_path)
                s.sendall(command.encode())

                response = b""
                while True:
                    data = s.recv(8192)
                    if not data:
                        break
                    response += data

                return response.decode("utf-8").strip()
        except Exception as e:
            self.log("error", f"Failed to send command '{command}': {e}")
            return None

    def get_json_data(self, command: str) -> Optional[Dict]:
        """JSON 형태의 응답을 받는 명령어 실행"""
        response = self.send_command(f"j/{command}")
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError as e:
                self.log("error", f"Failed to parse JSON response: {e}")
        return None

    def dispatch(self, action: str) -> bool:
        """Hyprland dispatch 명령어 실행"""
        response = self.send_command(f"dispatch {action}")
        return response is not None

    def check_dependencies(self):
        """의존성 체크"""
        print("Checking dependencies...")

        required_deps = ["jq"]
        optional_deps = ["notify-send", "rofi", "bemenu"]

        for dep in required_deps:
            if shutil.which(dep):
                self.log("ok", dep)
            else:
                self.log("error", f"{dep} - Required")

        for dep in optional_deps:
            if shutil.which(dep):
                self.log("ok", f"{dep} (Optional)")
            else:
                self.log("info", f"{dep} (Optional)")

        # Hyprland 소켓 상태 체크
        if os.path.exists(self.socket_path):
            self.log("ok", "Hyprland IPC socket")
        else:
            self.log("error", "Hyprland IPC socket")

    def get_current_workspace(self) -> Optional[str]:
        """현재 워크스페이스 가져오기"""
        monitors = self.get_json_data("monitors")
        if not monitors:
            return None

        for monitor in monitors:
            if monitor.get("focused"):
                return monitor.get("activeWorkspace", {}).get("name")
        return None

    def get_scratchpad_clients(self) -> List[Dict]:
        """scratchpad의 클라이언트 목록 가져오기"""
        clients = self.get_json_data("clients")
        if not clients:
            return []

        scratchpad_clients = []
        for client in clients:
            workspace_name = client.get("workspace", {}).get("name", "")
            if workspace_name == f"special:{self.scratchpad_name}":
                client_info = {
                    "class": client.get("class", ""),
                    "title": client.get("title", ""),
                    "address": client.get("address", ""),
                    "pid": client.get("pid", ""),
                    "floating": client.get("floating", False),
                }
                client_info["display"] = (
                    f"{client_info['class']} - {client_info['title']}"
                )
                scratchpad_clients.append(client_info)

        return scratchpad_clients

    def get_active_window(self) -> Optional[Dict]:
        """현재 활성 창 정보 가져오기"""
        return self.get_json_data("activewindow")

    def send_to_scratchpad(self):
        """현재 포커스된 창을 scratchpad로 보내기"""
        active_window = self.get_active_window()
        if not active_window or not active_window.get("address"):
            self.log("error", "No active window found")
            return

        window_title = active_window.get("title", "Unknown")
        window_class = active_window.get("class", "Unknown")

        if self.dispatch(f"movetoworkspacesilent special:{self.scratchpad_name}"):
            self.log(
                "ok",
                f"Window '{window_class} - {window_title}' moved to {self.scratchpad_name}",
            )
            self.notify("Scratchpad", f"Window moved to {self.scratchpad_name}")
        else:
            self.log("error", "Failed to move window to scratchpad")

    def list_scratchpad_clients(self):
        """스크래치패드 클라이언트 목록 출력"""
        clients = self.get_scratchpad_clients()

        if not clients:
            self.log("info", f"No clients found in {self.scratchpad_name}")
            return

        print(
            f"\n{Colors.BLUE}Scratchpad '{self.scratchpad_name}' contents:{Colors.RESET}"
        )
        print(f"{Colors.BLUE}{'=' * 50}{Colors.RESET}")

        for i, client in enumerate(clients, 1):
            status = "🎈" if client["floating"] else "📌"
            print(f"{i:2d}. {status} {Colors.GREEN}{client['class']}{Colors.RESET}")
            print(f"     📝 {client['title']}")
            print(f"     🆔 {client['address']}")
            print()

        print(f"{Colors.BLUE}Total: {len(clients)} windows{Colors.RESET}")

    def browse_and_restore(self):
        """rofi를 통해 스크래치패드 클라이언트를 선택하고 복구"""
        # 기존 메뉴 프로세스 종료
        menu_program = self.menu_cmd[0]
        try:
            subprocess.run(["killall", "-q", menu_program], capture_output=True)
        except subprocess.CalledProcessError:
            pass

        current_workspace = self.get_current_workspace()
        if not current_workspace:
            self.notify("Error", "Could not get current workspace")
            return

        clients = self.get_scratchpad_clients()

        if not clients:
            self.notify("No Clients", f"No clients found in {self.scratchpad_name}")
            return

        # rofi 메뉴용 클라이언트 목록 생성
        menu_items = []
        for client in clients:
            status_icon = "🎈" if client["floating"] else "📌"
            display_text = f"{status_icon} {client['class']} - {client['title']}"
            menu_items.append(display_text)

        client_list = "\n".join(menu_items)

        try:
            # rofi로 선택
            result = subprocess.run(
                self.menu_cmd,
                input=client_list,
                text=True,
                capture_output=True,
                check=True,
            )

            selected_display = result.stdout.strip()
            if not selected_display:
                self.log("info", "No selection made")
                return

            # 선택된 항목과 매칭되는 클라이언트 찾기
            selected_client = None
            for i, display_text in enumerate(menu_items):
                if display_text == selected_display:
                    selected_client = clients[i]
                    break

            if not selected_client:
                self.log("error", "Selected client not found")
                return

            # 선택된 클라이언트를 현재 워크스페이스로 이동
            address = selected_client["address"]

            success1 = self.dispatch(
                f"movetoworkspace {current_workspace},address:{address}"
            )
            success2 = self.dispatch(f"focuswindow address:{address}")

            if success1 and success2:
                # 플로팅 창이면 위로 가져오기
                if selected_client["floating"]:
                    self.dispatch("bringactivetotop")

                self.log(
                    "ok",
                    f"Client '{selected_client['class']} - {selected_client['title']}' restored to {current_workspace}",
                )
                self.notify("Restored", f"{selected_client['class']} restored")
            else:
                self.log("error", "Failed to restore client")

        except subprocess.CalledProcessError:
            self.log("info", "Menu cancelled by user")
            return
        except KeyboardInterrupt:
            self.log("info", "Operation cancelled")
            return

    def show_scratchpad_count(self):
        """스크래치패드의 클라이언트 개수 표시"""
        clients = self.get_scratchpad_clients()
        print(len(clients))

    def set_menu_command(self, menu_cmd: str):
        """메뉴 명령어 설정"""
        self.menu_cmd = menu_cmd.split()

    def set_scratchpad_name(self, name: str):
        """scratchpad 이름 설정"""
        self.scratchpad_name = name

    def get_workspaces(self) -> List[Dict]:
        """모든 워크스페이스 정보 가져오기"""
        return self.get_json_data("workspaces") or []

    def get_version(self) -> Optional[str]:
        """Hyprland 버전 정보 가져오기"""
        return self.send_command("version")


def create_parser():
    """명령행 인자 파서 생성"""
    parser = argparse.ArgumentParser(
        description="Hyprland Scratchpad Manager - Move windows to/from scratchpad using IPC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Show this help message
  %(prog)s -s                 # Send focused window to scratchpad
  %(prog)s -l                 # List scratchpad clients
  %(prog)s -l -b             # Browse and restore via rofi menu
  %(prog)s --count            # Show number of windows in scratchpad
  %(prog)s -m "bemenu"        # Use bemenu instead of rofi
  %(prog)s -n myscratch       # Use custom scratchpad name

Key bindings example (hyprland.conf):
  bind = SUPER, s, exec, /path/to/scratchpad.py -s
  bind = SUPER_CTRL, s, exec, /path/to/scratchpad.py -l -b
        """,
    )

    parser.add_argument(
        "-s", "--send", action="store_true", help="Send focused window to scratchpad"
    )

    parser.add_argument(
        "-l", "--list", action="store_true", help="List scratchpad clients"
    )

    parser.add_argument(
        "-b",
        "--browse",
        action="store_true",
        help="Browse scratchpad clients via menu and restore selected one (use with -l)",
    )

    parser.add_argument(
        "-m",
        "--menu",
        type=str,
        help="Set menu program (e.g., 'rofi -dmenu -i' or 'bemenu')",
    )

    parser.add_argument(
        "-n", "--name", type=str, help="Set scratchpad name (default: 'scratchpad')"
    )

    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Check dependencies and Hyprland status",
    )

    parser.add_argument(
        "--count", action="store_true", help="Show count of windows in scratchpad"
    )

    parser.add_argument("--version", action="store_true", help="Show Hyprland version")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    try:
        ipc = HyprlandIPC()
    except SystemExit:
        return

    # 옵션 설정
    if args.menu:
        ipc.set_menu_command(args.menu)

    if args.name:
        ipc.set_scratchpad_name(args.name)

    # 액션 실행
    if args.check:
        ipc.check_dependencies()
    elif args.send:
        # -s: 현재 창을 scratchpad로 보내기
        ipc.send_to_scratchpad()
    elif args.list and args.browse:
        # -l -b: rofi를 통한 브라우징 및 복구
        ipc.browse_and_restore()
    elif args.list:
        # -l: 클라이언트 목록만 출력
        ipc.list_scratchpad_clients()
    elif args.count:
        # --count: 스크래치패드 클라이언트 개수
        ipc.show_scratchpad_count()
    elif args.version:
        # --version: Hyprland 버전 표시
        version = ipc.get_version()
        if version:
            print(version)
        else:
            ipc.log("error", "Could not get Hyprland version")
    else:
        # 기본 동작: 도움말 표시
        parser.print_help()
        print(f"\n{Colors.BLUE}Quick Start:{Colors.RESET}")
        print("  scratchpad.py -s           # Send current window to scratchpad")
        print("  scratchpad.py -l           # List scratchpad contents")
        print("  scratchpad.py -l -b        # Browse and restore via menu")
        print("  scratchpad.py --count      # Show scratchpad window count")


if __name__ == "__main__":
    main()
