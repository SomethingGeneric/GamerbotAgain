#!/usr/bin/env bash

git clone https://github.com/shawwn/openai-server
cd openai-server

# install dependencies.
pip3 install -r requirements.txt

# grab a gpt-2 model.
python3 download_model.py 117M # or 345M, 774M, 1558M