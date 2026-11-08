FROM ros:jazzy-perception

ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=1000

# Install ros2 packages & other deps.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    cmake \
    git \
    sudo \
    python3-pip \
    python3-setuptools \
    python3-venv \
    ros-jazzy-desktop \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-pcl-ros \
    ros-jazzy-web-video-server \
    ros-jazzy-camera-ros \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# macos web page
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     xvfb \
#     x11vnc \
#     novnc \
#     websockify \
#     fluxbox \
#     mesa-utils \
#     && rm -rf /var/lib/apt/lists/*

RUN if ! id -u "${USER_UID}" >/dev/null 2>&1; then \
    groupadd --gid "${USER_GID}" "${USERNAME}" && \
    useradd --create-home --shell /bin/bash \
    --uid "${USER_UID}" \
    --gid "${USER_GID}" \
    "${USERNAME}"; \
fi

RUN echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > "/etc/sudoers.d/${USERNAME}" \
    && chmod 0440 "/etc/sudoers.d/${USERNAME}"

# Add user to video group to allow access to webcam
RUN usermod --append --groups video $USERNAME

# install and build external libraries
# includes CppLinuxSerial, IXWebSocket, etc
RUN git clone https://github.com/gbmhunter/CppLinuxSerial.git /tmp/CppLinuxSerial \
    && cmake -S /tmp/CppLinuxSerial -B /tmp/CppLinuxSerial/build \
    && cmake --build /tmp/CppLinuxSerial/build --parallel 2 \
    && cmake --install /tmp/CppLinuxSerial/build

RUN git clone https://github.com/machinezone/IXWebSocket.git /tmp/IXWebSocket \
    && cmake -S /tmp/IXWebSocket -B /tmp/IXWebSocket/build \
    && cmake --build /tmp/IXWebSocket/build --parallel 2 \
    && cmake --install /tmp/IXWebSocket/build

USER ${USERNAME}

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /home/${USERNAME}/.bashrc
