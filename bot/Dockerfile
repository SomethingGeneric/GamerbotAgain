FROM gamerthebase:latest
WORKDIR /bot
COPY . .
RUN python3 -m venv venv
RUN venv/bin/pip3 install -r requirements.txt
RUN mkdir -p /root/.ssh
RUN echo "StrictHostKeyChecking no" > /root/.ssh/config
RUN mv /bot/gb /root/.ssh/id_rsa
RUN mv /bot/gb.pub /root/.ssh/id_rsa.pub
RUN chmod -R 600 /root/.ssh
CMD ["venv/bin/python3", "run.py"]
