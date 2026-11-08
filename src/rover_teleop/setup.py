from setuptools import find_packages, setup

package_name = "rover_teleop"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="ubuntu",
    maintainer_email="NicholasBalsom@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "drive_teleop = rover_teleop.drive_teleop:main",
            "udp_receiver = rover_teleop.udp_receiver:main",
            "esp32_serial_bridge = rover_teleop.esp32_serial_bridge:main",
        ],
    },
)
