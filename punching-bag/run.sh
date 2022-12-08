#!/usr/bin/env bash

if [[ "$1" == "-d" ]]; then
  docker run -d punchingbag
else
  docker run punchingbag
fi
