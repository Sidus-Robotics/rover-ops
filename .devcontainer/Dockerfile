FROM ros:jazzy-perception

# Add ubuntu user with same UID and GID as your host system, if it doesn't already exist
# Since Ubuntu 24.04, a non-root user is created by default with the name vscode and UID=1000
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN if ! id -u $USER_UID >/dev/null 2>&1; then \
        groupadd --gid $USER_GID $USERNAME && \
        useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME; \
    fi
# Add sudo support for the non-root user
RUN apt-get update && \
    apt-get install -y sudo && \
    echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME

# nbalsom addition - install ros2 packages & other deps.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-desktop \
    ros-jazzy-ros-gz \
    ros-jazzy-ros-gz-bridge \
    ros-jazzy-pcl-conversions \
    ros-jazzy-pcl-ros \
    ros-jazzy-web-video-server \
    ros-jazzy-camera-ros \
    libssl-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# install and build external libraries
# includes CppLinuxSerial, IXWebSocket, etc
# RUN git clone https://github.com/gbmhunter/CppLinuxSerial.git /tmp/CppLinuxSerial \
#     && cmake -S /tmp/CppLinuxSerial -B /tmp/CppLinuxSerial/build \
#     && cmake --build /tmp/CppLinuxSerial/build --parallel 2 \
#     && cmake --install /tmp/CppLinuxSerial/build \
#     && git clone https://github.com/machinezone/IXWebSocket.git /tmp/IXWebSocket \
#     && cmake -S /tmp/IXWebSocket -B /tmp/IXWebSocket/build \
#     && cmake --build /tmp/IXWebSocket/build --parallel 2 \
#     && cmake --install /tmp/IXWebSocket/build 

# macos web page - DONT THINK WE WILL NEED THESE, BUT I PUT HERE JUST IN CASE
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     xvfb \
#     x11vnc \
#     novnc \
#     websockify \
#     fluxbox \
#     mesa-utils \
#     && rm -rf /var/lib/apt/lists/*

# Switch from root to user
USER $USERNAME

# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME

# Update all packages
RUN sudo apt update && sudo apt upgrade -y

# Rosdep update
RUN rosdep update

# Source the ROS setup file
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

################################
## ADD ANY CUSTOM SETUP BELOW ##
################################
