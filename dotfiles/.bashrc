if [ -f ~/.bash_aliases ]; then
	. ~/.bash_aliases
fi

# Test for an interactive shell.  There is no need to set anything
# past this point for scp and rcp, and it's important to refrain from
# outputting anything in those cases.
if [[ $- != *i* ]] ; then
	# Shell is non-interactive.  Be done now!
	return
fi

shopt -s histappend
HISTCONTROL=ignoredups:ignorespace
HISTSIZE=1000
HISTFILESIZE=2000

shopt -s checkwinsize

use_color=false
case "$TERM" in
	linux|rxvt|screen) use_color=true
esac

if ${use_color}; then
	PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w \[\033[01;31m\]$(__git_ps1 "%s ")\[\033[01;34m\]\$\[\033[00m\] '
else
	PS1='\u@\h \w $(__git_ps1 "%s ")\$ '
fi
unset use_color
