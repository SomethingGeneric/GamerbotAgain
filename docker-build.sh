#!/bin/sh

ARCH=$(uname -m)

if [ "$ARCH" = "armv7l" ] || [ "$ARCH" = "aarch64" ]; then
    BASE_IMAGE="menci/archlinuxarm"
else
    BASE_IMAGE="archlinux:latest"
fi

echo "Using base image: $BASE_IMAGE"

cd gamerthebase

DOCKER_BUILD_CMD="docker build -t gamerthebase:latest --build-arg BASE_IMAGE=$BASE_IMAGE ."

echo "Running Docker build command: $DOCKER_BUILD_CMD"

$DOCKER_BUILD_CMD

