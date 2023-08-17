FROM archlinux:latest
COPY mirrorlist /etc/pacman.d/mirrorlist
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng ffmpeg bc gnu-netcat openssh tldr nodejs