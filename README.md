<div align="center">

# rover-ops

![CI](https://github.com/Sidus-Robotics/rover-ops/actions/workflows/ci.yaml/badge.svg)

Robotic operating software for use with a student built rover competing in the Canadian International Rover Challenge (CIRC). Built using ROS 2.

[Development Setup](#development-setup) •
[Repository layout](#repository-layout) •
[Contributing](#contributing) •
[Acknowledgements](#acknowledgements)

</div>


## ROS 2 Packages
### 1. Rover Onboard
Onboard computing package. [README](src/rover_onboard/README.md)

### 2. Ground Station
<!-- Change readme location when ground station is converted to a ros2 package -->
Mission control & telemetry package. [README](ground_station/README.md)

## Table of Contents
* [Development Setup](#development-setup)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
* [Repository layout](#repository-layout)
* [Contributing](#contributing)
* [Acknowledgements](#acknowledgements) 


## Development Setup

The supported development environment is the ROS 2 Jazzy devcontainer, which provides the same compiler, ROS packages, and VS Code extensions to teammates using Linux, WSL2, or macOS.

Follow the instructions below for *first time setup:*

### Prerequisites
- Install [VS Code](https://code.visualstudio.com/download) and the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
- Install and configure [Docker Desktop](https://www.docker.com/products/docker-desktop/) for your operating system.

**For Windows users (recommended):**
- Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) and the Ubuntu 24.04 distribution.
- Make sure to enable WSL integration for the installed distribution in Docker Desktop. Under **settings** -> **WSL Integration**.

### Installation

1. **Clone the repository.**

    Open a local folder and clone the `rover-ops` repository.

    **NOTE:** If using WSL on windows, clone the repository within WSL distribution (Ubuntu 24.04) filesystem.

    ```bash
    git clone https://github.com/Sidus-Robotics/rover-ops.git
    ```

2. **Open the `rover-ops/` repository folder in VS Code.**

3. **Select "Reopen in container" when prompted on screen.** 

    If you are not prompted onscreen, you can open the VS Code command palette (Ctrl + Shift + P), and run "Dev Containers: Reopen in Container."

4. **Wait for the container to finish building.**

    The *first* time the container builds it can take a long time.


## Controller Support (Windows, WSL)

WSL does not nativley suppoport to use of usb or bluetooth devices (i.e. controllers). If you need to use a controller for development or testing purposes there are a few extra steps you need to take.

### Example Steps

*Example instructions for controller support. Steps will differ depending on your setup* 

Run this script seperately in WINDOWS (not WSL).

```PS
python3 controller_bridge.py
```

Inside the **devcontainer** run the udp_receiver node:

```bash
colcon build --select-packages rover_teleop
source install/setup.bash
ros2 run rover_teleop udp_receiver
```

## Repository layout

```text
.devcontainer/          VS Code Dev Container configuration
.github/                GitHub workflows and PR template
.vscode/                VS Code related configurations
docs/                   Additional developer documentation
ground_station/         Python ground station package (temp)
src/                    ROS 2 packages live here
utils/                  Helpful scripts for development and testing
```

## Contributing

Welcome to the Sidus Robotics team!

Before contributing to the project, please read our [contributing guidelines](CONTRIBUTING.md).

Check out the `docs/` folder for additional developer documentation that may be helpful for getting started. 

## Acknowledgements
