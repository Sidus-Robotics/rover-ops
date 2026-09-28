#!/bin/bash

setup () {
    # Look at docker build reference for flags: -f -t
    docker build -f docker/Dockerfile.ros2 -t ros2 .
}

run_windows() {
    docker compose run --build --rm ros2-windows
}

run_linux() {
    xhost +si:localuser:root
    docker compose run --build --rm ros2-linux
}

# Mac needs https://www.xquartz.org/
run_mac() {
    /opt/X11/bin/xhost +localhost
    docker compose run --build --rm ros2-mac
}