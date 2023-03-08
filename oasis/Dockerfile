FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed sudo python-pip git
WORKDIR /stuff
COPY . .
RUN chmod +x ./setup.sh
RUN ./setup.sh
RUN chmod +x ./do.sh
CMD ["./do.sh"]
