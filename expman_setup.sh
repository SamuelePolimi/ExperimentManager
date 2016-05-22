#!/bin/bash
export PATH="$PATH:$HOME/ExpMan/bin"
mkdir $HOME/ExpMan/bin
chmod +x $PWD/ExpMan/expman.py
ln -s $PWD/ExpMan/expman.py $HOME/ExpMan/bin/expman


