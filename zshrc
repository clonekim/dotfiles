# Use powerline
USE_POWERLINE="true"
# Has weird character width
# Example:
#    is not a diamond
HAS_WIDECHARS="false"
# Source manjaro-zsh-configuration
if [[ -e /usr/share/zsh/manjaro-zsh-config ]]; then
  source /usr/share/zsh/manjaro-zsh-config
fi
# Use manjaro zsh prompt
if [[ -e /usr/share/zsh/manjaro-zsh-prompt ]]; then
  source /usr/share/zsh/manjaro-zsh-prompt
fi

# FZF
if [[ -e /usr/share/fzf/completion.zsh ]]; then
  source /usr/share/fzf/completion.zsh
fi

if [[ -e /usr/share/fzf/key-bindings.zsh ]]; then
  source /usr/share/fzf/key-bindings.zsh
fi


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion



# -----------------------------------------------------
# Fastfetch 
# -----------------------------------------------------
if [[ $(tty) == *"pts"* ]]; then
    fastfetch --logo "${HOME}/.config/fastfetch/$(shuf -i 1-6 -n 1).txt"
else
    fastfetch --logo "${HOME}/.config/fastfetch/$(shuf -i 1-6 -n 1).txt"
fi

unsetopt correct_all
unsetopt correct

export MOZ_ENABLE_WAYLAND=1
export _JAVA_AWT_WM_NONREPARENTING=1

export JAVA_HOME=/usr/lib/jvm/default
export GRAALVM_HOME=/usr/lib/jvm/java-21-graalvm/
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

alias open='/usr/bin/xdg-open >/dev/null 2>&1'
alias vi=/usr/bin/nvim
alias vim=/usr/bin/nvim
alias ll='ls -al'
alias lh='ls -alh'


alias java21='rm -f /usr/lib/jvm/default* && ln -s /usr/lib/jvm/java-21-openjdk /usr/lib/jvm/default && ln -s /usr/lib/jvm/java-21-openjdk /usr/lib/jvm/default-runtime'
alias java24='rm -f /usr/lib/jvm/default* && ln -s /usr/lib/jvm/java-24-openjdk /usr/lib/jvm/default && ln -s /usr/lib/jvm/java-24-openjdk /usr/lib/jvm/default-runtime'
alias native21='rm -f /usr/lib/jvm/default* && ln -sf /usr/lib/jvm/java-21-graalvm /usr/lib/jvm/default && ln -sf /usr/lib/jvm/java-21-graalvm /usr/lib/jvm/default-runtime'

