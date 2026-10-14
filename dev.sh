#!/bin/bash

echo "
setup | run to build the dockerfile. 
run_linux | run with linux display configs.
run_windows | run with windows display configs. Needs to be within WSL.
run_mac | run with mac display configs. GUI opens in the browser at http://localhost:6080/vnc.html.
"

setup () {
    # Need to initialize these.
    git submodule update
    mkdir build
    mkdir install
    mkdir log

    # Look at docker build reference for flags: -f -t
    sudo groupadd docker
    sudo usermod -aG docker $USER 
    docker build -f docker/Dockerfile.ros2 -t ros2 .
}

# Windows needs WSL
run_windows() {
    docker compose run --build --rm ros2-windows
}

run_linux() {
    sudo apt install x11-xserver-utils
    xhost +local:root
    docker compose run --build --rm ros2-linux
}

# Mac renders GUIs inside the container; open http://localhost:6080/vnc.html in a browser.
run_mac() {
    docker compose run --build --rm --service-ports ros2-mac
}