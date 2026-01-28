#!/bin/bash

WAYBAR_DIR="$HOME/.config/waybar"

set_waybar_config() {
  local target="$1" # niri.jsonc / hyprland.jsonc / plasma.jsonc

  if [ -L "$WAYBAR_DIR/config.jsonc" ] || [ -e "$WAYBAR_DIR/config.jsonc" ]; then
    rm -f "$WAYBAR_DIR/config.jsonc"
  fi

  ln -s "$WAYBAR_DIR/$target" "$WAYBAR_DIR/config.jsonc"

}

case $XDG_CURRENT_DESKTOP in

hyprland | Hyprland)
  set_waybar_config "hyprland.jsonc"
  ;;
niri)
  set_waybar_config "niri.jsonc"
  ;;
*) ;;
esac
