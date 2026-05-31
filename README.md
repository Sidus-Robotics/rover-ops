# rover-ops
Operational "flight" code for the rover. May be combined with rover-sim for the simulation through cloning this repo or vice versa.
---
# Set up
WIP
---
# Dependency's
---
https://github.com/machinezone/IXWebSocket.git


sudo apt update
sudo apt install -y git cmake g++ libssl-dev zlib1g-dev

git clone https://github.com/machinezone/IXWebSocket.git
cd IXWebSocket
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install

git clone https://github.com/uNetworking/uWebSockets.git
cd uWebSockets
sudo apt install build-essential cmake zlib1g-dev libssl-dev
make
sudo make install

# Directory Information
---
WIP, src includes all ros2 packages
---
Edit your cpp include paths:  /usr/local/include/** and /usr/include/**
