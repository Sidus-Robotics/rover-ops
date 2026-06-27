import os 

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

import pygame
from pygame.event import Event
from pygame.joystick import JoystickType
from typing import Dict, List
import logging
import time
import serial
import struct
import math

import multiprocessing
import asyncio
import websockets
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

config: Dict = {
    'sync': 255,
    'x_axis': 0,
    "y_axis" :1,
}

class ControllerProcess:
    _joysticks: Dict
    _done = False
    _events: List[Event]
    _controller: JoystickType
    _controller_event: Event
    _x_axis: int 
    _y_axis: int

    def __init__(self, joysticks: Dict = {}, controller = None, config: Dict = config) -> None:
        if not pygame.joystick.get_init:
            pygame.joystick.init()

        self._joysticks = joysticks
        self._controller = controller
        self._controller_event = None
        self._x_axis = config['x_axis']
        self._y_axis = config['y_axis']
        self._sync =  config['sync']
        self._clock = pygame.time.Clock()
        pygame.init()
    
    def __exit__(self, exc_type, exc, tb):
        pygame.quit()
        return False
    
    def find_events(self) -> None:
        events: List[Event] = pygame.event.get()
        self._events = events
    
    def get_controller(self) -> None:
        for event in self._events:
            if event.type == pygame.JOYDEVICEADDED:
                self._controller_event = event
                logger.info(f"Got Controller: {self._controller_event}")

    def set_controller(self) -> None:
        joy = pygame.joystick.Joystick(
            self._controller_event.device_index
            )
        self._joysticks[joy.get_instance_id()] = joy
        self._controller = self._joysticks[joy.get_instance_id()]
        logger.info(f"Set Controller: {self._controller}")
        
    def get_payload(self) -> int:
        dead_zone = 0.15
        sync = 255
        x = round(self._controller.get_axis(self._x_axis), 2) + 0.0
        y = -1 * round(self._controller.get_axis(self._y_axis), 2) + 0.0

        if abs(x) < dead_zone:
            x = 0
        if abs(y) < dead_zone:
            y = 0
        return sync, x, y
    
    def set_payload(self):
        pass

    def time_step(self):
        pygame.event.pump()
        self._clock.tick(120)
    
def joy():
    ground = ControllerProcess(config=config)  
    try:
        with serial.Serial(port='/dev/ttyUSB0', baudrate=115200) as usb:
            while True:
                ground.find_events()

                if ground._controller == None:
                    ground.get_controller()
                    ground.set_controller()

                if ground._controller != None:
                    sync, x_axis, y_axis = ground.get_payload()
                    
                    """Pack each variable into a 4 byte float.
                    With 1 byte Sync. Total 9 byte payload."""
                    binary_payload = struct.pack('<Bff', sync, x_axis, y_axis) 

                    logger.info(f"Mag: {math.sqrt(pow(x_axis,2) + pow(y_axis,2))}\nX: {x_axis}\nY: {y_axis}\nbin: {binary_payload}")
                    usb.write(binary_payload)

                ground.time_step()
    except Exception as e:
        ground.__exit__
        logging.warning(
            f"{e}: ATTEMPTING RECONNECT."
        )
        time.sleep(1)
        joy()

if __name__ == "__main__":
    joy()
    pygame.quit()