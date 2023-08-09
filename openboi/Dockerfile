FROM archlinux:latest

# Install system dependencies
RUN pacman -Sy --noconfirm && \
    pacman -S --noconfirm python python-pip && \
    pacman -Scc --noconfirm && \
    pacman -S --noconfirm gcc && \
    pacman -S --noconfirm musl && \
    pacman -S --noconfirm libffi && \
    pacman -S --noconfirm gcc-libs

RUN python3 -m venv venv

# Install PyTorch
RUN venv/bin/pip install torch==1.13.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app/

# Install Python packages
RUN venv/bin/pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

RUN chmod +x launch.sh

# Start the app
CMD ["./launch.sh"]
