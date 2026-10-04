# Getting Started with ROS2 through Docker

Before starting this guide you will need to have docker desktop installed on your computer if you use Windows or Mac, `if using Linux @TIMNYLI answer this part`.

This guide will teach you how to use docker to develop software for  Sidus Robotics using ROS2, ...`@TIMNYLI`

The goal of developing our software through docker is ease-of-use and portability. In a team where everyone has a unique setup for their development environment standardizing it prevents the **it works on my machine** issue.

## General Commands to Run ROS2

Start your Docker Container you will need to first source the development shell script...

```sh
source dev.sh
```

```txt
Adams-MacBook-Pro:rover-ops adamstrang$ source dev.sh

setup | run to build the dockerfile. 
run_linux | run with linux display configs.
run_windows | run with windows display configs. Needs to be within WSL.
run_mac | run with mac display configs. GUI opens in the browser at http://localhost:6080/vnc.html.
```

Once you have sourced the development script you will be given a choice of run commands that correspond to which operating system you are using. I use MacOS so for me I would enter...

```sh
run_mac
```

This will now build the docker file and open a docker container, this may take some time and require a few GB of free space on your drive. Inside the container you then need to use the setup script for ROS jazzy...

```sh
source /opt/ros/jazzy/setup.bash
```

- **Opening a second terminal:** run `docker ps` to find the container name, then run `docker exec -it <container-name> bash`. The container is deleted when you exit the first terminal.

## Linux

let us know about linux `@TIMNYLI`

## Windows

let us know about windows

- WSL needed

## MacOS

Docker on MacOS cannot show GUI apps like `rviz2` or Gazebo the way Linux can. Docker Desktop runs containers inside a small Linux virtual machine, so the container can't reach your Mac's display directly. XQuartz (the Mac's X11 server) can connect them, but it only supports very old OpenGL versions, and `rviz2` will crash with errors like...

```txt
RenderingAPIException: OpenGL 1.5 is not supported
```

To get around this, the Mac container runs its own virtual display and streams it to your web browser. You do **not** need XQuartz installed.

```sh
source dev.sh
run_mac
```

Once the container is running, open this address in your browser and click **Connect**...

```txt
http://localhost:6080/vnc.html
```

NOTE: ADD IMAGE SHOWING VNC WINDOW IN BROWSER

You should see an empty desktop. Any GUI app you start in the container appears here...

```sh
ros2 run rviz2 rviz2
```

You will now see rviz2 in your browser window.

### How it works

When `run_mac` starts the container, the entrypoint script runs `start-vnc` (`docker/start_vnc.sh`), which launches:

- **Xvfb**: a virtual display (`:1`) that lives inside the container.
- **fluxbox**: a lightweight window manager, so windows can be moved and resized.
- **x11vnc**: shares the virtual display over VNC.
- **noVNC / websockify**: turns the VNC stream into the web page on port `6080`.

OpenGL is rendered in software by Mesa (`llvmpipe`), which supports modern OpenGL, so `rviz2` and Gazebo work. It runs on the CPU, so expect it to be slower than on a Linux machine with a GPU.

### Things to know

- **Networking:** the Mac container uses a bridge network instead of host networking, so the browser page can be reached. ROS nodes inside the container can talk to each other, but they won't discover ROS nodes on other machines, like the rover.

- **No password:** the VNC page has no password, but it is only reachable from your own Mac (`127.0.0.1`).
