FROM gamerthebase:latest
RUN pacman -S --noconfirm --needed figlet banner cowsay openssh sudo
WORKDIR /stuff
COPY . .
RUN chmod +x ./do.sh
CMD ["./do.sh"]
