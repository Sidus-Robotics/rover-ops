#!/bin/bash

echo "
setup | run to build the dockerfile. 
run_linux | run with linux display configs.
run_windows | run with windows display configs. Needs to be within WSL.
run_mac | run with mac display configs. GUI opens in the browser at http://localhost:6080/vnc.html.
"

prepare_submodules() {
    git submodule update --init --recursive
}

setup () {
    prepare_submodules || return 1
    mkdir build
    mkdir install
    mkdir log

    # Need to create a venv
    if [ ! -e ".venv" ]; then
        python3 -m venv .venv
    fi

    # Look at docker build reference for flags: -f -t
    sudo groupadd docker
    sudo usermod -aG docker $USER 
    docker build -f docker/Dockerfile.ros2 -t ros2 .
}

# Windows needs WSL
run_windows() {
    prepare_submodules || return 1
    docker compose run --build --rm ros2-windows
}

run_linux() {
    prepare_submodules || return 1
    sudo apt install x11-xserver-utils
    xhost +local:root
    docker compose run --build --rm ros2-linux
}

# Mac renders GUIs inside the container; open http://localhost:6080/vnc.html in a browser.
run_mac() {
    prepare_submodules || return 1
    docker compose run --build --rm --service-ports ros2-mac
}
