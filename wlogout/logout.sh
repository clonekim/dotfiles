#!/bin/bash

case $XDG_SESSION_DESKTOP in
hyprland | Hyprland)
  pkill kime
  pkill foot
  pkill swaybg
  pkill swayidle
  hyprctl dispatch exit
  ;;
niri)
  pkill kime
  pkill foot
  pkill swaybg
  pkill swayidle
  niri msg action quit --skip-confirmation
  ;;
*) ;;
esac
