# rover-ops
---
Operational "flight" code for the rover. May be combined with rover-sim for the simulation through cloning this repo or vice versa.
---
## Submodules

For a new checkout, clone with `git clone --recurse-submodules https://github.com/Sidus-Robotics/rover-ops.git`. In an existing checkout, run `git submodule update --init --recursive` from the repository root after pulling changes. The `dev.sh` setup and run helpers also do this before starting Docker.

# Repository Information
---
### flight-code: 
This directory is for the OBC, also known as the rover-code. It relies on a ROS ecosystem, and can **only be developed on Ubuntu machines.**

### ground-code: 
This directory is for the Ground Station. The Ground Station can be any machine, so long as the dependencies are setup. The methodolgy for the ground-code is portability with the least amount of setup. This is why we are using Python, however in future it may be written in C, C++, and Python.

"/src" folders contain .cpp code, while "/include" folders contain .hpp with respective documentation.

In each folder, i.e flight-code or ground-code, follow their README.md's for instructions on usage. Found here below. . .

[flight-code/README.md](flight-code/README.md)

[ground-code/README.md](ground-code/README.md)
