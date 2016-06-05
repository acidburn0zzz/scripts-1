# auto-addition
autoload -U compinit promptinit 
compinit
promptinit

setopt CORRECT_ALL

SPROMPT="Error! %r instead of %R? ([Y]es/[N]o/[E]dit/[A]bort) "

# auto-cd
setopt autocd

zstyle ':completion:*' menu select=long-list select=0
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}

# aliases
bindkey ';5D' backward-word
bindkey ';5C' forward-word

alias ls='ls --color=auto'
alias grep='grep --color=auto'

# history
export HISTFILE=~/.zsh_history
export HISTSIZE=500
export SAVEHIST=$HISTSIZE

setopt APPEND_HISTORY
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_IGNORE_BLANKS
