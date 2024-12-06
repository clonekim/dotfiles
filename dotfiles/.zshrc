# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

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
#if [[ -e /usr/share/zsh/manjaro-zsh-prompt ]]; then
#  source /usr/share/zsh/manjaro-zsh-prompt
#fi

# FZF
if [[ -e /usr/share/fzf/completion.zsh ]]; then
  source /usr/share/fzf/completion.zsh
fi

if [[ -e /usr/share/fzf/key-bindings.zsh ]]; then
  source /usr/share/fzf/key-bindings.zsh
fi

unsetopt correct_all
unsetopt correct

export NVM_DIR="$HOME/.config/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

if [ $TILIX_ID ] || [ $VTE_VERSION ]; then
	source /etc/profile.d/vte.sh
fi

export JAVA_HOME=/usr/lib/jvm/default
export GRAALVM_HOME=/usr/lib/jvm/java-21-graalvm/
export PATH=$PATH:$GRAALVM_HOME/bin

alias vi=/usr/bin/vim
alias vim=/usr/bin/nvim
alias ll='ls -al'
alias lh='ls -alh'
alias open='xdg-open'
alias java17='rm -f /usr/lib/jvm/default* && ln -s /usr/lib/jvm/java-17-openjdk /usr/lib/jvm/default && ln -s /usr/lib/jvm/java-17-openjdk /usr/lib/jvm/default-runtime'
alias java21='rm -f /usr/lib/jvm/default* && ln -s /usr/lib/jvm/java-21-openjdk /usr/lib/jvm/default && ln -s /usr/lib/jvm/java-21-openjdk /usr/lib/jvm/default-runtime'
alias graal21='rm -f /usr/lib/jvm/default* && ln -sf /usr/lib/jvm/java-21-graalvm /usr/lib/jvm/default && ln -sf /usr/lib/jvm/java-21-graalvm /usr/lib/jvm/default-runtime'

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
source /usr/share/zsh-theme-powerlevel10k/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
