#!/bin/bash

echo "
setup | run to build the dockerfile. 
run_linux | run with linux display configs.
run_windows | run with windows display configs. Needs to be within WSL.
run_mac | run with mac display configs. Needs some setup with xQuartz.
"

setup () {
    # Look at docker build reference for flags: -f -t
    sudo groupadd docker
    sudo usermod -aG docker
    docker build -f docker/Dockerfile.ros2 -t ros2 .
}

run_windows() {
    docker compose run --build --rm ros2-windows
}

run_linux() {
    xhost +local:root
    docker compose run --build --rm ros2-linux
}

# Mac needs https://www.xquartz.org/
run_mac() {
    /opt/X11/bin/xhost +localhost
    docker compose run --build --rm ros2-mac
}