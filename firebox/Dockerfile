FROM archlinux:latest
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed openssh sudo firefox geckodriver python-pip
RUN pip3 install selenium
WORKDIR /stuff
COPY . .
RUN chmod +x ./do.sh
CMD ["./do.sh"]
