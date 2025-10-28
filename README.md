# dotfiles
> Archlinux 기반으로 작성
## Post setup

1. 미러 설정
   ```sh
   sudo pacman-mirrors -c Global,Japan,Vietnam
   sudo pacman -Syu
   ```

2. 필수 라이브러리
   ```sh
   sudo pacman -S base-devel yay
   ```

3. 크롬 라이브러리
   ```sh
   yay -S google-chrom --cleanafter
   ```

4. 한글입력기
   ```sh
   yay -S kime-bin
   ```
   */etc/environment*
     > GTK_IM_MODULE=kime  
     > QT_IM_MODULE=kime  
     > XMODIFIERS=@im=kime  
  wayland를 기반으로 사용한다면   XMODIFIERS 만 설정한다.  
  그 외 kime-check를 통해서 IME 작동여부를 확인가능하다.

5. VSCode
   ```sh
   yay -S visual-studio-code-bin
   ```

5. Java
   ```sh
   sudo pacman -S jdk21-openjdk
   ```

## Hyprland

```sh
sudo pacman -S hyprland \
               hyprutils \
               hyprcursor \
               hyprlock \
               hyprpaper \
               hyprpolkitagent \
               rofi \
               waybar \
               wl-clipboard \
               grim \
               slurp \
               fastfetch \
               jq \
               mako \
               udiskie \
               xdg-desktop-portal-hyprland --needed
```

