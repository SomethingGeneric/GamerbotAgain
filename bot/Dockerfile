FROM gamerthebase:latest
WORKDIR /bot
COPY . .
RUN python -m venv /bot/venv
RUN /bot/venv/bin/python -m pip install --upgrade pip
RUN /bot/venv/bin/python -m pip install -r /bot/requirements.txt
RUN mkdir -p /root/.ssh
RUN echo "StrictHostKeyChecking no" > /root/.ssh/config
RUN mv /bot/gb /root/.ssh/id_rsa
RUN mv /bot/gb.pub /root/.ssh/id_rsa.pub
RUN chmod -R 600 /root/.ssh
CMD ["/bot/venv/bin/python3", "run.py"]