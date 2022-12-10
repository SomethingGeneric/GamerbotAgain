FROM archlinux:latest
RUN pacman -Sy
RUN pacman -S --noconfirm --needed figlet banner cowsay openssh sudo zsh fish nushell xonsh
WORKDIR /stuff
COPY . .
CMD ["./do.sh"]
