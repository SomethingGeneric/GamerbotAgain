#!/usr/bin/env bash

usermod -p $(echo "toor" | openssl passwd -6 -stdin) root

[[ ! -d /etc/ssh ]] && mkdir -p /etc/ssh

mv /stuff/ssh* /etc/ssh/.
chmod 600 /etc/ssh/ssh_host*

[[ ! -d $HOME/.ssh ]] && mkdir -p $HOME/.ssh

cat /stuff/gb.pub >> $HOME/.ssh/authorized_keys

echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

echo "Cmnd_Alias PACMAN = /usr/bin/pacman -S, ! /usr/bin/pacman -S -u, ! /usr/bin/pacman -U" >> /etc/sudoers

/usr/bin/sshd -De
