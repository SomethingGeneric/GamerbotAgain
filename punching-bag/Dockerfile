FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed figlet banner cowsay openssh sudo
WORKDIR /stuff
COPY . .
CMD ["./do.sh"]
