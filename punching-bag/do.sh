#!/usr/bin/env bash

ip a

usermod -p $(echo "toor" | openssl passwd -6 -stdin) root

[[ ! -d /etc/ssh ]] && mkdir -p /etc/ssh

mv /stuff/ssh* /etc/ssh/.
chmod 600 /etc/ssh/ssh_host*

[[ ! -d $HOME/.ssh ]] && mkdir -p $HOME/.ssh

cat /stuff/gb.pub >> $HOME/.ssh/authorized_keys

echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

/usr/bin/sshd -De
