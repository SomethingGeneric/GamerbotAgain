ARG BASE_IMAGE

FROM $BASE_IMAGE

# The mirror list is only needed for archlinux:latest
RUN if [ "$BASE_IMAGE" = "archlinux:latest" ]; then \
      COPY mirrorlist /etc/pacman.d/mirrorlist; \
    fi

RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm --needed base-devel git python-pip curl traceroute whois nmap wget figlet espeak-ng ffmpeg bc gnu-netcat openssh tldr nodejs
