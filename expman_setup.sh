#!/bin/bash
export PATH="$PATH:$HOME/ExpMan/bin"
chmod +x $PWD/ExpMan/expman.py
if [ ! -f /bin/expman ]; then	
	sudo ln -s $PWD/ExpMan/expman.py /bin/expman
fi


