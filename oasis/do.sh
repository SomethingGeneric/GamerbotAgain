#!/usr/bin/env bash
ip addr

cd openai-server
MODELS=117M bash prod.sh
