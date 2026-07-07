# Dependency's
---
### Edit your cpp include paths:  /usr/local/include/** and /usr/include/**
https://github.com/machinezone/IXWebSocket.git


```bash
sudo apt update 
sudo apt install -y git cmake g++ libssl-dev zlib1g-dev

git clone https://github.com/machinezone/IXWebSocket.git
cd IXWebSocket
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```


```sudo apt update
sudo apt install libgps-dev
```

TODO: Update this section


https://github.com/RobotWebTools/web_video_server
https://github.com/christianrauch/camera_ros
