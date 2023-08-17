FROM archlinux:latest
COPY mirrorlist /etc/pacman.d/mirrorlist
RUN pacman -Sy --noconfirm
RUN pacman -S --noconfirm --needed figlet banner cowsay openssh sudo
WORKDIR /stuff
COPY . .
RUN chmod +x ./do.sh
CMD ["./do.sh"]
