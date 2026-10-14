from setuptools import find_packages, setup

setup(
    name="ground-code",
    version="0.0.1",
    install_requires=["pygame-ce", "websockets", "pyserial", "fastapi", "uvicorn"],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "gui_scripts": [
            "ground-station = ground_station.controller_client:main",
        ],
        "console_scripts": [
            "ground-station = ground_station.controller_client:main",
        ],
    },
)
