FROM ghcr.io/archlinux/archlinux:latest
COPY mirrorlist /etc/pacman.d/mirrorlist
COPY pacman.conf /etc/pacman.conf
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng ffmpeg bc openssh tldr nodejs
# RUN pacman -S --noconfirm --needed gnu-netcat
