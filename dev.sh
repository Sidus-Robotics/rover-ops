#!/bin/bash

setup () {
    # Look at docker build reference for flags: -f -t
    docker build -f docker/Dockerfile.ros2 -t ros2 .
}

run() {
    # Look at docker run reference for flags: -i -t --rm
    docker compose run --rm ros2_dev_container bash
}
