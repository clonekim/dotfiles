# hyprland
Hyprland 설정
> Arch(XFCE4) 기반에서 작성 했음 

## Prerequiste

* hyprland
* hyprpaper
* hyprlock
* waybar
* rofi-wayland
* alacritty
* dunst
* nwg-drawer
* nwg-look
* xdg-desktop-portal-hyprland
* xdg-desktop-portal-wlr
* qt5-wayland
* qt6-wayland
* awesome-terminal-fonts
* ttf-font-awesome
* ttf-fira-sans 
* ttf-fira-code 
* ttf-firacode-nerd
* ttf-d2coding-nerd
* fastfetch
* fuse2
* gtk4
* libadwaita
* jq
* python-gobject
* udiskie
* brightnessctl
* pamixer 
* grim
* wl-clipboard
* thunar

## 로그인 

```
pacman -S greetd greetd-tuigreet
```

_/etc/greetd/config.toml_

```
[terminal]
type = "wayland"
vt = 1

[default_session]
command = "tuigreet"
user = "로그인 프롬프트에 표시할 사용자 ID 혹은 호스트명"
```

```sh
sudo systemctl disable lightdm.sevice
sudo systemctl enable greetd.service
```

## 모니터

`hyprctl monitors all` 로 확인 후 설정 할 것  
아래는 예시 
```
# See https://wiki.hyprland.org/Configuring/Monitors/
monitor=HDMI-A-1,1920x1080,auto,1,transform,3
monitor=DP-2,1920x1080,auto,1,transform,1
``` 


## 키바인딩

아래는 사용하지 않는다.  
`bind = $mainMod, M, exit # Exit Hyprland`


> 변경 전
`bind = $mainMod CTRL, RETURN, exec, rofi -show drun `

> 변경 후
`bind = $mainMod, D, exec, rofi -show drun # Open rofi`

